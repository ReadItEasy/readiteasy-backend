import os
from django.shortcuts import render
from django.http import Http404, JsonResponse
from utils.chinese_utils import make_chapter_from_chinese_book, chinese_tokenize, make_statistics_from_chinese_book
import time

from utils.path_utils import PathHandler

# fetch the root project and app path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

paths = PathHandler(BASE_DIR)
# path languages
path_languages = os.path.join(BASE_DIR, 'data', 'languages')

# path user known words
# path_users_known_words = os.path.join(BASE_DIR, 'data', 'users')


def get_languages(request):
    languages = []
    for language in os.listdir(paths.languages()):
        books = os.listdir(paths.books(language))
        languages.append({"lang":language, "books": books})
        print(languages)

    return JsonResponse({"languages" : languages})

def language_detector(request):
    return JsonResponse({"A":"1"})

def get_book_chapter(request):
    t1 = time.time()
    target_language = request.GET.get("targetLanguage")
    book_name = request.GET.get("bookName")
    chapter_number = request.GET.get("chapterNumber")

    path_book_folder = paths.book(target_language, book_name)
    # path_raw = os.path.join(path_book_folder, 'raw', book_name)
    # path_statistics = os.path.join(path_book_folder, 'statistics')
    path_book_chapters = os.path.join(path_book_folder, "chapters")

    make_chapter_from_chinese_book(path_book_folder, book_name)
    make_statistics_from_chinese_book(path_book_folder, book_name)

    path_book_chapter = os.path.join(path_book_chapters, "{}.txt".format(chapter_number))
    with open(path_book_chapter, "r", encoding="utf-8") as infile:
        chapter_text = infile.read()

    tokenized_chapter_text = list(chinese_tokenize(chapter_text))
    print(len(tokenized_chapter_text))
    json = {
        "tokenized_chapter_text": tokenized_chapter_text,
    }
    print("time to api call : {}".format(time.time()-t1))
    return JsonResponse(json)


#
# def get_user_known_words(request):
#     t1 = time.time()
#     user_id = request.GET.get("userId", "default")
#     target_language = request.GET.get("targetLanguage", "error")
#
#     path_user_known_words = os.path.join(path_users_known_words, user_id, "{}_known_words.txt".format(target_language))
#     user_known_words_dict = {}
#     with open(path_user_known_words, 'r', encoding="utf-8") as infile:
#         for line in infile:
#             word = line.rstrip('\n')
#             user_known_words_dict[word] = True
#
#     json = {"user_known_words_dict": user_known_words_dict}
#     print("time to user known words call : {}".format(time.time()-t1))
#
#     return JsonResponse(json)




