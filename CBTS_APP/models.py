from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    teacher = models.CharField(max_length=100, default="teachername")

    def __str__(self):
      return self.title
      
class Topic(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
      return self.title

class Test(models.Model):
    
    title = models.CharField(max_length=100)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    time_limit = models.IntegerField(default=60)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    

    


#storing result

class Result(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    score = models.IntegerField()

class CompositeObjective(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    topic1 = models.ForeignKey(Topic, related_name='topic1', on_delete=models.CASCADE)
    topic2 = models.ForeignKey(Topic, related_name='topic2', on_delete=models.CASCADE)
    cnt = models.PositiveIntegerField(default=0)

    def __str__(self):
        if self.topic1.title == self.topic2.title:
            return self.topic1.title
        return self.topic1.title + ' ' + self.topic2.title

class Question(models.Model):

    title = models.TextField(max_length=500)
    difficulty = models.IntegerField(validators=[MaxValueValidator(3), MinValueValidator(1)])
    topic = models.ForeignKey(CompositeObjective, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

class Choice(models.Model):
    choice = models.CharField(max_length=20)
    point = models.FloatField(default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)