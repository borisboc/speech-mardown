import argparse
from pathlib import Path
import mimetypes
from ffmpeg_implementation import FFmpegVideoFileToAudioFile
from vosk_implementation import VoskAudioFileToTextFile
from dummy_audio_to_text import DummyAudioFileToTextFile
from split_text import split_text_file_to_chunks
from ollama_implementation import OllamaSurfacing
from string import Template


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
        help="Path to the output text file",
    )
    parser.add_argument(
        "--lang-settings",
        "-ls",
        type=str,
        default=None,
        required=False,
        help="If Fr or En, it will overwrite speech-model-name, system-message, user-message-template values with default models and files appropriate for provided language (i.e. French or English). Default is None : in this case, it does not overwrite the above mentioned arguments.",
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
        "--chunk-size",
        type=int,
        default=1000,
        required=False,
        help="Size of chunks of characters (from audio) to pass to LLM for rephrasing / surfacing. Default is 1000.",
    )
    parser.add_argument(
        "--llm-model",
        type=str,
        default="llama3.2:3b-instruct-fp16",
        required=False,
        help="LLM model to use for surfacing / rephrasing (post audio to text).",
    )
    parser.add_argument(
        "--system-message",
        type=Path,
        default=Path(__file__).parent.joinpath("prompts/system_message_Fr.txt"),
        required=False,
        help="Path to the text file containing the system message (prompt) for surfacing with LLM.",
    )
    parser.add_argument(
        "--user-message-template",
        type=Path,
        default=Path(__file__).parent.joinpath("prompts/user_message_template_Fr.txt"),
        required=False,
        help="Path to the text file containing the user system message (prompt) templated (e.g. with $USER_MESSAGE) for surfacing with LLM.",
    )

    args = parser.parse_args()
    return args


def log(message):
    print(message)


def main(args):

    if args.lang_settings is not None:
        lang_settings = args.lang_settings.lower()
        if lang_settings == "fr":
            args.speech_model_name = "vosk-model-fr-0.22"
            args.system_message = Path(__file__).parent.joinpath(
                "prompts/system_message_Fr.txt"
            )
            args.user_message_template = Path(__file__).parent.joinpath(
                "prompts/user_message_template_Fr.txt"
            )
        elif lang_settings == "en":
            args.speech_model_name = "vosk-model-en-us-0.22"
            args.system_message = Path(__file__).parent.joinpath(
                "prompts/system_message_En.txt"
            )
            args.user_message_template = Path(__file__).parent.joinpath(
                "prompts/user_message_template_En.txt"
            )
        else:
            raise NotImplementedError(
                f"Language {args.lang_settings} is not implemented"
            )

        d = {
            "speech-model-name": args.speech_model_name,
            "system-message": args.system_message,
            "user-message-template": args.user_message_template,
        }
        log(
            f"Thanks to provided lang-settings : {args.lang_settings}, the following values have been modified : {d}\nPlease remove lang-settings argument if you don t want these values to be overwritten!"
        )

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
    # audio_to_txt = DummyAudioFileToTextFile()
    ret, txt_filepath = audio_to_txt.to_txt_file(audio_filepath, args.o, args)

    if ret != 0:
        raise Exception(f"to_txt_file returned non null code : {ret}")

    chunks = split_text_file_to_chunks(
        Path(txt_filepath), separator="\n", chunk_size=args.chunk_size
    )

    log(
        f"{len(chunks)} chunks with max size {args.chunk_size} will be rephrased / surfaced by LLM"
    )

    surfaced_filepath = txt_filepath.parent.joinpath(
        txt_filepath.stem + "_surfaced.txt"
    )

    surfacing = OllamaSurfacing()

    if not args.system_message.exists():
        log(
            f"WARNING : using default LLM system message because cannot find file {args.system_message}"
        )
        system_message = "Tu es une intelligence artificielle assistante, experte en relecture et correction orthographique de document."
    else:
        with open(args.system_message, "r") as f:
            system_message = str(f.read())

    if not args.user_message_template.exists():
        log(
            f"WARNING : using default LLM user message templated because cannot find file {args.user_message_template}"
        )
        user_template_message = Template(
            "Agis comme étant un simple programme informatique de traitement de texte."
            + " Voici mes demandes : tu vas corriger le texte ci dessous en essayant de rester le plus proche possible de celui-ci."
            + " Tu dois évidemment conserver la langue d'origine du texte : le français."
            + " Tu rajouteras la ponctuation (virgule et point) et les majuscules (pour le début des nouvelles phrase)."
            + " Tu corrigeras les fautes d'orthographe et de conjugaison."
            + " Tu corrigeras les erreurs de vocabulaire qui sont évidentes et indéniables. En cas de doute, tu laisseras le mot d'origine dans le texte."
            + " Tu ne changeras pas le contenu (hormis les fautes, la ponctuation, les majuscules et les erreurs indéniables sur le vocabulaire)."
            + " Tu ne supprimeras pas de contenu, même s'il semble inutile."
            + " Retourne uniquement le texte corrigé."
            + " Le résultat final sera sous la forme de markdown."
            + " Voici le texte à modifier :\n"
            + f"${surfacing.template_user_message}"
        )
    else:
        with open(args.user_message_template, "r") as f:
            user_template_message = Template(f.read())

    ret = surfacing.surface_text(
        chunks,
        surfaced_filepath,
        args.llm_model,
        system_message,
        user_template_message,
    )


if __name__ == "__main__":
    args = parse_args()
    main(args)
