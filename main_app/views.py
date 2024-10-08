import requests
import os
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_datetime
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
# from django.http import HttpResponseRedirect
from .models import NewsSource, Dose, FavoriteDose, BookmarkDose, Comment
from .forms import CommentForm, EditCommentForm

BASE_URL = "https://api.thenewsapi.com/v1/news/top?"

# Create your views here.
class Home(LoginView):
    template_name = "home.html"


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('dose-index')  # Redirect to the index page after sign-up

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
        return response


def fetch_doses():
    url = f'{BASE_URL}api_token={os.environ["API_KEY"]}'
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        print(data)  # Debug: print the full response to check its structure

        doses = data.get("data", [])

        if isinstance(doses, list):  # Ensure doses is a list
            for dose in doses:
                if isinstance(dose, dict):  # Ensure dose is a dictionary
                    # Adjusted to reflect the response structure
                    source_name = dose["source"]  # Source is now a string

                    # Get or create the source (assuming you want to keep track of sources)
                    source, created = NewsSource.objects.get_or_create(
                        name=source_name,
                    )

                    Dose.objects.create(
                        source=source,
                        author=dose.get(
                            "author"
                        ),  # 'author' may not be in the response; handle accordingly
                        title=dose.get("title"),
                        description=dose.get("description"),
                        url=dose.get("url"),
                        url_to_image=dose.get("image_url"),
                        published_at=parse_datetime(dose["published_at"]),
                        content=dose.get("snippet"),  # Using snippet as content
                        category=(
                            dose["categories"][0]
                            if dose.get("categories")
                            else "general"
                        ),  # Get the first category or default
                    )
                else:
                    print(f"Unexpected dose format: {dose}")  # Log unexpected formats
        else:
            print("Doses is not a list.")
    else:
        print(f"Error fetching doses: {response.status_code} - {response.text}")


def dose_list(request):
    # fetch_doses() // try this again tomorrow to test if new top articles are fetched
    doses = Dose.objects.all()[:3]
    print(doses)
    return render(request, "doses/index.html", {"doses": doses})


def dose_detail(request, dose_id):
    try:
        dose = Dose.objects.get(id=dose_id)
    except Dose.DoesNotExist:
        return redirect('dose-detail')  # Redirect if the dose does not exist

    comments = dose.comments.all()
    form = CommentForm()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login if the user is not authenticated
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.dose = dose
            comment.user = request.user
            comment.save()
            # Redirect to the same page to display the new comment
            return redirect('dose-detail', dose_id=dose.id)

    return render(request, 'doses/detail.html', {
        'dose': dose,
        'comments': comments,
        'form': form,
    })


# @login_required
def favorite_doses_list(request):
    user = request.user
    favorite_doses = FavoriteDose.objects.filter(user=user).select_related("dose")
    return render(
        request, "doses/favorite_doses_list.html", {"favorite_doses": favorite_doses}
    )


# @login_required
def bookmark_doses_list(request):
    user = request.user
    bookmarked_doses = BookmarkDose.objects.filter(user=user).select_related("dose")
    return render(request, "doses/bookmark_doses_list.html", {"bookmarked_doses": bookmarked_doses})


# @login_required
def bookmark_dose(request, dose_id):
    try:
        dose = Dose.objects.get(id=dose_id)
    except Dose.DoesNotExist:
        return redirect('bookmark-dose-index')  # Redirect if the dose does not exist

    user = request.user

    if not BookmarkDose.objects.filter(dose=dose, user=user).exists():
        BookmarkDose.objects.create(dose=dose, user=user)

    return redirect('bookmark-dose-index')


# @login_required
def unbookmark_dose(request, dose_id):
    try:
        dose = Dose.objects.get(id=dose_id)
    except Dose.DoesNotExist:
        return redirect('bookmark-dose-index')  # Redirect if the dose does not exist

    user = request.user

    bookmark = BookmarkDose.objects.filter(dose=dose, user=user).first()
    if bookmark:
        bookmark.delete()

    return redirect('bookmark-dose-index')


# @login_required
def favorite_dose(request, dose_id):
    try:
        dose = Dose.objects.get(id=dose_id)
    except Dose.DoesNotExist:
        return redirect('favorite-doses-index')  # Redirect if the dose does not exist

    user = request.user

    if not FavoriteDose.objects.filter(dose=dose, user=user).exists():
        FavoriteDose.objects.create(dose=dose, user=user)
    
    return redirect('favorite-doses-index')


# @login_required
def unfavorite_dose(request, dose_id):
    try:
        dose = Dose.objects.get(id=dose_id)
    except Dose.DoesNotExist:
        return redirect('favorite-doses-index')  # Redirect if the dose does not exist

    user = request.user

    favorite = FavoriteDose.objects.filter(dose=dose, user=user).first()
    if favorite:
        favorite.delete()

    return redirect('favorite-doses-index')

# @login_required
def add_comment(request, dose_id):
    try:
        dose = Dose.objects.get(id=dose_id)
    except Dose.DoesNotExist:
        return redirect('dose-index')  # Redirect if the dose does not exist

    user = request.user

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            Comment.objects.create(dose=dose, user=user, text=text)
            return redirect('dose-detail', dose_id=dose_id)
    else:
        form = CommentForm()

    return render(request, 'doses/detail.html', {
        'dose': dose,
        'comment_form': form
    })


def edit_comment(request, dose_id, comment_id):
    try:
        dose = Dose.objects.get(id=dose_id)
        comment = Comment.objects.get(id=comment_id, dose=dose)
    except (Dose.DoesNotExist, Comment.DoesNotExist):
        return redirect('dose-detail', dose_id=dose_id)  # Redirect if the dose or comment does not exist

    if comment.user != request.user:
        return redirect('dose-detail', dose_id=dose_id)  # Redirect if the user is not the author

    if request.method == 'POST':
        form = EditCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('dose-detail', dose_id=dose_id)
    else:
        form = EditCommentForm(instance=comment)

    return render(request, 'doses/edit_comment.html', {
        'dose': dose,
        'comment': comment,
        'form': form
    })


# @login_required
def delete_comment(request, dose_id, comment_id):
    try:
        dose = Dose.objects.get(id=dose_id)
        comment = Comment.objects.get(id=comment_id, dose=dose)
    except (Dose.DoesNotExist, Comment.DoesNotExist):
        return redirect('dose-detail', dose_id=dose_id)  # Redirect if the dose or comment does not exist

    if comment.user != request.user:
        return redirect('dose-detail', dose_id=dose_id)  # Redirect if the user is not the author

    comment.delete()

    return redirect('dose-detail', dose_id=dose_id)

