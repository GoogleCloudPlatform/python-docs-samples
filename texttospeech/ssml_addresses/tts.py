"""Source code for SSML Tutorial for Cloud Text-to-Speech API."""

# [START imports]
from __future__ import print_function
from google.cloud import texttospeech
# [END imports]


# [START audio]
def ssml_to_audio(ssml_text, outfile):
    # Generates SSML text from plaintext.

    # Given a string of SSML text and an output file name, this function calls the
    # Text-to-Speech API. The API returns a synthetic audio version of the text,
    # formatted according to the SSML commands. This function stores the synthetic
    # audio to the designated output file.

    # Args:
        # ssml_text: string of SSML text
        # outfile: string name of file under which to save audio output

    # Returns:
        # nothing

    # Checks to make sure ssml_text is not empty
    if ssml_text is None:
        print('Error in ssml_to_audio. The input text does not exist.')
        return

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Sets the text input to be synthesized
    synthesis_input = texttospeech.types.SynthesisInput(ssml=ssml_text)

    # Builds the voice request, selects the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

    # Selects the type of audio file to return
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    # Performs the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    # Writes the synthetic audio to the output file.
    with open(outfile, 'wb') as out:
        out.write(response.audio_content)
        print('Audio content written to file ' + outfile)
    # [END audio]

# [START ssml]
def text_to_ssml(inputfile):
    # Generates SSML text from plaintext.

    # Given an input filename, this function converts the contents of the text
    # file into a string of formatted SSML text. This function formats the SSML
    # string so that, when synthesized, the synthetic audio will pause for two
    # seconds between each line of the text file. This function also handles
    # special text characters which might interfere with SSML commands.

    # Args:
        # inputfile: string name of plaintext file

    # Returns:
        # A string of SSML text based on plaintext input

    # Parse lines of input file
    try:
        open_file = open(inputfile, 'r')
        raw_lines = open_file.readlines()

    # Checks to make sure that the input file exists
    except IOError:
        print('Error in text_to_ssml. The file ' + inputfile + ' does not exist.')
        return

    # Define SSML timed break between addresses
    time = '"2s"'
    brk = '<break time=' + time + '/>'

    # Initialize SSML script
    ssml = '<speak>'

    # Iterate through lines of file
    for l in raw_lines:

        # Expand select special characters
        # Some special characters might interfere with the SSML interpreter
        l = l.replace('&', ' and ')
        l = l.replace('<', ' open carot ')
        l = l.replace('>', ' close carot ')

        # Concatenate the line to the SSML script
        ssml += l

        # Wait 2 seconds between speaking each address
        ssml += brk

    # Terminate the SSML script
    ssml += '</speak>'

    # Return the concatenated string of ssml script
    return ssml
# [END ssml]

# [START test]
if __name__ == '__main__':
    plaintext = 'example.txt'
    ssml_text = text_to_ssml(plaintext)
    ssml_to_audio(ssml_text, 'example.mp3')
    # [END test]
    