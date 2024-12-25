from pathlib import Path
import mimetypes


def log(message):
    print(message)


class VideoFileToAudioFile:
    def __init__(self, **kwargs):
        pass

    def check_is_video(self, video_filepath: Path):
        guessed_type = mimetypes.guess_type(video_filepath)
        guessed_type_str = guessed_type[0]

        return guessed_type_str.startswith("video"), guessed_type_str

    def to_audio_file(self, video_filepath: Path, audio_filepath: Path, **kwargs):
        if not video_filepath.exists():
            raise FileNotFoundError(video_filepath)

        if not video_filepath.is_file():
            raise ValueError(f"Given video filepath is not a file : {video_filepath}")

        is_video, guessed_type_str = self.check_is_video(video_filepath)
        if not is_video:
            raise ValueError(
                f"Given video filepath : {video_filepath} is not a video file : {guessed_type_str}"
            )

        if audio_filepath is None:
            audio_filepath = video_filepath.parent.joinpath(
                video_filepath.stem + ".aac"
            )

        log(f"Turning video file {video_filepath} into audio file {audio_filepath}")
        return (
            self._to_audio_file(video_filepath, audio_filepath, **kwargs),
            audio_filepath,
        )

    def _to_audio_file(self, video_filepath: Path, audio_filepath: Path, **kwargs):
        raise NotImplementedError("VideoFileToAudioFile._to_audio_file")
