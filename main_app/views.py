from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Content
from .forms import EntryForm

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
    entry_form = EntryForm()
    return render(request, 'content/detail.html', {
        'cont': cont,
        'entry_form': entry_form
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
def add_entry(request, content_id):
    form = EntryForm(request.POST)
    if form.is_valid():
        new_entry = form.save(commit=False)
        new_entry.content_id = content_id
        new_entry.save()
    return redirect('detail', content_id=content_id)

#many to many -classes-
#index

#detail (show)

#create

#associations
#assoc

#unassoc

#photo -aws-

#signup -auth-