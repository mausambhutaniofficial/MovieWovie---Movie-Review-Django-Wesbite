from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import *
from . forms import *
from django.db.models import Avg


# Create your views here.
def home(request):
    query = request.GET.get('title')
    allmovies = None
    if query:
        allmovies = Movie.objects.filter(name__icontains=query)         #for case insenstivity
    else:
        allmovies = Movie.objects.all()     #select * from Movie
    context = {
        'movies':allmovies
    }

    return render(request, 'main/index.html', context)

def detail(request, id):
    movie = Movie.objects.get(id = id)  #select * from Movie where id = id
    reviews = Review.objects.filter(movie=id).order_by("-comment")
    average = reviews.aggregate(Avg('rating'))['rating__avg']
    if average == None:
        average = 0
    average = round(average,1)
    context = {
        'movie':movie,
        'reviews':reviews,
        'average':average
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

def add_review(request, id):
    if request.user.is_authenticated:
        movie = Movie.objects.get(id=id)
        if request.method == "POST":
            form = ReviewForm(request.POST or None)
            if form.is_valid():
                data = form.save(commit=False)
                data.comment = request.POST['comment']
                data.rating = request.POST['rating']
                data.user = request.user
                data.movie = movie
                data.save()
                return redirect("main:detail", id)
        
        else:
            form = ReviewForm()
        return render(request, 'main/details.html', {'form':form})
    else:
        return redirect("accounts:login")


def edit_review(request, movie_id, review_id):
    if request.user.is_authenticated:
        movie = Movie.objects.get(id=movie_id)
        review = Review.objects.get(movie=movie, id=review_id)

        #check if the review was done by the logged in user
        if request.user == review.user:
            #then grant permission
            if request.method == 'POST':
                form = ReviewForm(request.POST, instance=review)
                if form.is_valid():
                    data = form.save(commit=False)
                    if (data.rating > 10) or (data.rating < 0):
                        error = "Rating Out Of Range. Please give rating from 0 to 10."    
                        return render(request, 'main/editreview.html', {'error':error, 'form':form})
                    else:
                        data.save()
                        return redirect("main:detail", movie_id)
            else:
                form = ReviewForm(instance=review)
            return render(request, "main/editreview.html", {'form':form})
        else:
            return redirect("main:detail", movie_id)
    else:
        return redirect("accounts:login")


def delete_review(request, movie_id, review_id):
    if request.user.is_authenticated:
        movie = Movie.objects.get(id=movie_id)
        review = Review.objects.get(movie=movie, id=review_id)

        #check if the review was done by the logged in user
        if request.user == review.user:
            review.delete()
        
        return redirect("main:detail", movie_id)
    else:
        return redirect("accounts:login")
