from openai import OpenAI
from pathlib import Path
import requests

class Generate:
    def __init__(self) -> None:
        self.client = OpenAI(
            api_key=""
        )

    def generate_story(self, tag_line):
        """
        Recives tag_line and generates the story using open ai models
        """
        response = self.client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=f"write a moral story for this tageline : {tag_line}",
            max_tokens=500,
            temperature=0.3,
        )

        #return response.choices[0].text
        import google.generativeai as genai

        genai.configure(api_key="")
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content('write a morale story : unity is strength')

        print(response.text)

    def generate_sound(self, input_paragraph):
        """
        Takes pragraph and generates the sound using openai models
        """
        speech_file_path = Path(__file__).parent / "speech.mp3"
        response = self.client.audio.speech.create(
            model="tts-1-hd", voice="alloy", input=f"{input_paragraph}"
        )
        response.stream_to_file(speech_file_path)
        return speech_file_path

    def get_image(self,tag_line):
        response = self.client.images.generate(
                    model="dall-e-3",
                    prompt=f"{tag_line}",
                    size="1024x1024",
                    quality="standard",
                    n=1,
                    )

        image_url = response.data[0].url
        response_image = requests.get(image_url)
        with open(f"{ Path(__file__).parent}/image.jpg", 'wb') as file:
            file.write(response_image.content)
        image_path = Path(__file__).parent / "image.jpg"
        return image_path

import pathlib
import textwrap

import google.generativeai as genai

genai.configure(api_key="")
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content('write a morale story : unity is strength')

print(response.text)
