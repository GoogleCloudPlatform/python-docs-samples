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
streams it to Dialogflow CX for audio transcription, intent detection and
plays back the synthesized audio responses from Dialogflow CX through the
user's speakers.

Dependencies:
  - google-cloud-dialogflow-cx: Cloud Dialogflow CX API client library.
  - termcolor: For colored terminal output.
  - pyaudio: For interfacing with audio input/output devices.

NOTE: pyaudio may have additional dependencies depending on your platform.

Install dependencies using pip:

.. code-block:: sh

   pip install -r requirements.txt

Before Running:

  - Set up a Dialogflow CX agent and obtain the agent name.
  - Ensure you have properly configured Google Cloud authentication
    (e.g., using a service account key).

Information on running the script can be retrieved with:

.. code-block:: sh

   python streaming_detect_intent_infinite.py --help

Say "Hello" to trigger the Default Intent.

Press Ctrl+C to exit the program gracefully.
"""

# [START dialogflow_streaming_detect_intent_infinite]

from __future__ import annotations

import argparse
import asyncio
from collections.abc import AsyncGenerator
import logging
import os
import signal
import struct
import sys
import time
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
DEFAULT_LANGUAGE_CODE = "en-US"
DEFAULT_SAMPLE_RATE = 16000
DEFAULT_DIALOGFLOW_TIMEOUT = 60.0


def get_current_time() -> int:
    """Return Current Time in MS."""
    return int(round(time.time() * 1000))


class AudioIO:
    """Audio Input / Output"""

    def __init__(
        self,
        rate: int,
        chunk_size: int,
    ) -> None:
        self._rate = rate
        self.chunk_size = chunk_size
        self._buff = asyncio.Queue()
        self.closed = False
        self.start_time = None  # only set when first audio received
        self.audio_input = []
        self._audio_interface = pyaudio.PyAudio()
        self._input_audio_stream = None
        self._output_audio_stream = None

        # Get default input device info
        try:
            input_device_info = self._audio_interface.get_default_input_device_info()
            self.input_device_name = input_device_info["name"]
            logger.info(f"Using input device: {self.input_device_name}")
        except IOError:
            logger.error("Could not get default input device info. Exiting.")
            sys.exit(1)

        # Get default output device info
        try:
            output_device_info = self._audio_interface.get_default_output_device_info()
            self.output_device_name = output_device_info["name"]
            logger.info(f"Using output device: {self.output_device_name}")
        except IOError:
            logger.error("Could not get default output device info. Exiting.")
            sys.exit(1)

        # setup input audio stream
        try:
            self._input_audio_stream = self._audio_interface.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self._rate,
                input=True,
                frames_per_buffer=self.chunk_size,
                stream_callback=self._fill_buffer,
            )
        except OSError as e:
            logger.error(f"Could not open input stream: {e}. Exiting.")
            sys.exit(1)

        # setup output audio stream
        try:
            self._output_audio_stream = self._audio_interface.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self._rate,
                output=True,
                frames_per_buffer=self.chunk_size,
            )
            self._output_audio_stream.stop_stream()
        except OSError as e:
            logger.error(f"Could not open output stream: {e}. Exiting.")
            sys.exit(1)

    def __enter__(self) -> "AudioIO":
        """Opens the stream."""
        self.closed = False
        return self

    def __exit__(self, *args: any) -> None:
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
    ) -> tuple[None, int]:
        """Continuously collect data from the audio stream, into the buffer."""

        # Capture the true start time when the first chunk is received
        if self.start_time is None:
            self.start_time = get_current_time()

        # only capture microphone input when output audio stream is stopped
        if self._output_audio_stream and self._output_audio_stream.is_stopped():
            self._buff.put_nowait(in_data)
        self.audio_input.append(in_data)

        return None, pyaudio.paContinue

    async def generator(self) -> AsyncGenerator[bytes, None]:
        """Stream Audio from microphone to API and to local buffer."""
        while not self.closed:
            try:
                chunk = await asyncio.wait_for(self._buff.get(), timeout=1)

                if chunk is None:
                    logger.debug("[generator] Received None chunk, ending stream")
                    return

                data = [chunk]

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

                combined_data = b"".join(data)
                yield combined_data

            except asyncio.TimeoutError:
                logger.debug(
                    "[generator] No audio chunk received within timeout, continuing..."
                )
                continue

    def play_audio(self, audio_data: bytes) -> None:
        """Plays audio from the given bytes data, removing WAV header if needed."""
        # Remove WAV header if present
        if audio_data.startswith(b"RIFF"):
            try:
                # Attempt to unpack the WAV header to determine header size.
                header_size = struct.calcsize("<4sI4s4sIHHIIHH4sI")
                header = struct.unpack("<4sI4s4sIHHIIHH4sI", audio_data[:header_size])
                logger.debug(f"WAV header detected: {header}")
                audio_data = audio_data[header_size:]  # Remove the header
            except struct.error as e:
                logger.error(f"Error unpacking WAV header: {e}")
                # If header parsing fails, play the original data; may not be a valid WAV

        # Play the raw PCM audio
        try:
            self._output_audio_stream.start_stream()
            self._output_audio_stream.write(audio_data)
        finally:
            self._output_audio_stream.stop_stream()


class DialogflowCXStreaming:
    """Manages the interaction with the Dialogflow CX Streaming API."""

    def __init__(
        self,
        agent_name: str,
        language_code: str,
        single_utterance: bool,
        model: str | None,
        voice: str | None,
        sample_rate: int,
        dialogflow_timeout: float,
        debug: bool,
    ) -> None:
        """Initializes the Dialogflow CX Streaming API client."""
        try:
            _, project, _, location, _, agent_id = agent_name.split("/")
        except ValueError:
            raise ValueError(
                "Invalid agent name format. Expected format: projects/<project>/locations/<location>/agents/<agent_id>"
            )
        if location != "global":
            client_options = ClientOptions(
                api_endpoint=f"{location}-dialogflow.googleapis.com",
                quota_project_id=project,
            )
        else:
            client_options = ClientOptions(quota_project_id=project)

        self.client = dialogflowcx_v3.SessionsAsyncClient(client_options=client_options)
        self.agent_name = agent_name
        self.language_code = language_code
        self.single_utterance = single_utterance
        self.model = model
        self.session_id = str(uuid.uuid4())
        self.dialogflow_timeout = dialogflow_timeout
        self.debug = debug
        self.sample_rate = sample_rate
        self.voice = voice

        if self.debug:
            logger.setLevel(logging.DEBUG)
            logger.debug("Debug logging enabled")

    async def generate_streaming_detect_intent_requests(
        self, audio_queue: asyncio.Queue
    ) -> AsyncGenerator[dialogflowcx_v3.StreamingDetectIntentRequest, None]:
        """Generates the requests for the streaming API."""
        audio_config = dialogflowcx_v3.InputAudioConfig(
            audio_encoding=dialogflowcx_v3.AudioEncoding.AUDIO_ENCODING_LINEAR_16,
            sample_rate_hertz=self.sample_rate,
            model=self.model,
            single_utterance=self.single_utterance,
        )
        query_input = dialogflowcx_v3.QueryInput(
            language_code=self.language_code,
            audio=dialogflowcx_v3.AudioInput(config=audio_config),
        )
        output_audio_config = dialogflowcx_v3.OutputAudioConfig(
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

        # First request contains session ID, query input audio config, and output audio config
        request = dialogflowcx_v3.StreamingDetectIntentRequest(
            session=f"{self.agent_name}/sessions/{self.session_id}",
            query_input=query_input,
            enable_partial_response=True,
            output_audio_config=output_audio_config,
        )
        if self.debug:
            logger.debug(f"Sending initial request: {request}")
        yield request

        # Subsequent requests contain audio only
        while True:
            try:
                chunk = await audio_queue.get()
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
        requests_generator = self.generate_streaming_detect_intent_requests(audio_queue)

        retry_policy = retries.AsyncRetry(
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
            async def api_call():
                logger.debug("Initiating streaming request")
                return await self.client.streaming_detect_intent(
                    requests=requests_generator
                )

            response_stream = await retry_policy(api_call)()
            return response_stream

        try:
            responses = await streaming_request_with_retry()

            # Use async for to iterate over the responses, WITH timeout
            response_iterator = responses.__aiter__()  # Get the iterator
            while True:
                try:
                    response = await asyncio.wait_for(
                        response_iterator.__anext__(), timeout=self.dialogflow_timeout
                    )
                    if self.debug and response:
                        response_copy = MessageToDict(response._pb)
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
                    continue  # Continue to the next iteration, don't break
                except GoogleAPIError as e:  # Keep error handling
                    logger.error(f"Error: {e}")
                    if e.code == 500:  # Consider making this more robust
                        logger.warning("Encountered a 500 error during iteration.")

        except GoogleAPIError as e:
            logger.error(f"Error: {e}")
            if e.code == 500:
                logger.warning("Encountered a 500 error during iteration.")


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
            response = await asyncio.wait_for(
                response_iterator.__anext__(), timeout=dialogflow_timeout
            )

            if (
                response
                and response.detect_intent_response
                and response.detect_intent_response.output_audio
            ):
                audioIO.play_audio(response.detect_intent_response.output_audio)

            if (
                response
                and response.detect_intent_response
                and response.detect_intent_response.query_result
            ):
                query_result = response.detect_intent_response.query_result
                # Check for end_interaction in response messages
                if query_result.response_messages:
                    for message in query_result.response_messages:
                        if message.text:
                            logger.info(f"Dialogflow output: {message.text.text[0]}")
                        if message._pb.HasField("end_interaction"):
                            logger.info("End interaction detected.")
                            return False  # Signal to *not* restart the loop (exit)

                if query_result.intent and query_result.intent.display_name:
                    logger.info(f"Detected intent: {query_result.intent.display_name}")

                # ensure audio stream restarts
                return True
            elif response and response.recognition_result:
                transcript = response.recognition_result.transcript
                if transcript:
                    if response.recognition_result.is_final:
                        logger.info(f"Final transcript: {transcript}")
                        await audio_queue.put(None)  # Signal end of input
                    else:
                        print(
                            colored(transcript, "yellow"),
                            end="\r",
                        )
            else:
                logger.debug("No transcript in recognition result.")

        except StopAsyncIteration:
            logger.debug("End of response stream in listen_print_loop")
            break
        except asyncio.TimeoutError:
            logger.warning("Timeout waiting for response in listen_print_loop")
            continue  # Crucial: Continue, don't return, on timeout
        except Exception as e:
            logger.error(f"Error in listen_print_loop: {e}")
            return False  # Exit on any error within the loop

    return True  # Always return after the async for loop completes


async def handle_audio_input_output(
    dialogflow_streaming: DialogflowCXStreaming,
    audioIO: AudioIO,
    audio_queue: asyncio.Queue,
) -> None:
    """Handles audio input and output concurrently."""

    async def cancel_push_task(push_task: asyncio.Task | None) -> None:
        """Helper function to cancel push task safely."""
        if push_task is not None and not push_task.done():
            push_task.cancel()
            try:
                await push_task
            except asyncio.CancelledError:
                logger.debug("Push task cancelled successfully")

    push_task = None
    try:
        push_task = asyncio.create_task(
            push_to_audio_queue(audioIO.generator(), audio_queue)
        )
        while True:  # restart streaming here.
            responses = dialogflow_streaming.streaming_detect_intent(audio_queue)

            should_continue = await listen_print_loop(
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
                break  # exit while loop

            logger.debug("Restarting audio streaming loop")

    except asyncio.CancelledError:
        logger.warning("Handling of audio input/output was cancelled.")
        await cancel_push_task(push_task)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")


async def main(
    agent_name: str,
    language_code: str = DEFAULT_LANGUAGE_CODE,
    single_utterance: bool = False,
    model: str | None = None,
    voice: str | None = None,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    dialogflow_timeout: float = DEFAULT_DIALOGFLOW_TIMEOUT,
    debug: bool = False,
) -> None:
    """Start bidirectional streaming from microphone input to speech API"""

    chunk_size = int(sample_rate * CHUNK_SECONDS)

    audioIO = AudioIO(sample_rate, chunk_size)
    dialogflow_streaming = DialogflowCXStreaming(
        agent_name,
        language_code,
        single_utterance,
        model,
        voice,
        sample_rate,
        dialogflow_timeout,
        debug,
    )

    logger.info(f"Chunk size: {audioIO.chunk_size}")
    logger.info(f"Using input device: {audioIO.input_device_name}")
    logger.info(f"Using output device: {audioIO.output_device_name}")

    # Signal handler function
    def signal_handler(sig: int, frame: any) -> None:
        print(colored("\nExiting gracefully...", "yellow"))
        audioIO.closed = True  # Signal to stop the main loop
        sys.exit(0)

    # Set the signal handler for Ctrl+C (SIGINT)
    signal.signal(signal.SIGINT, signal_handler)

    with audioIO:
        logger.info(f"NEW REQUEST: {get_current_time() / 1000}")
        audio_queue = asyncio.Queue()

        try:
            # Apply overall timeout to the entire interaction
            await asyncio.wait_for(
                handle_audio_input_output(dialogflow_streaming, audioIO, audio_queue),
                timeout=dialogflow_streaming.dialogflow_timeout,
            )
        except asyncio.TimeoutError:
            logger.error(
                f"Dialogflow interaction timed out after {dialogflow_streaming.dialogflow_timeout} seconds."
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("agent_name", help="Agent Name")
    parser.add_argument(
        "--language_code",
        type=str,
        default=DEFAULT_LANGUAGE_CODE,
        help="Specify the language code (default: en-US)",
    )
    parser.add_argument(
        "--single_utterance",
        action="store_true",
        help="Enable single utterance mode (default: False)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Specify the speech recognition model to use (default: None)",
    )
    parser.add_argument(
        "--voice",
        type=str,
        default=None,
        help="Specify the voice for output audio (default: None)",
    )
    parser.add_argument(
        "--sample_rate",
        type=int,
        default=DEFAULT_SAMPLE_RATE,
        help="Specify the sample rate in Hz (default: 16000)",
    )
    parser.add_argument(
        "--dialogflow_timeout",
        type=float,
        default=DEFAULT_DIALOGFLOW_TIMEOUT,
        help="Specify the Dialogflow API timeout in seconds (default: 60)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )

    args = parser.parse_args()
    asyncio.run(
        main(
            args.agent_name,
            args.language_code,
            args.single_utterance,
            args.model,
            args.voice,
            args.sample_rate,
            args.dialogflow_timeout,
            args.debug,
        )
    )

# [END dialogflow_streaming_detect_intent_infinite]
