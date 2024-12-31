from pathlib import Path
from string import Template


def log(message):
    print(message)


class SurfacingTextFromAudio:
    def __init__(self, **kwargs):
        self.template_user_message = "USER_MESSAGE"
        return

    def surface_text(
        self,
        chunks: list[str],
        output_filepath: Path,
        llm_model: str,
        system_message: str,
        user_template_message: Template,
        **kwargs,
    ):
        if len(chunks) == 0:
            log("No chunks to process in SurfacingTextFromAudio.surface_text")
            return None

        if not output_filepath.parent.exists():
            output_filepath.parent.mkdir(parents=True, exist_ok=True)

        log(
            f"About to surface/rephrase {len(chunks)} chunks"
            + f"\nusing LLM model: {llm_model}"
            + f"\nwith system prompt:\n{system_message}"
            + f"\nand user prompt (templated):\n{user_template_message.template}"
        )

        ret = self._surface_text(
            chunks, llm_model, system_message, user_template_message, **kwargs
        )

        if ret is None:
            log(
                "WARNING : returned string from SurfacingTextFromAudio._surface_text is None"
            )
        else:
            with open(output_filepath, "w") as f:
                f.write(ret)

            log(f"Surfacing has been saved to file {output_filepath}")

        return ret

    def _surface_text(
        self,
        chunks: list[str],
        llm_model: str,
        system_message: str,
        user_template_message: str,
        **kwargs,
    ) -> str:
        raise NotImplementedError("SurfacingTextFromAudio._surface_text")
