from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Book)
admin.site.register(ImageBook)
admin.site.register(Listing)
admin.site.register(ReportedBooks)