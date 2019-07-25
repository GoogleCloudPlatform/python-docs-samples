from hybrid_tutorial import pic_to_text
"""
from hybrid_tutorial import translate_text
from hybrid_tutorial import
"""

# VISION TESTS


def test_vision_standard_format():

    # Generate text
    text = pic_to_text("resources/standard_format.JPG")

    # Read expected text
    with open("resources/standard_format.txt") as f:
        expected_text = f.read()
    
    assert text == expected_text

def test_vision_non_standard_format():

    # Generate text
    text = pic_to_text("resources/non_standard_format.png")

    # Read expected text
    with open("resources/non_standard_format.txt") as f:
        expected_text = f.read()
    
    assert text == expected_text


"""
def test_vision_special_chars():

    # Generate text
    text = pic_to_text("resources/special_chars.jpg")

    # Read expected text
    with open("resources/standard_format.txt") as f:
        expected_text = f.read()
    
    assert text is expected_text
"""

# TRANSLATE TESTS


def test_translate():
    assert 0 is 0
    return

# TEXT-TO-SPEECH TESTS


def test_tts_special_chars():
    return

