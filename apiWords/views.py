from rest_framework import viewsets

from apiWords.models import MandarinWord
from apiWords.serializers import MandarinWordSerializer


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
            print("LEEEN", len(queryset))
            if len(queryset) == 0:
                print("succeed find 0", simplified.split())
                queryset = MandarinWord.objects.all().filter(simplified__in=simplified)
                print(simplified, queryset)
                return queryset

        if pronunciation is not None:
            queryset = queryset.filter(pronunciation=pronunciation)

        return queryset