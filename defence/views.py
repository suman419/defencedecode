from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import EmptyPage,Paginator,PageNotAnInteger
from django.shortcuts import render,get_object_or_404,redirect
from defence.models import Category, Post, Comment, Contact, VideoItem, AboutCompany
from taggit.models import Tag
from django.contrib import messages
import datetime
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect,JsonResponse,Http404
from .forms import CommentForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.

def post_list(request):
    week_ago = datetime.date.today() - datetime.timedelta(days=15)
    trends = Post.objects.filter(created__gte =week_ago).order_by('-post_views')[0:5]
    post_list = Post.objects.filter(status='published').order_by('-id')[1::]
    latest_post = Post.objects.filter(status='published').order_by('-id')[0]
    popular_post = Post.objects.filter(status='published').order_by('-post_views')[0:5] 
    paginator=Paginator(post_list, 2)
    page_number=request.GET.get('page')
    query=request.GET.get("q")
    if query:
        post_list=post_list.filter(Q(title__icontains=query) | Q(body__icontains=query) | Q(publish__icontains=query)).distinct()   
    try:
        post_list=paginator.page(page_number)
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage:
        post_list=paginator.page(paginator.num_pages)
    return render(request, 'index.html', {'post_list':post_list, 'latest_post':latest_post,'popular_post':popular_post,'trends':trends})


def post_detail(request,pk):
    #post_obj=get_object_or_404(Post,slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)
    post_obj = Post.objects.get(id=pk)
    post_obj.post_views = post_obj.post_views+1
    post_obj.save()
    comments=post_obj.comments.filter(active=True)
    csubmit=False
    if request.method=='POST':
        if request.user.is_authenticated:
            form=CommentForm(request.POST)
            if form.is_valid():
                new_comment=form.save(commit=False)
                new_comment.post=post_obj
                new_comment.save()
                csubmit=True
                messages.success(request,f' Post Created Successfully !')
        else:
            messages.success(request,f' Please login first !')
            form=CommentForm()
    else:
        form=CommentForm()
    popular_post = Post.objects.filter(status='published').order_by('-post_views')[0:5] 
    is_liked=False
    if post_obj.post_likes.filter(id=request.user.id).exists():
        is_liked=True
    return render(request, 'post_detail.html', {'post_obj':post_obj,'form':form,'csubmit':csubmit,'comments':comments,'popular_post':popular_post,'is_liked':is_liked,'total_likes':post_obj.total_likes()})

def asian_country_post(request):
    category = Category.objects.get(name='Asia') 
    latest_post = Post.objects.filter(category=category)[0]
    asian_country_post = Post.objects.filter(category=category).order_by('-id')[1::] 
    popular_post = Post.objects.filter(status='published').order_by('-post_views')[0:5]
    paginator=Paginator(asian_country_post, 5)
    page_number=request.GET.get('page')
    query=request.GET.get("q")
    if query:
        asian_country_post=asian_country_post.filter(Q(title__icontains=query) | Q(body__icontains=query) | Q(publish__icontains=query)).distinct()   
    try:
        asian_country_post=paginator.page(page_number)
    except PageNotAnInteger:
        asian_country_post=paginator.page(1)
    except EmptyPage:
        asian_country_post=paginator.page(paginator.num_pages)
    return render(request, 'asia.html',{'asian_country_post':asian_country_post,'latest_post':latest_post,'popular_post':popular_post})   

def about_us(request):
    company_detail = AboutCompany.objects.all()
    popular_post = Post.objects.filter(status='published').order_by('-post_views')[0:5]
    for company_detail in company_detail:
        return render(request, 'aboutus.html', {'company_detail':company_detail,'popular_post':popular_post})

def contact_form(request):
    return render(request, 'contact.html')

def contact_us(request):
    if request.method =="POST":
        your_name =request.POST['yourname']
        your_email =request.POST['youremail']
        your_phone =request.POST['yourphone']
        your_address =request.POST['youraddress']
        details = request.POST['details']
        Contact.objects.create(name=your_name,email=your_email,phone=your_phone,address=your_address,body=details)
        messages.success(request,f' Message Send Successfully !')
        return redirect("/")
    return render(request, 'contact.html')       

def broadcast_video(request):
    my_video = VideoItem.objects.all()
    popular_post = Post.objects.filter(status='published').order_by('-post_views')[0:5]
    return render(request, 'broadcast.html',{'my_video':my_video,'popular_post':popular_post})

def europe_country_post(request):
    category = Category.objects.get(name='Asia') 
    latest_post = Post.objects.filter(category=category)[0]
    europe_country_post = Post.objects.filter(category=category).order_by('-id')[1::] 
    popular_post = Post.objects.filter(status='published').order_by('-post_views')[0:5]
    paginator=Paginator(europe_country_post, 5)
    page_number=request.GET.get('page')
    query=request.GET.get("q")
    if query:
        europe_country_post=europe_country_post.filter(Q(title__icontains=query) | Q(body__icontains=query) | Q(publish__icontains=query)).distinct()   
    try:
        europe_country_post=paginator.page(page_number)
    except PageNotAnInteger:
        europe_country_post=paginator.page(1)
    except EmptyPage:
        europe_country_post=paginator.page(paginator.num_pages)
    return render(request, 'asia.html',{'europe_country_post':europe_country_post,'latest_post':latest_post,'popular_post':popular_post})   

def latest_news(request):
    latest_post = Post.objects.filter(status='published').order_by('-id')
    popular_post = Post.objects.filter(status='published').order_by('-post_views')[0:5] 
    week_ago = datetime.date.today() - datetime.timedelta(days=15)
    trends = Post.objects.filter(created__gte =week_ago).order_by('-post_views')[0:5]
    paginator=Paginator(latest_post, 5)
    page_number=request.GET.get('page')
    query=request.GET.get("q")
    if query:
        latest_post=latest_post.filter(Q(title__icontains=query) | Q(body__icontains=query) | Q(publish__icontains=query)).distinct()   
    try:
        latest_post=paginator.page(page_number)
    except PageNotAnInteger:
        latest_post=paginator.page(1)
    except EmptyPage:
        latest_post=paginator.page(paginator.num_pages)
    return render(request, 'latest_news.html', { 'latest_post':latest_post,'popular_post':popular_post,'trends':trends})

#Like & Dislike

def like_post(request):
    post=get_object_or_404(Post,id=request.POST.get('post_id'))
    is_liked=False
    if request.user.is_authenticated:
        if post.post_likes.filter(id=request.user.id).exists():
            post.post_likes.remove(request.user)
            is_liked=False
        else:
            post.post_likes.add(request.user)
            is_liked=True
        context={'post':post,'is_liked':is_liked,'total_likes':post.total_likes()}
        return HttpResponseRedirect(reverse('defence:post_detail',args = (post.id,)))
    else:
        messages.success(request,f' login first !')
        context={'post':post,'is_liked':is_liked,'total_likes':post.total_likes()}
        return HttpResponseRedirect(reverse('defence:post_detail',args = (post.id,)))  
    #return HttpResponseRedirect(request.path)
    
       