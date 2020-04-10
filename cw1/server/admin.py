from django.contrib import admin
from .models import Professor, Module, Student, Rating

admin.site.register(Professor)
admin.site.register(Module)
admin.site.register(Student)
admin.site.register(Rating)
