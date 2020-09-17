from django.shortcuts import render, redirect
from .models import User, Book, Review
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    return render(request, "index.html")

def books(request):
    if 'logged_in_user' not in request.session:
        return redirect("/")
    else:
        context = {
            'logged_in': User.objects.get(id=request.session['logged_in_user']),
            'allbooks': Book.objects.all(),
            'reviews': Review.objects.all().order_by("-created_at")[:3]
        }
        return render(request, "dashboard.html", context)

def add_book(request):
    if 'logged_in_user' not in request.session:
        return redirect("/")
    else:
        context = {
            'bookauthors': Book.objects.all()
        }
        return render(request, "addBook.html", context)

def one_book(request, id):
    if 'logged_in_user' not in request.session:
        return redirect("/")
    else:
        context = {
            'book': Book.objects.get(id=id)
        }
        return render(request, "book.html", context)

def one_user(request, id):
    if 'logged_in_user' not in request.session:
        return redirect("/")
    else:
        context = {
            'user': User.objects.get(id=id)
        }
        return render(request, "user.html", context)

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        newuser = User.objects.create(name=request.POST['name'],alias=request.POST['alias'],email=request.POST['email'],password=hash1)
        request.session['logged_in_user'] = newuser.id
        return redirect("/books")

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['logged_in_user'] = user.id
        return redirect("/books")

def new_book(request):
    if 'logged_in_user' not in request.session:
        return redirect("/")
    else:
        errors = Book.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/books/add")
        else:
            if len(request.POST['newauthor']) > 0:
                book = Book.objects.create(title=request.POST['title'], author=request.POST['newauthor'])
            else:
                book = Book.objects.create(title=request.POST['title'], author=request.POST['author'])
            user = User.objects.get(id=request.session['logged_in_user'])
            Review.objects.create(content=request.POST['content'],rating=request.POST['rating'],user=user,book=book)
            return redirect(f"/books/{book.id}")

def logout(request):
    del request.session['logged_in_user']
    return redirect("/")

def addreview(request, id):
    book = Book.objects.get(id=id)
    user = User.objects.get(id=request.session['logged_in_user'])
    Review.objects.create(content=request.POST['content'],rating=request.POST['rating'],user=user,book=book)
    return redirect(f"/books/{book.id}")

def delete(request, id):
    rev = Review.objects.get(id=id)
    rev.delete()
    return redirect(f"/books/{rev.book.id}")