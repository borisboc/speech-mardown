import argparse
from pathlib import Path
import mimetypes
from ffmpeg_implementation import FFmpegVideoFileToAudioFile
from vosk_implementation import VoskAudioFileToTextFile
from split_text import split_text_file_to_chuncks


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
    parser.add_argument(
        "--speech-model-name",
        "-sn",
        type=str,
        default="vosk-model-fr-0.22",
        required=False,
        help="Speech (audio to text) model name. See VOSK documentation. Default is vosk-model-fr-0.22",
    )
    parser.add_argument(
        "--chunck-size",
        type=int,
        default=1000,
        required=False,
        help="Size of chuncks of characters (from audio) to pass to LLM for rephrasing / surfacing. Default is 1000.",
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
    audio_to_txt = VoskAudioFileToTextFile()
    ret, txt_filepath = audio_to_txt.to_txt_file(audio_filepath, None, args)

    if ret != 0:
        raise Exception(f"to_txt_file returned non null code : {ret}")

    chunks = split_text_file_to_chuncks(
        Path(txt_filepath), separator="\n", chunck_size=args.chunck_size
    )

    log(
        f"{len(chunks)} chunks with max size {args.chunck_size} will be rephrased / surfaced by LLM"
    )

    log("TODO (LLM)")


if __name__ == "__main__":
    main()
