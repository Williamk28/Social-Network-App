import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from itertools import chain
from .forms import CreateUserForm, CreatePostForm, AccountSettingForm, CreateCommentForm
from .models import CustomUser, UserPost, LikePost, FriendRequest, ChatRoom, LiveChatMessage

# Create your views here.


class RegisterUserView(SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = CreateUserForm
    template_name = 'register.html'
    success_url = '/login/'
    success_message = 'Account was created!'


class LoginUserView(View):
    def get(self, request):
        return render(request, 'sna/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request, 'Username or Password is incorrect')
            return redirect('/')


class LogoutUserView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        logout(request)
        return redirect('login')


class HomeView(LoginRequiredMixin, CreateView):
    model = UserPost
    form_class = CreateCommentForm
    template_name = 'home.html'
    login_url = '/login/'
    success_url = '/'

    def form_valid(self, form):
        comment_post_form = form.save(commit=False)
        post = UserPost.objects.get(id=self.request.POST['post'])
        comment_post_form.username = self.request.user.username
        comment_post_form.post = post
        comment_post_form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter_friends = CustomUser.objects.filter(
            friends=self.request.user.id).values_list('username', flat=True)
        context['new_post_feed'] = self.model.objects.filter(username__in=filter_friends.all()).order_by('-post_date')
        return context


class LikePostView(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def get(self, request):
        username = request.user.username
        post_id = request.GET.get('post_id')
        post = UserPost.objects.get(id=post_id)

        like = LikePost.objects.filter(
            post_id=post, username=username).first()

        if like == None:
            new_like = LikePost.objects.create(
                post_id=post, username=username)
            new_like.save()
            post.no_of_likes = post.no_of_likes+1
            post.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            like.delete()
            post.no_of_likes = post.no_of_likes-1
            post.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ProfileView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, username):
        profile = CustomUser.objects.get(username=username)

        post_feed = UserPost.objects.filter(profile=profile)

        friend_list = CustomUser.objects.filter(
            friends=self.request.user.id)
        friend_request = FriendRequest.objects.filter(
            receiver=self.request.user.id)

        try:
            friend_request_sent = FriendRequest.objects.get(
                sender=self.request.user, receiver=profile)
        except FriendRequest.DoesNotExist:
            friend_request_sent = None

        try:
            friend_request_exist = FriendRequest.objects.get(
                sender=profile, receiver=self.request.user)
        except FriendRequest.DoesNotExist:
            friend_request_exist = None

        post_form = CreatePostForm(prefix='post_form')
        comment_form = CreateCommentForm(prefix='comment_form')

        context = {
            'profile': profile,
            'post_feed': post_feed,
            'friend_list': friend_list,
            'friend_request': friend_request,
            'friend_request_sent': friend_request_sent,
            'friend_request_exist': friend_request_exist,
            'post_form': post_form,
            'comment_form': comment_form
        }
        return render(request, 'sna/profile.html', context)

    def post(self, request, username):
        post_form = CreatePostForm(prefix='post_form')
        comment_form = CreateCommentForm(prefix='comment_form')

        form = self.request.POST['form']

        if form == 'submit_post':
            post_form = CreatePostForm(
                request.POST, request.FILES, prefix='post_form')
            if post_form.is_valid():
                form = post_form.save(commit=False)
                form.username = self.request.user.username
                form.profile = username
                form.save()
        elif form == 'submit_comment':
            comment_form = CreateCommentForm(
                request.POST, prefix='comment_form')
            if comment_form.is_valid():
                form = comment_form.save(commit=False)
                post = UserPost.objects.get(id=self.request.POST['post'])
                form.username = self.request.user.username
                form.post = post
                form.save()
        return redirect("profile", username)


class FriendsView():
    def friend_request(request, pk):
        sender = request.user
        receiver = CustomUser.objects.get(id=pk)
        friend_request, created = FriendRequest.objects.get_or_create(
            sender=sender, receiver=receiver)
        if created:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            friend_request.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def accept_friend_request(request, pk):
        friend_request = FriendRequest.objects.get(id=pk)
        if friend_request.receiver == request.user:
            friend_request.receiver.friends.add(friend_request.sender)
            friend_request.sender.friends.add(friend_request.receiver)
            friend_request.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def delete_friend_request(request, pk):
        friend_request = FriendRequest.objects.get(id=pk)
        if friend_request.receiver == request.user:
            friend_request.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def unfollow_friend(request, pk):
        friend_list = CustomUser.objects.filter(friends=pk)
        current = request.user
        if current in friend_list:
            CustomUser.objects.get(id=current.id).friends.remove(pk)
            CustomUser.objects.get(id=pk).friends.remove(current.id)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def search_list(search_object):
    profile_search = []
    profile_search_list = []

    if search_object:
        for users in search_object:
            profile_search.append(users.id)

        for ids in profile_search:
            profile_lists = CustomUser.objects.filter(id=ids)
            profile_search_list.append(profile_lists)

        profile_search_list = list(chain(*profile_search_list))
    return profile_search_list


class SearchView(LoginRequiredMixin, TemplateView):
    template_name = 'search.html'

    def get(self, request):
        search = request.GET.get('interest')
        if CustomUser.objects.filter(interests__name__in=[search]):
            search_object = CustomUser.objects.filter(
                interests__name__in=[search])
        else:
            search_object = None

        profile_search_list = search_list(search_object)
        context = {
            'profile_search_list': profile_search_list
        }
        return render(request, self.template_name, context)

    def post(self, request):
        search = request.POST['search']
        if CustomUser.objects.filter(username__icontains=search):
            search_object = CustomUser.objects.filter(
                username__icontains=search)
        elif CustomUser.objects.filter(email__icontains=search):
            search_object = CustomUser.objects.filter(email__icontains=search)
        elif CustomUser.objects.filter(age__icontains=search):
            search_object = CustomUser.objects.filter(age__icontains=search)
        elif CustomUser.objects.filter(interests__name__in=[search]):
            search_object = CustomUser.objects.filter(
                interests__name__in=[search])
        else:
            search_object = None

        profile_search_list = search_list(search_object)

        context = {
            'profile_search_list': profile_search_list
        }
        return render(request, self.template_name, context)


class AccountSettingsView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CustomUser
    form_class = AccountSettingForm
    template_name = 'account_settings.html'
    login_url = '/login/'
    success_url = '/account_settings/'
    success_message = 'Account was updated!'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        account_settings_form = form.save(commit=False)
        account_settings_form.save()
        form.save_m2m()
        return super().form_valid(form)


class LiveChatView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'livechat.html')

    def post(self, request):
        room = request.POST['room_name']

        if room == "":
            return redirect('/livechat/')
        elif ChatRoom.objects.filter(name=room).exists():
            return redirect('/livechat/' + room)
        else:
            new_room = ChatRoom.objects.create(name=room)
            new_room.save()
            return redirect('/livechat/' + room)


class ChatRoomView(LoginRequiredMixin, View):
    def get(self, request, room):
        room_name = ChatRoom.objects.get(name=room)
        context = {
            'room': room,
            'room_name': room_name
        }
        return render(request, 'chatroom.html', context)

    def send(request):
        username = request.user.username
        data = json.loads(request.body)
        message = data['message']
        room_id = data['room_id']

        if request.user.is_staff:
            is_staff = True
        else:
            is_staff = False

        chatroom = ChatRoom.objects.get(name=room_id)

        new_message = LiveChatMessage.objects.create(
            username=username, message=message, chatroom=chatroom, staff=is_staff)
        new_message.save()
        return HttpResponse('Message sent successfully')

    def getMessages(request, room):
        room_details = ChatRoom.objects.get(name=room)
        messages = LiveChatMessage.objects.filter(
            chatroom=room_details)
        return JsonResponse({"messages": list(messages.values())})
