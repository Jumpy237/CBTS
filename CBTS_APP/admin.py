from django.contrib import admin
from .models import Test, Question, Choice, Subject, Topic, Result, CompositeObjective
admin.site.register(Subject)
admin.site.register(Topic)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Result)
admin.site.register(CompositeObjective)
