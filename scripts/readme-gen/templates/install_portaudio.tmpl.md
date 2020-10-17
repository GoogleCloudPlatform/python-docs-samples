Install PortAudio
=================

Install [PortAudio](http://www.portaudio.com/). This is required by the
[PyAudio](https://people.csail.mit.edu/hubert/pyaudio/) library to
stream audio from your computer\'s microphone. PyAudio depends on
PortAudio for cross-platform compatibility, and is installed differently
depending on the platform.

-   For Mac OS X, you can use [Homebrew](http://brew.sh):

        brew install portaudio

    **Note**: if you encounter an error when running [pip
    install]{.title-ref} that indicates it can\'t find
    [portaudio.h]{.title-ref}, try running [pip install]{.title-ref}
    with the following flags:

        pip install --global-option='build_ext' \
            --global-option='-I/usr/local/include' \
            --global-option='-L/usr/local/lib' \
            pyaudio

-   For Debian / Ubuntu Linux:

        apt-get install portaudio19-dev python-all-dev

-   Windows may work without having to install PortAudio explicitly (it
    will get installed with PyAudio).

For more details, see the [PyAudio
installation](https://people.csail.mit.edu/hubert/pyaudio/#downloads)
page.
