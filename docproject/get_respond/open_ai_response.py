import json
import os
import uuid
from openai import OpenAI
from pathlib import Path
import requests


class Generate:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=self._load_api_key_from_json())

    def _load_api_key_from_json(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_directory, "cred_config.json")
        with open(file_path, "r") as file:
            config = json.load(file)
        return config.get("openai_api_key")

    def generate_story(self, tag_line) -> str:
        """
        Recives tag_line and generates the story using open ai models
        """
        response = self.client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=f"write a layman to technical explanation for : {tag_line}",
            max_tokens=500,
            temperature=0.3,
        )
        return response.choices[0].text

    def generate_sound(self, input_paragraph, tag_line) -> Path:
        """
        Takes pragraph and generates the sound using openai models
        """
        if not os.path.isdir("temp_audios"):
            os.mkdir("temp_audios")
        speech_file_path: Path = (
            Path(__file__).parents[1] / f"temp_audios/{tag_line}.mp3"
        )
        response = self.client.audio.speech.create(
            model="tts-1-hd", voice="alloy", input=f"{input_paragraph}"
        )
        response.stream_to_file(speech_file_path)
        return speech_file_path, f"{tag_line}.mp3"

    def get_image(self, tag_line) -> Path:
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=f"{tag_line}",
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url
        response_image = requests.get(image_url)
        with open(f"{Path(__file__).parent}/image.jpg", "wb") as file:
            file.write(response_image.content)
        image_path = Path(__file__).parent / "image.jpg"
        return image_path
