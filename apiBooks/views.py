import os
from django.shortcuts import render
from django.http import Http404, JsonResponse


# fetch the root project and app path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# path languages
path_languages = os.path.join(BASE_DIR, 'data_new', 'languages')


def get_languages(request):
    languages = []
    for language in os.listdir(path_languages):
        books = os.listdir(os.path.join(path_languages, language))
        languages.append({"lang":language, "books": books})

    return JsonResponse({"languages" : languages})

def language_detector(request):
    return JsonResponse({"A":"1"})

def get_book(request):
    return JsonResponse({"A":"1"})
