from django.shortcuts import render,HttpResponse,redirect,get_object_or_404,reverse
from .forms import ArticleForm
from .models import Article,Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def articles(request):
    keyword = request.GET.get("keyword")

    if keyword:
        articles = Article.objects.filter(title__contains = keyword)
        return render(request,"articles.html",{"articles":articles})
    
    articles = Article.objects.all()
    return render(request,"articles.html",{"articles":articles})

def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

@login_required(login_url="user:login")
def dashboard(request):
    articles = Article.objects.filter(author = request.user)
    context = {
        "articles" : articles
    }
    return render(request,"dashboard.html",context)

@login_required(login_url="user:login")
def addarticle(request):
    form = ArticleForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()

        messages.success(request,"Makale başarıyla oluşturuldu.")
        return redirect("article:dashboard")

    return render(request,"addarticle.html",{"form":form})

def detail(request,id):
    article = get_object_or_404(Article,id = id)
    #article = Article.objects.filter(id = id).first()
    user = request.user
    total_likes = article.total_likes()

    liked = False
    if article.likes.filter(username=request.user.username).exists():
        liked = True
   

    comments = article.comments.all()
    context = {
        "article":article,
        "comments":comments,
        "total_likes":total_likes,
        "liked":liked,
        "user":user
        }
    
    return render(request,"detail.html",context)

@login_required(login_url="user:login")
def updatearticle(request,id):
    article = get_object_or_404(Article,id=id)
    form = ArticleForm(request.POST or None,request.FILES or None,instance = article)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()

        messages.success(request,"Makale başarıyla güncellendi.")
        return redirect("article:dashboard")

    return render(request,"update.html",{"form":form})

@login_required(login_url="user:login")
def deletearticle(request,id):
    article = get_object_or_404(Article,id=id)
    article.delete()
    messages.success(request,"Makale başarıyla silindi.")
    return redirect("article:dashboard")

@login_required(login_url="user:login")
def addcomment(request,id):
    article = get_object_or_404(Article,id=id)

    if request.method == "POST":
        
        comment_content = request.POST.get("comment_content")

        newComment = Comment(comment_content = comment_content)
        newComment.comment_author = request.user
        newComment.article = article
        newComment.save()
    return redirect(reverse("article:detail",kwargs={"id":id}))

@login_required(login_url="user:login")
def likearticle(request,id):
    article = get_object_or_404(Article,id=id)
    
    liked = False
    if article.likes.filter(username=request.user.username).exists():
        article.likes.remove(request.user)
        liked = False
        messages.success(request,"Makale beğenisi başarıyla kaldırıldı.")
    else:
        article.likes.add(request.user)
        liked = True
        messages.success(request,"Makale başarıyla beğenildi.")
    
    return redirect(reverse("article:detail",kwargs={"id":id}))

def privacy_policy(request):
    return render(request,"privacy_policy.html")
