from django.contrib import admin

# Register your models here.
from .models import *

# Register your models here.
admin.site.register(Blog)
admin.site.register(Contact)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Comment)