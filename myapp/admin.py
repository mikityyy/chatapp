from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Message
from .forms import SignUpForm

class CustomUserAdmin(UserAdmin):
    add_form = SignUpForm
    model = CustomUser
    list_display = ('username', 'email', 'thumbnail', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email','thumbnail')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email',)
    ordering = ('username',)

    def thumbnail_tag(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" style="width: 75px; height: 75px;" />'.format(obj.thumbnail.url))
        else:
            return '-'

    thumbnail_tag.short_description = 'Thumbnail'

admin.site.register(CustomUser, CustomUserAdmin)





admin.site.register(Message)
