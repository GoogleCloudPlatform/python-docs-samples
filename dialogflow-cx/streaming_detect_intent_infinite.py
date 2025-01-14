#!/usr/bin/env python

# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This script implements a real-time bidirectional streaming audio interface
with Google Cloud Dialogflow CX. It captures audio from the user's microphone,
streams it to Dialogflow CX for intent detection and natural language
processing, and plays back the synthesized audio responses from Dialogflow
CX through the user's speakers.

Dependencies:

    - google-cloud-dialogflow-cx: Cloud Dialogflow CX API client library.
    - termcolor: For colored terminal output.
    - pyaudio: For interfacing with audio input/output devices.

    Install dependencies using pip:

    ```bash
    pip install -r requirements.txt
    ```

Before Running:

    - Set up a Dialogflow CX agent and obtain the agent name.
    - Ensure you have properly configured Google Cloud authentication
      (e.g., using a service account key).

To Run:
    - Execute the script from the command line, providing the necessary
       arguments:

    ```bash
    ./streaming_detect_intent_infinite.py projects/your-project/locations/your-location/agents/your-agent-id --language_code en-US --sample_rate 16000  --single_utterance
    ```

    Example:

    ```bash
    python dialogflow_cx_streaming.py projects/your-project/locations/your-location/agents/your-agent-id --language_code en-US --sample_rate 16000  --single_utterance
    ```

    Replace `projects/your-project/locations/your-location/agents/your-agent-id`
    with your Dialogflow CX agent name.

    Optional Arguments:
        --help: Get help about command line arguments.
        --debug: Enable debug logging.
        --model: Specify the speech recognition model.
        --language_code: Specify the language code (default: en-US).
        --dialogflow_timeout: Set the Dialogflow API timeout in seconds (default: 60).
        --sample_rate: Set the audio sample rate in Hz (default: 16000).
        --voice: Specify the voice for output audio.
        --single_utterance: Enable single utterance mode. NO_INPUT events only work with single_utterance enabled!

The script will start capturing audio from the default microphone, stream it
to Dialogflow CX, and play back the audio responses. Press Ctrl+C to exit the
program gracefully.
"""

import argparse
import asyncio
import logging
import os
import signal
import struct
import sys
import time
from typing import Any, AsyncGenerator, List, Optional, Tuple
import uuid

from google.api_core import retry as retries
from google.api_core.client_options import ClientOptions
from google.api_core.exceptions import GoogleAPIError, ServiceUnavailable
from google.cloud import dialogflowcx_v3
from google.protobuf.json_format import MessageToDict

import pyaudio
from termcolor import colored

# TODO: Remove once GRPC log spam is gone see https://github.com/grpc/grpc/issues/37642
os.environ["GRPC_VERBOSITY"] = "NONE"

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

CHUNK_SECONDS = 0.1


def get_current_time() -> int:
    """Return Current Time in MS."""
    return int(round(time.time() * 1000))


class AudioIO:
    """Audio Input / Output"""

    def __init__(
        self,
        rate: int,
        chunk_size: int,
        audio_encoding: str = "LINEAR16",
        output_audio_encoding: str = "LINEAR16",
    ) -> None:
        self._rate: int = rate
        self.chunk_size: int = chunk_size
        self._num_channels: int = 1
        self._buff: asyncio.Queue[Optional[bytes]] = asyncio.Queue()
        self.closed: bool = True
        self.start_time: Optional[int] = None  # only set when first audio received
        self.restart_counter: int = 0
        self.audio_input: List[bytes] = []
        self.last_audio_input: List[bytes] = []
        self.result_end_time: Optional[float] = None
        self.is_final_end_time: Optional[float] = None
        self.final_request_end_time: Optional[float] = None
        self.bridging_offset: int = 0
        self.last_transcript_was_final: bool = False
        self.new_stream: bool = True
        self._audio_interface: pyaudio.PyAudio = pyaudio.PyAudio()
        self._input_audio_stream: Optional[pyaudio.Stream] = None
        self._output_audio_stream: Optional[pyaudio.Stream] = None
        self.audio_encoding: str = audio_encoding
        self.output_audio_encoding: str = output_audio_encoding
        self.audio_format: int = pyaudio.paInt16
        self.input_device_name: str
        self.output_device_name: str

        # Initialize input and output streams
        self._init_streams()

    def _init_streams(self) -> None:
        """Initializes audio input and output streams."""
        # Get default input device info
        try:
            input_device_info: dict = (
                self._audio_interface.get_default_input_device_info()
            )
            self.input_device_name = input_device_info["name"]
            logger.info(f"Using input device: {self.input_device_name}")
        except IOError:
            self.input_device_name = "Could not get default input device name"
            logger.warning("Could not get default input device info.")

        # Get default output device info
        try:
            output_device_info: dict = (
                self._audio_interface.get_default_output_device_info()
            )
            self.output_device_name = output_device_info["name"]
            logger.info(f"Using output device: {self.output_device_name}")
        except IOError:
            self.output_device_name = "Could not get default output device name"
            logger.warning("Could not get default output device info.")

        self._input_audio_stream = self._audio_interface.open(
            format=self.audio_format,
            channels=self._num_channels,
            rate=self._rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            stream_callback=self._fill_buffer,
        )

        self._output_audio_stream = self._audio_interface.open(
            format=self.audio_format,
            channels=self._num_channels,
            rate=self._rate,
            output=True,
            frames_per_buffer=self.chunk_size,
        )
        self._output_audio_stream.stop_stream()

    def __enter__(self) -> "AudioIO":
        """Opens the stream."""
        self.closed = False
        return self

    def __exit__(self, type: Any, value: Any, traceback: Any) -> None:
        """Closes the stream and releases resources."""
        self.closed = True
        if self._input_audio_stream:
            self._input_audio_stream.stop_stream()
            self._input_audio_stream.close()
            self._input_audio_stream = None

        if self._output_audio_stream:
            self._output_audio_stream.stop_stream()
            self._output_audio_stream.close()
            self._output_audio_stream = None

        # Signal the generator to terminate
        self._buff.put_nowait(None)
        self._audio_interface.terminate()

    def _fill_buffer(
        self, in_data: bytes, frame_count: int, time_info: dict, status_flags: int
    ) -> Tuple[None, int]:
        """Continuously collect data from the audio stream, into the buffer."""

        # Capture the true start time when the first chunk is received
        if self.start_time is None:
            self.start_time = get_current_time()

        # only capture microphone input when output audio stream is stopped
        if self._output_audio_stream.is_stopped():
            self._buff.put_nowait(in_data)
        self.audio_input.append(in_data)

        return None, pyaudio.paContinue

    async def generator(self) -> AsyncGenerator[bytes, None]:
        """Stream Audio from microphone to API and to local buffer."""
        while not self.closed:
            try:
                chunk: Optional[bytes] = await asyncio.wait_for(
                    self._buff.get(), timeout=1
                )

                if chunk is None:
                    logger.debug("[generator] Received None chunk, ending stream")
                    return

                data: List[bytes] = [chunk]

                while True:
                    try:
                        chunk = self._buff.get_nowait()
                        if chunk is None:
                            logger.debug(
                                "[generator] Received None chunk (nowait), ending stream"
                            )
                            return
                        data.append(chunk)
                    except asyncio.QueueEmpty:
                        break

                combined_data: bytes = b"".join(data)
                yield combined_data

            except asyncio.TimeoutError:
                logger.debug(
                    "[generator] No audio chunk received within timeout, continuing..."
                )
                continue

    def _extract_wav_header(self, audio_data: bytes) -> bytes:
        """Extracts the WAV header from the audio data.

        Args:
            audio_data: The audio data potentially containing a WAV header.

        Returns:
            The audio data without the WAV header.
        """
        if audio_data[:4] == b"RIFF":
            try:
                header: Tuple[
                    bytes, int, bytes, bytes, int, int, int, int, int, int, bytes, int
                ] = struct.unpack("<4sI4s4sIHHIIHH4sI", audio_data[:44])
                logger.debug(f"WAV header detected: {header}")
                return audio_data[44:]
            except struct.error as e:
                logger.error(f"Error unpacking WAV header: {e}")
                return audio_data
        else:
            logger.warning("No WAV header found.")
            return audio_data

    def play_audio(self, audio: bytes) -> None:
        """Plays audio from the given bytes data and removes WAV header."""
        # Remove WAV header if present
        audio = self._extract_wav_header(audio)

        # Play the raw PCM audio
        try:
            self._output_audio_stream.start_stream()
            self._output_audio_stream.write(audio)
        finally:
            self._output_audio_stream.stop_stream()


class DialogflowCXStreaming:
    """Manages the interaction with the Dialogflow CX Streaming API."""

    def __init__(
        self,
        agent_name: str,
        language_code: str,
        model: str,
        dialogflow_timeout: float,
        debug: bool = False,
        sample_rate: int = 16000,
        audio_encoding: str = "LINEAR16",
        output_audio_encoding: str = "LINEAR16",
        voice: Optional[str] = None,
        single_utterance: bool = False,
    ) -> None:
        """Initializes the Dialogflow CX Streaming API client."""
        try:
            _, project, _, location, _, agent_id = agent_name.split('/')
        except ValueError:
            raise ValueError('Invalid agent name format. Expected format: projects/<project>/locations/<location>/agents/<agent_id>')
        if location != 'global':
            client_options: ClientOptions = ClientOptions(
                api_endpoint=f'{location}-dialogflow.googleapis.com',
                quota_project_id=project,
            )
        else:
            client_options = ClientOptions(quota_project_id=project)
        self.client: dialogflowcx_v3.SessionsAsyncClient = (
            dialogflowcx_v3.SessionsAsyncClient(client_options=client_options)
        )
        self.agent_name: str = agent_name
        self.language_code: str = language_code
        self.model: str = model
        self.session_id: str = str(uuid.uuid4())
        self.dialogflow_timeout: float = dialogflow_timeout
        self.debug: bool = debug
        self.sample_rate: int = sample_rate
        self.audio_encoding: str = audio_encoding
        self.voice: Optional[str] = voice
        self.output_audio_encoding: str = output_audio_encoding
        self.single_utterance: bool = single_utterance

        if self.debug:
            logger.setLevel(logging.DEBUG)
            logger.debug("Debug logging enabled")

    async def generate_streaming_detect_intent_requests(
        self, audio_queue: asyncio.Queue
    ) -> AsyncGenerator[dialogflowcx_v3.StreamingDetectIntentRequest, None]:
        """Generates the requests for the streaming API."""
        audio_config: dialogflowcx_v3.InputAudioConfig = (
            dialogflowcx_v3.InputAudioConfig(
                audio_encoding=dialogflowcx_v3.AudioEncoding.AUDIO_ENCODING_LINEAR_16,
                sample_rate_hertz=self.sample_rate,
                model=self.model,
                single_utterance=self.single_utterance,
            )
        )
        query_input: dialogflowcx_v3.QueryInput = dialogflowcx_v3.QueryInput(
            language_code=self.language_code,
            audio=dialogflowcx_v3.AudioInput(config=audio_config),
        )
        output_audio_config: dialogflowcx_v3.OutputAudioConfig = (
            dialogflowcx_v3.OutputAudioConfig(
                audio_encoding=dialogflowcx_v3.OutputAudioEncoding.OUTPUT_AUDIO_ENCODING_LINEAR_16,
                sample_rate_hertz=self.sample_rate,
                synthesize_speech_config=(
                    dialogflowcx_v3.SynthesizeSpeechConfig(
                        voice=dialogflowcx_v3.VoiceSelectionParams(name=self.voice)
                    )
                    if self.voice
                    else None
                ),
            )
        )

        # First request contains session ID, query input audio config, and output audio config with audio_encoding
        request: dialogflowcx_v3.StreamingDetectIntentRequest = (
            dialogflowcx_v3.StreamingDetectIntentRequest(
                session=f"{self.agent_name}/sessions/{self.session_id}",
                query_input=query_input,
                enable_partial_response=True,
                output_audio_config=output_audio_config,
            )
        )
        if self.debug:
            logger.debug(f"Sending initial request: {request}")
        yield request

        # Subsequent requests contain audio only
        while True:
            try:
                chunk: Optional[bytes] = await audio_queue.get()
                if chunk is None:
                    logger.debug(
                        "[generate_streaming_detect_intent_requests] Received None chunk, signaling end of utterance"
                    )
                    break  # Exit the generator

                request = dialogflowcx_v3.StreamingDetectIntentRequest(
                    query_input=dialogflowcx_v3.QueryInput(
                        audio=dialogflowcx_v3.AudioInput(audio=chunk)
                    )
                )
                yield request

            except asyncio.CancelledError:
                logger.debug(
                    "[generate_streaming_detect_intent_requests] Audio queue processing was cancelled"
                )
                break

    async def streaming_detect_intent(
        self,
        audio_queue: asyncio.Queue,
    ) -> AsyncGenerator[dialogflowcx_v3.StreamingDetectIntentResponse, None]:
        """Transcribes the audio into text and yields each response."""
        requests_generator: AsyncGenerator[
            dialogflowcx_v3.StreamingDetectIntentRequest, None
        ] = self.generate_streaming_detect_intent_requests(audio_queue)

        retry_policy: retries.AsyncRetry = retries.AsyncRetry(
            predicate=retries.if_exception_type(ServiceUnavailable),
            initial=0.5,
            maximum=60.0,
            multiplier=2.0,
            timeout=300.0,
            on_error=lambda e: logger.warning(f"Retrying due to error: {e}"),
        )

        async def streaming_request_with_retry() -> (
            AsyncGenerator[dialogflowcx_v3.StreamingDetectIntentResponse, None]
        ):
            async def api_call() -> (
                dialogflowcx_v3.SessionsAsyncClient.streaming_detect_intent
            ):
                logger.debug("Initiating streaming request")
                return await self.client.streaming_detect_intent(
                    requests=requests_generator
                )

            return await retry_policy(api_call)()

        try:
            responses: Optional[
                AsyncGenerator[dialogflowcx_v3.StreamingDetectIntentResponse, None]
            ] = await streaming_request_with_retry()

            if responses is None:
                logger.error("Failed after multiple retries.")
                return

            # Use __aiter__() and __anext__() for iteration
            response_iterator = responses.__aiter__()
            while True:
                try:
                    response: dialogflowcx_v3.StreamingDetectIntentResponse = (
                        await asyncio.wait_for(
                            response_iterator.__anext__(),
                            timeout=self.dialogflow_timeout,
                        )
                    )
                    if self.debug and response:
                        # Create a copy of the response for logging
                        response_copy: dict = MessageToDict(response._pb)
                        if response_copy.get("detectIntentResponse"):
                            response_copy["detectIntentResponse"][
                                "outputAudio"
                            ] = "REMOVED"
                        logger.debug(f"Received response: {response_copy}")
                    yield response
                except StopAsyncIteration:
                    logger.debug("End of response stream")
                    break
                except asyncio.TimeoutError:
                    logger.warning("Timeout waiting for response from Dialogflow.")
                    continue
                except GoogleAPIError as e:
                    logger.error(f"Error: {e}")
                    if e.code == 500:
                        logger.warning("Encountered a 500 error during iteration.")

        except GoogleAPIError as e:
            logger.error(f"Error: {e}")
            if e.code == 500:
                logger.warning("Encountered a 500 error during iteration.")

        finally:
            logger.debug("streaming_detect_intent finally block reached")


async def push_to_audio_queue(
    audio_generator: AsyncGenerator, audio_queue: asyncio.Queue
) -> None:
    """Pushes audio chunks from a generator to an asyncio queue."""
    try:
        async for chunk in audio_generator:
            await audio_queue.put(chunk)
    except Exception as e:
        logger.error(f"Error in push_to_audio_queue: {e}")


async def listen_print_loop(
    responses: AsyncGenerator[dialogflowcx_v3.StreamingDetectIntentResponse, None],
    audioIO: AudioIO,
    audio_queue: asyncio.Queue,
    dialogflow_timeout: float,
) -> bool:
    """Iterates through server responses and prints them."""
    response_iterator = responses.__aiter__()
    while True:
        try:
            response: dialogflowcx_v3.StreamingDetectIntentResponse = (
                await asyncio.wait_for(
                    response_iterator.__anext__(), timeout=dialogflow_timeout
                )
            )

            if response.detect_intent_response:
                if response.detect_intent_response.output_audio:
                    audioIO.play_audio(response.detect_intent_response.output_audio)

                # Check for end_interaction in response messages
                for (
                    message
                ) in response.detect_intent_response.query_result.response_messages:
                    if message._pb.HasField("end_interaction"):
                        logger.info("End interaction detected.")
                        return False  # Signal to not restart the loop
                    if message.text:
                        logger.info(f"Dialogflow output: {message.text.text[0]}")

                if response.detect_intent_response.query_result.intent.display_name:
                    logger.info(
                        f"Detected intent: {response.detect_intent_response.query_result.intent.display_name}"
                    )

                # ensure audio stream restarts
                return True

            transcript: str = response.recognition_result.transcript
            if transcript:
                if response.recognition_result.is_final:
                    logger.info(f"Final transcript: {transcript}")
                    audioIO.is_final_end_time = get_current_time() / 1000
                    audioIO.last_transcript_was_final = True
                    await audio_queue.put(None)
                else:
                    audioIO.result_end_time = get_current_time() / 1000
                    print(
                        colored(f"{audioIO.result_end_time}: {transcript}", "yellow"),
                        end="\r",
                    )
                    audioIO.last_transcript_was_final = False
            else:
                logger.debug("No transcript in recognition result.")

        except StopAsyncIteration:
            logger.debug("End of response stream in listen_print_loop")
            return True  # Restart loop if the stream ends without end_interaction
        except asyncio.TimeoutError:
            logger.warning("Timeout waiting for response in listen_print_loop")
            continue
        except Exception as e:
            logger.error(f"Error in listen_print_loop: {e}")
            break

    return True  # Default to restarting the loop


async def handle_audio_input_output(
    dialogflow_streaming: DialogflowCXStreaming,
    audioIO: AudioIO,
    audio_queue: asyncio.Queue,
) -> None:
    """Handles audio input and output concurrently."""

    async def cancel_push_task(push_task: Optional[asyncio.Task]) -> None:
        """Helper function to cancel push task safely."""
        if push_task is not None and not push_task.done():
            push_task.cancel()
            try:
                await push_task
            except asyncio.CancelledError:
                logger.debug("Push task cancelled successfully")

    push_task: Optional[asyncio.Task] = None
    try:
        async with asyncio.TaskGroup() as tg:
            push_task = tg.create_task(
                push_to_audio_queue(audioIO.generator(), audio_queue)
            )
            while True:
                responses: AsyncGenerator[
                    dialogflowcx_v3.StreamingDetectIntentResponse, None
                ] = dialogflow_streaming.streaming_detect_intent(audio_queue)
                should_continue: bool = await listen_print_loop(
                    responses,
                    audioIO,
                    audio_queue,
                    dialogflow_streaming.dialogflow_timeout,
                )
                if not should_continue:
                    logger.debug(
                        "End interaction detected, exiting handle_audio_input_output"
                    )
                    await cancel_push_task(push_task)
                    break
                logger.debug("Restarting listen_print_loop")
    except asyncio.CancelledError:
        logger.warning("Handling of audio input/output was cancelled.")
        await cancel_push_task(push_task)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")


async def main(
    agent_name: str,
    debug: bool,
    model: str,
    language_code: str,
    dialogflow_timeout: float,
    sample_rate: int,
    voice: Optional[str],
    single_utterance: bool,
) -> None:
    """Start bidirectional streaming from microphone input to speech API"""

    chunk_size: int = int(sample_rate * CHUNK_SECONDS)

    audioIO: AudioIO = AudioIO(sample_rate, chunk_size)
    dialogflow_streaming: DialogflowCXStreaming = DialogflowCXStreaming(
        agent_name,
        language_code,
        model,
        dialogflow_timeout,
        debug,
        sample_rate,
        "LINEAR16",
        "LINEAR16",
        voice,
        single_utterance,
    )

    logger.info(f"Chunk size: {audioIO.chunk_size}")
    logger.info(f"Using input device: {audioIO.input_device_name}")
    if hasattr(audioIO, "output_device_name"):
        logger.info(f"Using output device: {audioIO.output_device_name}")
    sys.stdout.write(
        colored('\nListening, say "Quit" or "Exit" to stop.\n\n', "yellow")
    )
    sys.stdout.write(colored("End (ms)       Transcript Results/Status\n", "yellow"))
    sys.stdout.write(
        colored("=====================================================\n", "yellow")
    )

    # Signal handler function
    def signal_handler(sig: int, frame: Any) -> None:
        print(colored("\nExiting gracefully...", "yellow"))
        audioIO.closed = True  # Signal to stop the main loop
        sys.exit(0)

    # Set the signal handler for Ctrl+C (SIGINT)
    signal.signal(signal.SIGINT, signal_handler)

    with audioIO:
        logger.info(f"NEW REQUEST: {get_current_time() / 1000}")

        audio_queue: asyncio.Queue = asyncio.Queue()

        await handle_audio_input_output(dialogflow_streaming, audioIO, audio_queue)


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("agent_name", help="Agent Name")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Specify the speech recognition model to use (default: None)",
    )
    parser.add_argument(
        "--language_code",
        type=str,
        default="en-US",
        help="Specify the language code (default: en-US)",
    )
    parser.add_argument(
        "--dialogflow_timeout",
        type=float,
        default=60.0,
        help="Specify the Dialogflow API timeout in seconds (default: 60)",
    )
    parser.add_argument(
        "--sample_rate",
        type=int,
        default=16000,
        help="Specify the sample rate in Hz (default: 16000 for LINEAR16 audio encoding)",
    )
    parser.add_argument(
        "--voice",
        type=str,
        default=None,
        help="Specify the voice for output audio (default: None)",
    )
    parser.add_argument(
        "--single_utterance",
        action="store_true",
        help="Enable single utterance mode (default: False)",
    )
    args: argparse.Namespace = parser.parse_args()
    asyncio.run(
        main(
            args.agent_name,
            args.debug,
            args.model,
            args.language_code,
            args.dialogflow_timeout,
            args.sample_rate,
            args.voice,
            args.single_utterance,
        )
    )
