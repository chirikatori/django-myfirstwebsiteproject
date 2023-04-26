from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import Mytable

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def home(request):
    records = Mytable.objects.all()

    #Check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have been Logged In")
            return redirect('home')
        else:
            messages.success(request, "There was an Error, try again")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records': records})

@csrf_exempt
def logout_user(request):
    logout(request)
    messages.success(request, "You have been Logged Out")
    return redirect('home')

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #Authenticate
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered")
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form':form})

@csrf_exempt
def crawler(request):
    crawl_list = Mytable.objects.all()

    pagination = Paginator(Mytable.objects.all(), 10)
    page = request.GET.get('page')
    crawls = pagination.get_page(page)
    nums = "a" * crawls.paginator.num_pages
    return render(request, 
                  'mytable.html', 
                  {'crawl_list': crawl_list, 
                    'crawls':crawls,
                    'nums': nums})

@csrf_exempt
def show_off(request, Mytable_id):
    data = Mytable.objects.get(pk=Mytable_id)
    return render(request, 'show_off.html', {'data': data})

@csrf_exempt
def searchInfo(request):
    crawls = Mytable.objects.all()
    if 'searched' in request.GET:
        searched = request.GET['searched']
        multiple_search = Q(Q(title__icontains=searched) | Q(url__icontains=searched) | Q(content__icontains=searched))
        pagination = Paginator(Mytable.objects.filter(multiple_search), 8)
        page = request.GET.get('page')
        try:
            crawls = pagination.page(page)
        except PageNotAnInteger:
            crawls = pagination.page(1)
        except EmptyPage:
            crawls = pagination.page(pagination.num_pages)
        return render(request, 'searchInfo.html', {'searched': searched, 'crawls':crawls,})
    else:
        return render(request, 'searchInfo.html', {})
    

    