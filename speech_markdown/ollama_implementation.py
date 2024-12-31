from string import Template
from ollama import chat
from ollama import ChatResponse
from surfacing_text_from_audio import SurfacingTextFromAudio
from tqdm import tqdm


class OllamaSurfacing(SurfacingTextFromAudio):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass

    def _surface_text(
        self,
        chunks: list[str],
        llm_model: str,
        system_message: str,
        user_template_message: Template,
        **kwargs
    ) -> str:

        full_answer = None

        for i, chunk in tqdm(enumerate(chunks)):

            user_message = user_template_message.substitute(
                {self.template_user_message: chunk}
            )
            response: ChatResponse = chat(
                model=llm_model,
                messages=[
                    {
                        "role": "system",
                        "content": system_message,
                    },
                    {
                        "role": "user",
                        "content": user_message,
                    },
                ],
            )

            if i == 0:
                full_answer = response.message.content
            else:
                full_answer += " " + response.message.content

        return full_answer
