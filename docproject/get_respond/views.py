from django.shortcuts import render
import json
import requests
from pathlib import Path
from .open_ai_response import Generate
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def get_story(request) -> HttpResponse | None:
    if request.method == "POST":
        binary_data = request.POST.get("story_for", b"")
        text_story = Generate().generate_story(binary_data)
        audio_story = Generate().generate_sound(text_story)
        with open(audio_story, 'rb') as audio_file:
            audio_data = audio_file.read()
        content_type = 'audio/mp3'
        response = HttpResponse(audio_data, content_type=content_type)
        return response


def combined_response(audio_path, image_path):
    # Read image data
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    # Read audio data
    with open(audio_path, "rb") as audio_file:
        audio_data = audio_file.read()

    # Set content types
    image_content_type = "image/jpeg"
    audio_content_type = "audio/mp3"

    # Set response headers
    response = HttpResponse(content_type="multipart/mixed")
    response["Content-Disposition"] = "inline; filename=combined_response"

    # Add image data to the response
    response.write(
        f"--boundary\r\nContent-Type: {image_content_type}\r\n\r\n".encode())
    response.write(image_data)
    response.write(b"\r\n")

    # Add audio data to the response
    response.write(
        f"--boundary\r\nContent-Type: {audio_content_type}\r\n\r\n".encode())
    response.write(audio_data)
    response.write(b"\r\n")

    # Add boundary for the end of the response
    response.write(b"--boundary--")

    return response
