import base64
from calendar import c
from multiprocessing.managers import BaseManager
from django.shortcuts import redirect, render

from .store_files import StoreGcp
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
from django.shortcuts import get_object_or_404

GCS = StoreGcp


def home(request) -> HttpResponse:
    return render(request=request, template_name="home.html")


@login_required
@csrf_exempt
def get_story(request) -> HttpResponse | None:
    if request.method == "POST":
        story_line = request.POST.get("prompt", b"")
        text_story = Generate().generate_story(story_line)
        audio_story, story_line = Generate().generate_sound(text_story, story_line)
        with open(audio_story, "rb") as audio_file:
            audio_data = base64.b64encode(audio_file.read()).decode("utf-8")
        GCS(source_file_name=story_line, file_type="audio").upload_data()
        story = Stories(user=request.user, topic=story_line)
        story.save()
        return render(request, "get_story.html", {"audio_data": audio_data})
    else:
        return render(request=request, template_name="get_story.html")


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
        return render(request=request, template_name="signup.html")


@csrf_exempt
def login(
    request,
) -> HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse:
    if request.method == "POST":
        user_name = request.POST.get("username")
        password = request.POST.get("password")

        user_authentication = auth.authenticate(
            request=request,
            username=user_name,
            password=password,
        )

        if user_authentication:
            auth.login(request, user_authentication)
            response = HttpResponse("User auth successful")
            response.set_cookie("logged_in", "True")
            return redirect("/my_stories")
        else:
            return HttpResponse("User auth failed")

    else:
        return render(request=request, template_name="login.html")


def logout(request) -> HttpResponse:
    auth.logout(request=request)
    return HttpResponse("You have been logged out.")


def my_stories(request) -> HttpResponse:
    user_stories: BaseManager[Stories] = Stories.objects.filter(user=request.user)
    # Stories.objects.filter(Q(topic__contains="civilization")&Q(user=request.user))
    story_topics = []
    for stories in user_stories:
        story_topics.append(stories)
    return render(
        request=request, template_name="stories.html", context={"stories": story_topics}
    )


@login_required
def story_url(request, story_id) -> HttpResponse:
    story = get_object_or_404(Stories, Q(user__id=request.user.id) & Q(id=story_id))
    story_path = GCS(source_file_name=story.topic, file_type="audio")
    print(story_path, story.topic)
    return render(
        request=request,
        template_name="story_url.html",
        context={"signed_url": story_path.get_signed_url()},
    )
