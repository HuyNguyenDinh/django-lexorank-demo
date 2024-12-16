from django_lexorank.models import RankedModel
from django.db import models


class Board(RankedModel):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name


class Task(RankedModel):
    name = models.CharField(max_length=255)
    board = models.ForeignKey("Board", on_delete=models.CASCADE, related_name="tasks")
    order_with_respect_to = ["board"]

    def __str__(self):
        return self.name
