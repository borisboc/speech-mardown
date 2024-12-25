from pathlib import Path
from audio_to_text import AudioFileToTextFile
from vosk.transcriber.transcriber import Transcriber
import copy
from types import SimpleNamespace


class VoskAudioFileToTextFile(AudioFileToTextFile):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass

    def _to_txt_file(self, audio_filepath: Path, text_filepath: Path, args, **kwargs):
        # vosk_args = copy.deepcopy(args)
        vosk_args = SimpleNamespace()
        vosk_args.input = str(audio_filepath.absolute())
        vosk_args.output = str(text_filepath.absolute())
        vosk_args.output_type = "txt"
        vosk_args.model = None
        vosk_args.model_name = args.speech_model_name
        vosk_args.lang = "fr-FR"
        vosk_args.server = None
        vosk_args.tasks = 10
        vosk_args.log_level = "INFO"

        transcriber = Transcriber(vosk_args)
        task_list = [(Path(vosk_args.input), Path(vosk_args.output))]

        transcriber.process_task_list(task_list)

        return 0
