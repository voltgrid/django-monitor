from rest_framework import viewsets

from .models import Result
from .serializers import ResultSerializer


class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer