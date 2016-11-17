Install PortAudio
+++++++++++++++++

Install `PortAudio`_. This is required by the `PyAudio`_ library to stream
audio from your computer's microphone. PyAudio depends on PortAudio for cross-platform compatibility, and is installed differently depending on the
platform.

For Mac OS X, you can use `Homebrew`_::

    brew install portaudio

For Debian / Ubuntu Linux::

    apt-get install portaudio19-dev python-all-dev

Windows may work without having to install PortAudio explicitly (it will get
installed with PyAudio).

For more details, see the `PyAudio installation`_ page.


.. _PyAudio: https://people.csail.mit.edu/hubert/pyaudio/
.. _PortAudio: http://www.portaudio.com/
.. _PyAudio installation:
  https://people.csail.mit.edu/hubert/pyaudio/#downloads
.. _Homebrew: http://brew.sh
