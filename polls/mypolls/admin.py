from django.contrib import admin
from mypolls.models import Question, Choice

# Register your models here.
admin.site.register(Question)
admin.site.register(Choice)


