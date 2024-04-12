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



def index(request):
    return render(request, "myapp/index.html")
    

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
            # print("Form is valid")
            keyword = form.cleaned_data['keyword'] 
            friends = CustomUser.objects.filter(username__icontains=keyword).exclude(id=user.id)
            context={
                "form": form,
                "friends":friends,
                # 検索結果を表示する画面にするために、そうであることを明示する変数を作る
                "is_searched": True,
            }
            return render(request, "myapp/friends.html", context)
        # else:
            # print("Form is invalid")  # Debugging print statement
            # print(form.errors)  # Debugging print statement

    context = {
        "form": form,
        "friends": friends,
    }

    

    
    for friend in friends:
        latest_message = Message.objects.filter(
            Q(from_name=user, to_name=friend) | Q(from_name=friend, to_name=user)
        ).order_by('-created_at').last()
        friend.latest_message = latest_message

        
    return render(request, "myapp/friends.html", context)




@login_required
def talk_room(request, pk):

    user = request.user
    friend = get_object_or_404(CustomUser, pk=pk)

     
    messages = Message.objects.all().filter(
        Q(from_name=user, to_name=friend) | Q(from_name=friend, to_name=user)
    ).order_by('-created_at')

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




