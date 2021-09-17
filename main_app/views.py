from django.shortcuts import render

from .models import Content

# Create your views here.
#home
def home(request):
    return render(request, 'home.html')

#about
def about(request):
    return render(request, 'about.html')

#index
def content(request):
    content_ = Content.objects.all()
    return render(request, 'content/index.html', {
        'content': content_
    })

#detail (show)

#create

#update

#delete

#one to one

#many to many -classes-
#index

#detail (show)

#create

#associations
#assoc

#unassoc

#photo -aws-

#signup -auth-