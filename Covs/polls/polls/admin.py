from django.contrib import admin
from .models import Poll,Candidate,Vote

# Register your models here.
admin.site.register((Poll,Candidate,Vote)) 