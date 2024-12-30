from pathlib import Path
import mimetypes


def log(message):
    print(message)


class AudioFileToTextFile:
    def __init__(self, **kwargs):
        pass

    def check_is_audio(self, audio_filepath: Path):
        guessed_type = mimetypes.guess_type(audio_filepath)
        guessed_type_str = guessed_type[0]

        return guessed_type_str.startswith("audio"), guessed_type_str

    def to_txt_file(self, audio_filepath: Path, text_filepath: Path, args, **kwargs):
        if not audio_filepath.exists():
            raise FileNotFoundError(audio_filepath)

        if not audio_filepath.is_file():
            raise ValueError(f"Given audio filepath is not a file : {audio_filepath}")

        is_video, guessed_type_str = self.check_is_audio(audio_filepath)
        if not is_video:
            raise ValueError(
                f"Given audio filepath : {audio_filepath} is not an audio file : {guessed_type_str}"
            )

        if text_filepath is None:
            text_filepath = audio_filepath.parent.joinpath(audio_filepath.stem + ".txt")

        log(f"Turning audio file {audio_filepath} into txt file {text_filepath}")
        return (
            self._to_txt_file(audio_filepath, text_filepath, args, **kwargs),
            text_filepath,
        )

    def _to_txt_file(self, audio_filepath: Path, text_filepath: Path, args, **kwargs):
        raise NotImplementedError("AudioFileToTextFile._to_txt_file")
