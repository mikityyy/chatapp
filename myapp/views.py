from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import  MessageForm, UsernameChangeForm, EmailChangeForm, ThumbnailChangeForm, PasswordChangeForm, FriendSearchForm
from myapp.models import CustomUser, Message
from django.db.models import Q
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import ListView
import operator
from django.db.models import Max




def index(request):
    ip = request.META.get('REMOTE_ADDR')  # これで取得できたIPをINTERNAL_IPSに追加する
    return render(request, 'myapp/index.html', {"ip": ip})
    
    

# def signup(self, request, user):
#     form = SignupForm(request.POST)
#     if form.is_valid():
#         user.thumbnail = form.cleaned_data['thumbnail']
#         user.save()
#     return user



@login_required
def friends(request):
    form=FriendSearchForm()
    user = request.user
    friends = CustomUser.objects.exclude(id=user.id)
    
    
    if request.method == "GET" and "friends_search" in request.GET:
        form = FriendSearchForm(request.GET)
        # print("Form submitted with search query")

        if form.is_valid():
            keyword = form.cleaned_data['keyword']
            email = form.cleaned_data['email']
            
            # ユーザー名の部分一致検索
            friends = CustomUser.objects.filter(
                Q(username__icontains=keyword)
            ).exclude(id=user.id)

            # メールアドレスの部分一致検索
            if email:
                friends = friends.filter(email__icontains=email)
            
            context = {
                "form": form,
                "friends": friends,
                "is_searched": True,
            }
            return render(request, "myapp/friends.html", context)

        # 友達の ID をリストとして取得
    friend_ids = friends.values_list('id', flat=True)

    # メッセージを取得するクエリ
    latest_messages = Message.objects.filter(
        Q(from_name=user, to_name_id__in=friend_ids) | Q(from_name_id__in=friend_ids, to_name=user)
    ).annotate(
        latest_message_time=Max('created_at')
    )

    # 最新のメッセージを友達ごとに取得し、辞書に保存する
    latest_messages_dict = {}
    for msg in latest_messages:
        if msg.from_name_id == user.id:
            friend_id = msg.to_name_id
        else:
            friend_id = msg.from_name_id
        
        if friend_id not in latest_messages_dict or msg.latest_message_time > latest_messages_dict[friend_id]['latest_message_time']:
            latest_messages_dict[friend_id] = {'latest_message': msg, 'latest_message_time': msg.latest_message_time}

    # 友達のリストに最新のメッセージを追加する
    for friend in friends:
        friend.latest_message = latest_messages_dict.get(friend.id, {}).get('latest_message')

    # context に追加
    context = {
        "form": form,
        "friends": friends,
    }
    
    return render(request, "myapp/friends.html", context)




@login_required
def talk_room(request, pk):

    user = request.user
    friend = get_object_or_404(CustomUser, pk=pk)

     
    messages = Message.objects.filter(
        Q(from_name=user, to_name=friend) | Q(from_name=friend, to_name=user)
    ).select_related('from_name', 'to_name').order_by('-created_at')

    form=MessageForm
    data = {
        'form':form,
        'messages': messages,
        'friend':friend,
    }


    if request.method == 'POST':

        obj = Message()
        form = MessageForm(request.POST, instance=obj)

        if form.is_valid():
            
            # 送信者と受信者を設定して保存する
            form.instance.from_name = request.user
            form.instance.to_name = get_object_or_404(CustomUser, pk=pk)
            form.save()
            return redirect("talk_room", pk)
           
    
    # テンプレートにデータを渡してレンダリングする
    return render(request, "myapp/talk_room.html", data)



@login_required
def setting(request):
    return render(request, "myapp/setting.html")



@login_required
def username_change(request):
    if request.method == 'POST':
        form = UsernameChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UsernameChangeForm(instance=request.user)
    
    return render(request, 'myapp/username_change.html', {'form': form})



@login_required
def email_change(request):
    if request.method == 'POST':
        form = EmailChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = EmailChangeForm(instance=request.user)
    
    return render(request, 'myapp/email_change.html', {'form': form})




@login_required
def thumbnail_change(request):
    if request.method == 'POST' :
        form = ThumbnailChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ThumbnailChangeForm(instance=request.user)
    
    return render(request, 'myapp/thumbnail_change.html', {'form': form})


class PasswordChangeView(PasswordChangeView):
    template_name = 'myapp/password_change.html'  # パスワード変更フォームのテンプレート
    form_class = PasswordChangeForm
    success_url = reverse_lazy('index')  # パスワード変更成功後のリダイレクト先のURL




