import argparse
from pathlib import Path
import mimetypes
from ffmpeg_implementation import FFmpegVideoFileToAudioFile


def parse_args():
    parser = argparse.ArgumentParser(
        description="Get the speech from audio (or video), and turn this into markdown. Mainly designed for serious / educational purposes"
    )
    parser.add_argument("filepath", type=Path, help="Path to you video or audio file")
    parser.add_argument(
        "--o",
        type=Path,
        default=None,
        required=False,
        help="Path to the output markdown file",
    )

    args = parser.parse_args()
    return args


def log(message):
    print(message)


def main():
    args = parse_args()

    filepath = Path(args.filepath)

    if not filepath.exists():
        raise FileNotFoundError(filepath)

    if not filepath.is_file():
        raise ValueError(f"Given filepath is not a file : {filepath}")

    filename_no_ext = filepath.stem

    guessed_type = mimetypes.guess_type(filepath)
    guessed_type_str = guessed_type[0]

    if guessed_type_str.startswith("video"):
        video_to_audio = FFmpegVideoFileToAudioFile()
        ret, audio_filepath = video_to_audio.to_audio_file(filepath, None)
        if ret != 0:
            raise Exception(f"video_to_audio returned non null code : {ret}")
    elif guessed_type_str.startswith("audio"):
        audio_filepath = filepath
    else:
        raise NotImplementedError(
            f"File type not implemented : {guessed_type_str} for file {filepath}"
        )

    log(f"Processing audio file {audio_filepath}")


if __name__ == "__main__":
    main()
