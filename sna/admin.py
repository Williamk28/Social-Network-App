from django.contrib import admin
from .models import CustomUser, UserPost, ChatRoom, LiveChatMessage, LikePost, CommentPost, FriendRequest

# Register your models here.


admin.site.register(CustomUser)
admin.site.register(UserPost)
admin.site.register(LikePost)
admin.site.register(CommentPost)
admin.site.register(ChatRoom)
admin.site.register(LiveChatMessage)
admin.site.register(FriendRequest)
