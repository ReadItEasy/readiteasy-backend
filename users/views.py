from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


# @csrf_exempt
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print("valid OOOOOOOOOOOO")

            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You can now login.')
            return redirect('login')
        else:
            print("not valid TTTTTTTT")
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def profile(request):
    user = {}
    user['username'] = 0
    return render(request, 'users/profile.html')

@csrf_exempt
def apiRegister(request):
    if request.method == 'POST':
        print("request.body", request.body)

        form = UserCreationForm(request.body)
        if form.is_valid():
            print("valid OOOOOOOOOOOO")

            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You can now login.')
            return redirect('login')
        else:
            print("not valid TTTTTTTT")
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})