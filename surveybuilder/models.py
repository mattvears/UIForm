from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UIForm(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    owner = models.ForeignKey(User)

class Question(models.Model):
    form = models.ForeignKey(UIForm)
    datatype = models.SmallIntegerField()
    text = models.TextField()

class Answer(models.Model):
    form = models.ForeignKey(UIForm)
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User)
    value = models.CharField(max_length=200)
