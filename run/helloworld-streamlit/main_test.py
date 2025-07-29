from streamlit.testing.v1 import AppTest

def test_balloons():
    """A user presses the balloons button"""
    at = AppTest.from_file("main.py").run()
    at.text_input[0].set_value("Foo").run()
    at.button[0].click().run()
    assert at.markdown.values[0] == "This is a demo Streamlit app.\n\nEnter your name in the text box below and press a button to see some fun features in Streamlit."
    assert at.markdown.values[1] == "Time to celebrate Foo! 🥳"
    assert at.markdown.values[2] == "You deployed a Streamlit app! 👏"

def test_snow():
    """A user presses the snow button"""
    at = AppTest.from_file("main.py").run()
    at.text_input[0].set_value("Foo").run()
    at.button[1].click().run()
    assert at.markdown.values[0] == "This is a demo Streamlit app.\n\nEnter your name in the text box below and press a button to see some fun features in Streamlit."
    assert at.markdown.values[1] == "Let it snow Foo! 🌨️"
    assert at.markdown.values[2] == "You deployed a Streamlit app! 👏"
    
