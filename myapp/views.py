from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm, MessageForm, UsernameChangeForm, EmailChangeForm, ThumbnailChangeForm
from myapp.models import CustomUser, Message
from django.db.models import Q
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return render(request, "myapp/index.html", {'form': form})
    else:
        form = SignUpForm()
    return render(request, "myapp/signup.html", {'form': form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                return redirect('friends')
            else:
                # Authentication failed
                # You may want to handle this case differently, e.g., show an error message
                pass
    else:
        form = LoginForm()

    return render(request, "myapp/login.html", {'form':form})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def friends(request):
    user = request.user
    friends = CustomUser.objects.exclude(id=user.id)
    for friend in friends:
        latest_message = Message.objects.filter(
            (Q(from_name=user, to_name=friend) | Q(from_name=friend, to_name=user))
        ).order_by('-created_at').first()
        friend.latest_message = latest_message
    return render(request, "myapp/friends.html", {'friends': friends})


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
    if request.method == 'POST':
        form = ThumbnailChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = EmailChangeForm(instance=request.user)
    
    return render(request, 'myapp/thumbnail_change.html', {'form': form})