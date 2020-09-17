from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('books', views.books),
    path('books/add', views.add_book),
    path('books/<int:id>', views.one_book),
    path('users/<int:id>', views.one_user),
    path('register', views.register),
    path('login', views.login),
    path('books/new', views.new_book),
    path('logout', views.logout),
    path('addreview/<int:id>', views.addreview),
    path('deletereview/<int:id>', views.delete)
]


#ALL THE URLS
#Login page - HTML (GET)
#Dashboard - HTML (GET)
#Add a book - HTML (GET)
#One Book - HTML (GET)
#One User - HTML (GET)
#Post request for Register (POST)
#Post request for Login (POST)
#Post request for adding a book (POST)