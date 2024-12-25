from ffmpeg import (
    FFmpeg,
)  # requires python-ffmpeg. Check https://python-ffmpeg.readthedocs.io/en/stable/
from pathlib import Path
from video_to_audio import VideoFileToAudioFile


class FFmpegVideoFileToAudioFile(VideoFileToAudioFile):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass

    def _to_audio_file(self, video_filepath: Path, audio_filepath: Path, **kwargs):
        ffmpeg = (
            FFmpeg()
            .option("y")
            .input(str(video_filepath))
            .output(str(audio_filepath), vn=None, acodec="copy")
        )

        ffmpeg.execute()
        return 0
