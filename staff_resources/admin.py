from django.contrib import admin

# Register your models here.

class AnnouncementAdminn(admin.ModelAdmin):
      exclude = ('short_school',)