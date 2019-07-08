from tts import text_to_ssml
from tts import ssml_to_audio

import filecmp
import os
import sys


def test_text_to_ssml():
# Tests text_to_ssml() function
# Args: none
# Returns: array of 2 ssml strings

    # Array to hold strings of ssml
	ssml = []

	# Assert non-special characters converted to SSML
	input_chars = 'normal_chars.txt'
	tested_chars = text_to_ssml(input_chars)
	expected_chars = '<speak>This is a normal test.\n<break time="2s"/>Hopefully it passes!\n<break time="2s"/>:)<break time="2s"/></speak>'
	assert tested_chars == expected_chars

	# Add SSML to array
	ssml.append(tested_chars)

	# Assert special characters converted to SSML
	input_special_chars = 'special_chars.txt'
	tested_special_chars = text_to_ssml('special_chars.txt')
	expected_special_chars = '<speak> open carot  and  close carot \n<break time="2s"/> close carot  close carot \n<break time="2s"/> and <break time="2s"/></speak>'
	assert tested_special_chars == expected_special_chars

	# Add SSML to array
	ssml.append(tested_special_chars)

	# Assert that nothing returned if given nonexistent input
	non_existent_input = text_to_ssml('mysterfile.txt')
	assert non_existent_input == None

	return ssml


def test_ssml_to_audio(ssml):
# Tests ssml_to_audio() function
# Args: ssml = array of 2 ssml strings
# Returns: none

	# Assert audio file of non-special characters generated
	ssml_to_audio(ssml[0], 'out1.mp3')
	assert os.path.isfile('out1.mp3')

	# Assert audio file of non-special characters generated correctly
	assert filecmp.cmp('out1.mp3', 'expected_non_special_audio.mp3', shallow=True)

	# Assert audio file of special characters generated
	ssml_to_audio(ssml[1], 'out2.mp3')
	assert os.path.isfile('out2.mp3')

	# Assert audio file of special characters generated correctly
	assert filecmp.cmp('out2.mp3', 'expected_special_audio.mp3', shallow=True)

	# Assert that no mp3 file generated if given empty SSML input
	# NOTE to work correctly, directory must not already contain a file named 'out3.mp3'
	ssml_to_audio(None, 'out3.mp3')
	assert os.path.isfile('out3.mp3') == False


def suppressPrint():
# Suppresses printing; helper function
# Args: none
# Returns: none

    sys.stdout = open(os.devnull, 'w')


def enablePrint():
# Enables printing; helper function
# Args: None
# Returns: None

    sys.stdout = sys.__stdout__


if __name__ == '__main__':

    # Suppress printing while testing
    suppressPrint()

    ssml = test_text_to_ssml()
    test_ssml_to_audio(ssml)

    # Restores printing
    enablePrint()

    # Print success if achieved
    print("All tests passed!")