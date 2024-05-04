from django.contrib import admin
from .models import PersonalInfo, GalleryImage, Timeline, Question, QuizResult

admin.site.register(PersonalInfo)
admin.site.register(GalleryImage)
admin.site.register(Timeline)
admin.site.register(Question)
admin.site.register(QuizResult)
