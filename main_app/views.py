from django.shortcuts import render
from django.views.generic.edit import CreateView

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
    content_ = Content.objects.get(id=content_id)
    return render(request, 'content/detail.html', {
        'content_': content_
    })

#create
class ContentCreate(CreateView):
    model = Content
    fields= '__all__'

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