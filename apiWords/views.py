import os

from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from apiWords.models import MandarinWord
from apiWords.serializers import MandarinWordSerializer

from utils.path_utils import PathHandler

# fetch the root project and app path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
paths = PathHandler(BASE_DIR)


class MandarinWordSet(viewsets.ModelViewSet):
    queryset = MandarinWord.objects.all()
    serializer_class = MandarinWordSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = MandarinWord.objects.all()
        print("self.request.query_params", {**self.request.query_params})
        simplified = self.request.query_params.get('simplified', None)
        pronunciation = self.request.query_params.get('pronunciation', None)
        if simplified is not None:
            queryset = queryset.filter(simplified=simplified)
            if len(queryset) == 0:
                print("succeed find 0", simplified.split())
                queryset = MandarinWord.objects.all().filter(simplified__in=simplified)
                print(simplified, queryset)
                return queryset

        if pronunciation is not None:
            queryset = queryset.filter(pronunciation=pronunciation)

        return queryset

    @action(detail=False, methods=['GET'], name='Get word statistics')
    def word_statistics(self, request):
        """Does something on single item."""
        queryset = MandarinWord.objects.all()
        serializer = self.get_serializer(queryset,
                                         many=False)
        print("self.request", self.request.query_params)
        word = self.request.query_params.get("word")
        print({**self.request.query_params})

        with open(paths.corpus_statistics("mandarin"), 'r', encoding="utf-8") as infile:
            first_line = infile.readline()
            rank, freq, n_tokens = 0., 0., 0.
            if "tokens" in first_line:
                n_tokens = float((first_line.rstrip("\n").split("\t")[1]))
            for line in infile:
                char, rank, freq = line.rstrip("\n").split("\t")
                if char == word:
                    rank, freq = int(rank), float(freq)
                    print("FOUNDED !!!", int(rank), float(freq), n_tokens)
                    break

        json = {
            "word": word,
            "rank": rank,
            "freq": freq,
            "n_tokens": n_tokens,
                }
        print(json)
        return JsonResponse(json)
