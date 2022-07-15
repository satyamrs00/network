import http
import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


from .models import User, Post
from .forms import newpostform


def index(request):
    if request.method == "POST":
        p = Post(message=request.POST['message'], user=request.user)
        p.save()
        return redirect('index')
    
    if not request.GET.get('p'):
        return HttpResponseRedirect('/?p=1')
 
    aposts = Post.objects.all().order_by('-id')
    p = Paginator(aposts, 10)
    if int(request.GET.get('p')) not in p.page_range:
        return HttpResponse('Page Not Found', status=404)

    page = p.page(int(request.GET.get('p')))

    return render(request, "network/index.html", {
        "newpostform": newpostform,
        "page": page,
        "formDisplay": "block"
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
def user(request, usern):
    if request.method == "POST":
        userr = User.objects.get(username=usern)
        if userr in request.user.following.all():
            request.user.following.remove(userr)
        else:
            request.user.following.add(userr)
        request.user.save()
        followstatus = "notfollowing"
        if userr in request.user.following.all():
            followstatus = "following"
        return JsonResponse({
            "success": f"updated user {request.user}",
            "followstatus": followstatus
        }, status=200)


    userr = User.objects.get(username=usern)
    posts = userr.posts.all().order_by("-id")
    return render(request, "network/user.html", {
        "userr": userr,
        "posts": posts
    })

@login_required
def following(request):
    if not request.GET.get('p'):
        return HttpResponseRedirect('/following?p=1')

    aposts = Post.objects.filter(user__in=request.user.following.all()).order_by('-id')
    p = Paginator(aposts, 10)

    if int(request.GET.get('p')) not in p.page_range:
        return HttpResponse('Page Not Found', status=404)

    page = p.page(int(request.GET.get('p')))
    return render(request, 'network/index.html', {
        "page": page,
        "formDisplay": "none",
        "cpage": int(request.GET['p']),
        "lpage": p.num_pages
    })

@csrf_exempt
@login_required
def getpost(request, postId):
    try:
        post = Post.objects.get(id=postId)
    except Post.DoesNotExist:
        return HttpResponse("post does not exist")
    if request.method == "PUT":
        data = json.loads(request.body)
        post.message = data.get('message')
        post.is_edited = data.get('is_edited')
        post.save()
        return JsonResponse({
            "success": "message updated",
            "edited_message": post.message
        })

    if request.method == "GET":
        return JsonResponse({
            "id": post.id,
            "message": post.message,
            "userid": post.user.id,
            "username": post.user.username
        }, status=200)
    
    if request.method == "POST":
        p = Post.objects.get(id=postId)
        if request.user in p.likes.all():
            p.likes.remove(request.user)
        else:
            p.likes.add(request.user)
        p.save
        return JsonResponse({
            "success": "like updated",
            "newlikescount": p.getlikescount()
        })