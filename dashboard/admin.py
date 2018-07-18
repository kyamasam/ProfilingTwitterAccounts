from django.contrib import admin

# Register your models here.

admin.site.site_header = 'Spider Admin'

from .models import Social_Accounts ,Watching_Accounts
admin.site.register(Watching_Accounts)
admin.site.register(Social_Accounts)


class MyModelAdmin(admin.ModelAdmin):
    class Media:
        # js = ('js/admin/my_own_admin.js',)
        css = {
             'all': ('css/admin/admin.css',)
        }