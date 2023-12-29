from multiprocessing.managers import BaseManager
from django.shortcuts import redirect
from .open_ai_response import Generate
from django.http import (
    HttpResponse,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import Stories
from django.db.models import Q


@login_required
@csrf_exempt
def get_story(request) -> HttpResponse | None:
    if request.method == "POST":
        binary_data = request.POST.get("story_for", b"")
        text_story = Generate().generate_story(binary_data)
        audio_story = Generate().generate_sound(text_story)
        with open(audio_story, "rb") as audio_file:
            audio_data = audio_file.read()
        content_type = "audio/mp3"
        response = HttpResponse(audio_data, content_type=content_type)
        story = Stories(user=request.user, topic=binary_data, path=audio_story)
        story.save()
        return response


@csrf_exempt
def register(request) -> HttpResponse | None:
    if request.method == "POST":
        user_name = request.POST.get("user_name")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        email = request.POST.get("email")
        if confirm_password == password:
            if User.objects.filter(email=email).exists():
                return HttpResponse("Email already exisits")
            elif User.objects.filter(username=user_name).exists():
                return HttpResponse("Username already taken")
            else:
                user_obj = User.objects.create_user(
                    username=user_name, email=email, password=password
                )
                user_obj.save()
                return HttpResponse("user created successfully")
        else:
            return HttpResponse("Password Doesnot match")
    else:
        return HttpResponse("Nothing please sit tight")


@csrf_exempt
def login(
    request,
) -> HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse:
    user_authentication = auth.authenticate(
        request=request,
        username=request.POST.get("user_name"),
        password=request.POST.get("password"),
    )
    if user_authentication:
        auth.login(request, user_authentication)  # Log the user in.
        response = HttpResponse("User auth successful")
        # Set a cookie on the response
        response.set_cookie("logged_in", "True")
        return redirect("/my_stories")
    else:
        return HttpResponse("User auth failed")


def logout(request) -> HttpResponse:
    auth.logout(request=request)
    return HttpResponse("You have been logged out.")


def my_stories(request) -> HttpResponse:
    user_stories: BaseManager[Stories] = Stories.objects.filter(user=request.user)
    # Stories.objects.filter(Q(topic__contains="civilization")&Q(user=request.user))
    story_topics = []
    for stories in user_stories:
        story_topics.append(stories.topic)
    return HttpResponse(story_topics)
