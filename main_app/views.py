from django.db.models import fields
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView

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
        'content_': content_
    })

#detail (show)
def content_detail(request, content_id):
    cont = Content.objects.get(id=content_id)
    return render(request, 'content/detail.html', {
        'cont': cont
    })

#create
class ContentCreate(CreateView):
    model = Content
    fields= '__all__'

#update
class ContentUpdate(UpdateView):
    model = Content
    fields = ['name', 'description', 'seasons']
        

#delete
class ContentDelete(DeleteView):
    model = Content
    success_url = '/content/'
        

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