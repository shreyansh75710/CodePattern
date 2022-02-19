from django.shortcuts import render, redirect
from .models import codeSnippet, comment, theoryNote, feedback as fb
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
import requests
import os

def sendMessage(token, msg, chat_id):
    url = "https://api.telegram.org/bot{}/sendMessage?text={}&chat_id={}".format(token, msg, chat_id)
    requests.get(url)

# Create your views here.
def index(request):
    theorynotes = theoryNote.objects.all()
    query  = request.GET.get('query')
    if query is not None:
        codeSnippets = codeSnippet.objects.filter(
            Q(question__contains=query) |
            Q(user__username__contains=query)
        )
    else:
        codeSnippets = codeSnippet.objects.all()
    context = {'codeSnippets':codeSnippets, 'theoryNotes':theorynotes}
    if not request.user.is_authenticated :
        messages.add_message(request, messages.INFO,'Login or register to access theorynotes or view CodeSnippets.')
    return render(request, 'base/index.html', context)

def deleteComment(request, pk):
    Comment = comment.objects.get(id=pk)
    id = Comment.codeSnippet.id
    Comment.delete()
    messages.add_message(request, messages.SUCCESS, 'Comment deleted')
    return redirect('codeView', id)


@login_required
def codeView(request, pk):
    CodeSnippet = codeSnippet.objects.get(id=pk)
    if request.method == 'POST':
        commentText = request.POST.get('comment')
        Comment = comment(codeSnippet=CodeSnippet, user=request.user, comment=commentText)
        Comment.save()
    comments = comment.objects.filter(codeSnippet=CodeSnippet)
    return render(request, 'base/codeView.html', {'codeSnippet':CodeSnippet,'comments':comments})

@login_required
def feedback(request):
    if request.method == 'POST':
        description = request.POST.get("feedback")
        Feedback = fb(user=request.user, description=description)
        Feedback.save()
        messages.add_message(request, messages.SUCCESS, "Feedback submitted")
        sendMessage(
            str(os.environ.get('telegramToken')),
            "New Feedback\n\"{}\"\n@{}".format(Feedback.description,Feedback.user), 
            "1385528751"
        )
    return redirect("index")

@login_required
def codeUpdate(request, pk):
    CodeSnippet = codeSnippet.objects.get(id=pk)
    if not request.user == CodeSnippet.user :
        messages.add_message(request, messages.ERROR, 'You are not authorised to edit this code snippet')
        return redirect('index')
    if request.method == 'POST':
        CodeSnippet.question = request.POST.get('question')
        CodeSnippet.solution = request.POST.get('solution')
        CodeSnippet.save()
        messages.add_message(request, messages.SUCCESS, 'Code snippet updated successfully.')
        return redirect('codeView', CodeSnippet.id)
    return render(request, 'base/codeUpdate.html', {'codeSnippet':CodeSnippet})

@login_required
def codeDelete(request, pk):
    CodeSnippet = codeSnippet.objects.get(id=pk)
    CodeSnippet.delete()
    messages.add_message(request, messages.SUCCESS, 'Code Snippet deleted succesfully.')
    return redirect('index')

@login_required
def codeCreate(request):
    if request.method == 'POST':
        CodeSnippet = codeSnippet()
        CodeSnippet.user = request.user
        CodeSnippet.question = request.POST.get('question')
        CodeSnippet.solution = request.POST.get('solution')
        CodeSnippet.save()
        messages.add_message(request, messages.SUCCESS, 'Code snippet added successfully')
        return redirect('codeView', CodeSnippet.id)
    return render(request, 'base/codeUpdate.html')

@login_required
def noteView(request, pk):
    notesObject = theoryNote.objects.get(id=pk)
    return render(request, 'base/noteView.html',{'note':notesObject})