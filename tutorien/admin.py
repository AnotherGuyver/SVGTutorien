from django.contrib import admin
from tutorien.models import TutDate, Tut, Attendance, TutUser, TutorSuggestion

admin.site.register(TutDate)
admin.site.register(TutUser)
admin.site.register(Tut)
admin.site.register(Attendance)
admin.site.register(TutorSuggestion)