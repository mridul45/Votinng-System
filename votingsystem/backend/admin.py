from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Candidate)
admin.site.register(Voter)
admin.site.register(Results)
admin.site.register(Election)
admin.site.register(Voted)
admin.site.register(Shares)