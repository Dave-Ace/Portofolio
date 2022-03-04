from django.contrib import admin
from User.models import Message, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.
class ChatAdmin(admin.ModelAdmin):
    model = Message
    readonly_fields =('author', 'content', 'timestamp')

class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        ('None', {
            'fields': ('username', 'first_name', 'last_name', 'email', 'About', 'Hobbies','Nationality', 'image', 'password1', 'password2')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active')
        })
    )
    fieldsets = (
        ('Profile', {
            'fields': ('username', 'first_name', 'last_name', 'email', 'About', 'Hobbies', 'Nationality', 'image', 'password')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active')
        })
    )

    list_display=['username','first_name', 'last_name', 'email', 'Nationality']
    ordering =('username',)

    def get_queryset(self, request):
        
        if request.user.is_superuser == True:
            user = self.model.objects.all()
        else:
            user = self.model.objects.filter(username=request.user.username)
        return user


admin.site.register(Message, ChatAdmin)
admin.site.register(User, UserAdmin)