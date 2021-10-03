from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Book
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        errors= User.objects.register_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user=User.objects.create(first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=pw_hash)
        request.session['user_id'] = new_user.id
        return redirect('profile/')
    return redirect('/')

def signin(request):
    errors= User.objects.login_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        this_user= User.objects.filter(email=request.POST['email'])[0]
        request.session['user_id']=this_user.id
        return redirect('profile/')

def profile(request):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user=User.objects.filter(id = request.session['user_id'])
    context={
        'user': this_user[0],
        'all_the_books':Book.objects.all(),
        #'uploader':Book.objects.first().uploaded_by
        
    }
    return render(request,'profile.html', context)

def create_book(request):
    errors= Book.objects.book_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/profile')
    else:
        this_user=User.objects.filter(id = request.session['user_id'])
        new_book=Book.objects.create(title=request.POST['title'],
        description=request.POST['description'], uploaded_by=this_user)
    this_user.liked_books.add(new_book)
    return redirect('profile/')


def logout(request):
    request.session.flush()
    return redirect('/')


# Create your views here.
