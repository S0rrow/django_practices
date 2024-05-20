from django.shortcuts import render
from .forms import UserForm

# Create your views here.

def signup(request):
    if request.method=="POST":
        pass
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {"form":form})
    
