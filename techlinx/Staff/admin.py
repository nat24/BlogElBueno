from django.contrib import admin
from .models import Staff
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.

class StaffAdmin(SummernoteModelAdmin):
    exclude = ('slug', )
    summer_note_fields = ('biografia',)

admin.site.register(Staff,StaffAdmin)
