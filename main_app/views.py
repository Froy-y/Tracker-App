from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from .models import Content, Entry, Platform
from .forms import EntryForm, DeleteEntry

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
    content = Content.objects.get(id=content_id)
    platforms_content_doesnt_have = Platform.objects.exclude(id__in = content.platform.all().values_list('id'))
    entry_form = EntryForm()
    return render(request, 'content/detail.html', {
        'cont': content,
        'entry_form': entry_form,
        'platforms': platforms_content_doesnt_have
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
#create
def add_entry(request, content_id):
    form = EntryForm(request.POST)
    if form.is_valid():
        new_entry = form.save(commit=False)
        new_entry.content_id = content_id
        new_entry.save()
    return redirect('detail', content_id=content_id)

# delete
def delete_entry(request, content_id):
    entry = Entry.objects.filter(content_id=content_id)
    form = DeleteEntry(request.POST)
    if form.is_valid():
        entry.delete()
    return redirect('detail', content_id=content_id)

# def delete_entry(request, content_id):
#     entry = get_object_or_404(Entry, content_id=content_id)
#     if request.method == "POST":
#         form = DeleteEntry(request.POST, instance=entry)
#         if form.is_valid:
#             entry.delete()
#             return redirect('detail')
#     else:
#         form = DeleteEntry(instance=entry)
#     return render(request, 'detail', {
#         'form': form,
#         'entry': entry
#     })

#many to many -classes-
#index
class PlatformList(ListView):
    model = Platform

#detail (show)
class PlatformDetail(DetailView):
    model = Platform

#create
class PlatformCreate(CreateView):
    model = Platform
    fields = '__all__'

#update
class PlatformUpdate(UpdateView):
    model = Platform
    fields = '__all__'

#delete
class PlatformDelete(DeleteView):
    model = Platform
    success_url = '/platforms'

#associations
#assoc
def assoc_platform(request, content_id, platform_id):
    Content.objects.get(id=content_id).platform.add(platform_id)
    return redirect('detail', content_id=content_id)
    
#unassoc
def unassoc_platform(request, content_id, platform_id):
    Content.objects.get(id=content_id).platform.remove(platform_id)
    return redirect('detail', content_id=content_id)    

#photo -aws-


#signup -auth-
