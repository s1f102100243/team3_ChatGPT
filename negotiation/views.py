from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.utils import timezone
from django.template import loader
from .forms import ChatForm
from negotiation.models import Article, Comment
from django.http import Http404, JsonResponse
from django.conf import settings

import openai

API_KEY = settings.OPENAI_API_KEY
BASE_URL = settings.OPENAI_API_BASE


# Create your views here.

def index(request):
    """
    チャット画面
    """
    client = openai.OpenAI(

    api_key=API_KEY,

    base_url=BASE_URL,
    )

    # 応答結果
    chat_results = ""

    if request.method == "POST":
        # ChatGPTボタン押下時

        form = ChatForm(request.POST)
        if form.is_valid():

            sentence = form.cleaned_data['sentence']

            # ChatGPT
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "日本語で応答してください"
                    },
                    {
                        "role": "user",
                        "content": sentence
                    },
                ],
            )

            chat_results = response.choices[0].message.content
    else:
        form = ChatForm()

    template = loader.get_template('negotiation/index.html')
    context = {
        'form': form,
        'chat_results': chat_results
    }
    return HttpResponse(template.render(context, request))

def feedback(request):
    if request.method == 'POST':
        article = Article(title=request.POST['title'], body=request.POST['text'])
        article.save()
        return redirect(reply, article.id)
    
    if ('sort' in request.GET):
        if request.GET['sort'] == 'like':
            articles = Article.objects.order_by('-like')
        else:
            articles = Article.objects.order_by('-posted_at')
    else:
        articles = Article.objects.order_by('-posted_at')
    context = {
        "articles": articles    
    }
    
    return render(request, 'negotiation/feedback.html', context)

def update(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404('Article does not exist')
    if request.method == 'POST':
        article.title = request.POST['title']
        article.body = request.POST['text']
        article.save()
        return redirect(reply, article_id)
    context = {
        'article': article
    }
    return render(request, 'negotiation/edit.html', context)
    


def reply(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except:
        raise Http404('Article does not exist')
    
    if request.method == 'POST':
        comment = Comment(article=article, text=request.POST['text'])
        comment.save()
    context = {
        "article": article,
        'comments' : article.comments.order_by('-posted_at')
    }
    return render(request, "negotiation/reply.html", context)


def delete(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404('Article does not exist')

    article.delete()
    
    return redirect(feedback)

def like(request, article_id):
    try:
        article = Article.objects.get(pk = article_id)
        article.like += 1
        article.save()
    except Article.DoesNotExist:
        raise Http404("Article does not exist")

    return redirect(reply, article_id)

def api_like(request, article_id):
    try:
        article = Article.objects.get(pk = article_id)
        article.like += 1
        article.save()
    except Article.DoesNotExist:
        raise Http404("Article does not exist")
    result = {
        'id' : article_id,
        'like' : article.like
    }

    return JsonResponse(result)

def room(request, room_name):
    return render(request, "negotiation/room.html", {"room_name": room_name})

