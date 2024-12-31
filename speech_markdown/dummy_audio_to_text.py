from pathlib import Path
from audio_to_text import AudioFileToTextFile


class DummyAudioFileToTextFile(AudioFileToTextFile):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass

    def _to_txt_file(self, audio_filepath: Path, text_filepath: Path, args, **kwargs):
        return 0
