from django.urls import path
from django.contrib.auth import views as auth_views
from .views import HomeView, AccountSettingsView, ProfileView, SearchView, RegisterUserView, LoginUserView, LogoutUserView, LiveChatView, ChatRoomView, FriendsView
from . import views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('like-post/', views.LikePostView.as_view(), name='like-post'),
    path('account_settings/', AccountSettingsView.as_view(), name='account_settings'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('search/', SearchView.as_view(), name='search'),

    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name="logout"),

    path('friend_request/<int:pk>/', FriendsView.friend_request, name='friend_request'),
    path('accept_friend_request/<int:pk>/', FriendsView.accept_friend_request, name='accept_friend_request'),
    path('delete_friend_request/<int:pk>/', FriendsView.delete_friend_request, name='delete_friend_request'),
    path('unfollow_friend/<int:pk>/', FriendsView.unfollow_friend, name='unfollow_friend'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='sna/password_reset.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='sna/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='sna/password_reset_form.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='sna/password_reset_done.html'), name='password_reset_complete'),

    path('livechat/', LiveChatView.as_view(), name='livechat'),
    path('livechat/<str:room>/', ChatRoomView.as_view(), name='chatroom'),
    path('send/', ChatRoomView.send, name='send'),
    path('getMessages/<str:room>/', ChatRoomView.getMessages, name='getMessages'),
]
