import os
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework.decorators import action

from apiUsers.models import User
from apiUsers.serializers import UserSerializer
from apiUsers.permissions import IsLoggedInUserOrAdmin, IsAdminUser
from utils.path_utils import PathHandler
from utils.chinese_utils import read_freqs_dict, word_statistics_in_file



# fetch the root project and app path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
paths = PathHandler(BASE_DIR)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


    # Add this code block
    # def get_permissions(self):
    #     permission_classes = []
    #     if self.action == 'create':
    #         permission_classes = [AllowAny]
    #     elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
    #         permission_classes = [IsLoggedInUserOrAdmin]
    #     elif self.action == 'list' or self.action == 'destroy':
    #         permission_classes = [IsAdminUser]
    #     return [permission() for permission in permission_classes]

    @action(detail=True, methods=['POST'], name='Add a word to your known list')
    def add_word(self, request, pk=None):
        """Does something on single item."""
        queryset = User.objects.get(pk=pk)
        serializer = self.get_serializer(queryset,
                                         many=False)
        word = request.data.get("word")
        list_ = request.data.get("list")
        target_language = request.data.get('targetLanguage', None)
        mandarin_known_words_field = getattr(queryset.profile, f'{target_language}_{list_}_words')
        # mandarin_known_words_field = queryset.profile.mandarin_known_words.replace('\r','')
        if word:
            mandarin_known_words_list = mandarin_known_words_field.split("\n")
            if word not in mandarin_known_words_list:
                mandarin_known_words_list.append(word)
                mandarin_known_words_field = "\n".join(mandarin_known_words_list)
                profile = {
                    f"{target_language}_{list_}_words": mandarin_known_words_field
                }

                data = {
                    "profile": profile
                }
                serializer = self.get_serializer(queryset,
                                                 data=data,
                                                 partial=True,
                                                 many=False)
                if serializer.is_valid():
                    serializer.save()
                    message = "'{}' was correctly processed (added)".format(word)
                else:
                    message = "serializer not valid"

            else:
                message = "the word {} was already found in the known_words list".format(word)

        else:
            message = "no word was found in the post request"
        json = {"message": message}
        return JsonResponse(json)

    @action(detail=True, methods=['POST'], name='Remove a word from your known list')
    def remove_word(self, request, pk=None):
        """Does something on single item."""
        queryset = User.objects.get(pk=pk)
        serializer = self.get_serializer(queryset,
                                         many=False)
        word = request.data.get("word")
        list_ = request.data.get("list")
        target_language = request.data.get('targetLanguage', None)
        mandarin_known_words_field = getattr(queryset.profile, f'{target_language}_{list_}_words')

        if word:
            mandarin_known_words_list = mandarin_known_words_field.split("\n")
            if word in mandarin_known_words_list:
                mandarin_known_words_list.remove(word)
                mandarin_known_words_field = "\n".join(mandarin_known_words_list)
                profile = {
                    f"{target_language}_{list_}_words" : mandarin_known_words_field
                }

                data = {
                    "profile": profile
                }
                serializer = self.get_serializer(queryset,
                                                 data=data,
                                                 partial = True,
                                                 many=False)
                if serializer.is_valid():
                    serializer.save()
                    message = "'{}' was correctly processed (removed)".format(word)
                else:
                    message = "serializer not valid"

            else:
                message = "the word {} was not found in the known_words list".format(word)

        else:
            message = "no word was found in the post request"
        json = {"message": message}
        return JsonResponse(json)


    @action(detail=True, methods=['GET'], name='Get the known words for a book')
    def book_known_words(self, request, pk=None):
        print(request.user)
        """Does something on single item."""
        queryset = User.objects.get(pk=pk)
        serializer = self.get_serializer(queryset,
                                         many=False)
        mandarin_known_words_field = queryset.profile.mandarin_known_words.replace('\r','')
        mandarin_known_words_list = mandarin_known_words_field.split('\n')
        book_name = request.query_params.get('bookName', None)
        target_language = request.query_params.get('targetLanguage', None)

        path_book_statistics = paths.book_statistics(target_language, book_name)
        book_freqs, n_book_tokens, n_book_types, book_char_95percentile = read_freqs_dict(path_book_statistics)

        book_rank_95percentile, _, _, _ = word_statistics_in_file(book_char_95percentile,
                                                              paths.corpus_statistics(target_language))

        n_user_tokens = 0
        n_user_types = 0
        for known_word in mandarin_known_words_list:
            n_user_tokens += book_freqs.get(known_word, 0)
            if known_word in book_freqs:
                n_user_types += 1

        json = {
          "n_user_tokens": n_user_tokens,
          "n_user_types" : n_user_types,
          "n_book_tokens": n_book_tokens,
          "n_book_types": n_book_types,
          "book_char_95percentile": book_char_95percentile,
          "book_rank_95percentile": book_rank_95percentile
        }
        return JsonResponse(json)



class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        print(request.headers)
        content = {'message': 'Hello, World!'}
        return Response(content)
