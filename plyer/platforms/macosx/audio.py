from plyer.facades import Audio
from pyobjus.dylib_manager import load_framework, INCLUDE
from pyobjus import autoclass
from os.path import join, expanduser

load_framework(INCLUDE.Foundation)
load_framework(INCLUDE.AVFoundation)

AVAudioPlayer = autoclass("AVAudioPlayer")
AVAudioRecorder = autoclass("AVAudioRecorder")
AVAudioFormat = autoclass("AVAudioFormat")
NSString = autoclass('NSString')
NSURL = autoclass('NSURL')

class OSXAudio(Audio):
    def __init__(self, file_path=None):
        default_path = join(expanduser('~'), 'Desktop', 'audio.wav')
        super(OSXAudio, self).__init__(file_path or default_path)

        self._recorder = None
        self._player = None
        self._current_file = None

    def _start(self):
        # Conversion of Python file path string to Objective-C NSString
        file_path_NSString = NSString.alloc()
        file_path_NSString = file_path_NSString.initWithUTF8String_(
            self._file_path
        )

        # Definition of Objective-C NSURL object for the output record file
        # specified by NSString file path
        file_NSURL = NSURL.alloc()
        file_NSURL = file_NSURL.initWithString_(file_path_NSString)

        # Internal audio file format specification
        af = AVAudioFormat.alloc()
        af = af.initWithCommonFormat_sampleRate_channels_interleaved_(
            1, 44100.0, 2, True
        )

        # Audio recorder instance initialization with specified file NSURL
        # and audio file format
        self._recorder = AVAudioRecorder.alloc()
        self._recorder = self._recorder.initWithURL_format_error_(
            file_NSURL, af, None
        )
        
        if self._recorder:
            self._recorder.record()
            print("Recording...")

            # Setting the currently recorded file as current file
            # for using it as a parameter in audio player
            self._current_file = file_NSURL

    def _stop(self):
        if self._recorder:
            self._recorder.stop()
            print("Stopped recording.")
            self._recorder = None

        if self._player:
            self._player.stop()
            print("Stopped playing.")
            self._player = None

    def _play(self):
        # Audio player instance initialization with the file NSURL
        # of the last recorded audio file
        self._player = AVAudioPlayer.alloc()
        self._player = self._player.initWithContentsOfURL_error_(
            self._current_file, None
        )

        if self._player:
            self._player.play()
            print("Playing the last recorded audio file...")

def instance():
    return OSXAudio()
