from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import *
from . forms import *


# Create your views here.
def home(request):
    allmovies = Movie.objects.all()     #select * from Movie
    context = {
        'movies':allmovies
    }

    return render(request, 'main/index.html', context)

def detail(request, id):
    movie = Movie.objects.get(id = id)  #select * from Movie where id = id
    context = {
        'movie':movie
    }

    return render(request, 'main/details.html', context)

def add_movies(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == 'POST':
                form = MovieForm(request.POST or None)

                if form.is_valid():
                    data = form.save(commit=False)
                    data.save()
                    return redirect("main:home")
            else:
                form = MovieForm()
            return render(request, 'main/addmovies.html', {'form':form, 'controller_h':'Add A Movie!', 'controller':'Add Movie'})

        #if they are not admin
        else:
            return redirect("main:home")
    #if they are not logged in
    return redirect("accounts:login")


def edit_movies(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            movie = Movie.objects.get(id=id)
            if request.method == 'POST':
                form = MovieForm(request.POST or None, instance=movie)
                if form.is_valid():
                    data = form.save(commit=False)
                    data.save()
                    return redirect("main:detail", id)
            else:
                form = MovieForm(instance=movie)
            return render(request, 'main/addmovies.html', {'form':form, 'controller_h':'Edit A Movie!', 'controller':'Edit Movie'})

        #if they are not admin
        else:
            return redirect("main:home")
    #if they are not logged in
    return redirect("accounts:login")

def delete_movies(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            movie = Movie.objects.get(id=id)
            movie.delete()
            return redirect('main:home')
    
        #if they are not admin
        else:
            return redirect("main:home")
    
    #if they are not logged in
    return redirect("accounts:login")