from openai import OpenAI
from pathlib import Path
import requests


class Generate:
    def __init__(self) -> None:
        self.client = OpenAI(
            api_key="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"
        )

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

    def generate_sound(self, input_paragraph) -> Path:
        """
        Takes pragraph and generates the sound using openai models
        """
        speech_file_path: Path = Path(__file__).parent / "speech.mp3"
        response = self.client.audio.speech.create(
            model="tts-1-hd", voice="alloy", input=f"{input_paragraph}"
        )
        response.stream_to_file(speech_file_path)
        return speech_file_path

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


# Generate().generate_story("how a data is being transported , stored when i write on my notepad in linux ")

# def combined_response(audio_path, image_path):
#     # Read image data
#     with open(image_path, "rb") as image_file:
#         image_data = image_file.read()

#     # Read audio data
#     with open(audio_path, "rb") as audio_file:
#         audio_data = audio_file.read()

#     # Set content types
#     image_content_type = "image/jpeg"
#     audio_content_type = "audio/mp3"

#     # Set response headers
#     response = HttpResponse(content_type="multipart/mixed")
#     response["Content-Disposition"] = "inline; filename=combined_response"

#     # Add image data to the response
#     response.write(
#         f"--boundary\r\nContent-Type: {image_content_type}\r\n\r\n".encode())
#     response.write(image_data)
#     response.write(b"\r\n")

#     # Add audio data to the response
#     response.write(
#         f"--boundary\r\nContent-Type: {audio_content_type}\r\n\r\n".encode())
#     response.write(audio_data)
#     response.write(b"\r\n")

#     # Add boundary for the end of the response
#     response.write(b"--boundary--")

#     return response
