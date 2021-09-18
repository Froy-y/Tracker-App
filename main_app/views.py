from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.conf import settings

from .models import Content, Entry, Platform, Photo
from .forms import EntryForm, DeleteEntry

import os
import uuid
import boto3
import botocore.exceptions

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
def add_photo(request, content_id):
      # photo-file will be the "name" attribute on the <input type="file">
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
      s3 = boto3.client('s3')
      # need a unique "key" for S3 / needs image file extension too
      key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
      # just in case something goes wrong
      try:
          bucket = os.environ['S3_BUCKET']
          s3.upload_fileobj(photo_file, bucket, key)
          # build the full url string
          url = f"https://{bucket}.{os.environ['S3_BASE_URL']}{key}"
          print(url)
          # we can assign to content_id or content (if you have a content object)
          Photo.objects.create(url=url, content_id=content_id)
      except botocore.exceptions.ClientError as error:
            print('An error occurred uploading file to S3')
            # Put your error handling logic here
            raise error
      except botocore.exceptions.ParamValidationError as error:
            raise ValueError('The parameters you provided are incorrect: {}'.format(error))
      except:
          print('An error occurred uploading file to S3')
  return redirect('detail', content_id=content_id)

#delete photo
def delete_photo(request, content_id):
      # photo-file will be the "name" attribute on the <input type="file">
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
      s3 = boto3.client('s3')
      # need a unique "key" for S3 / needs image file extension too
      key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
      # just in case something goes wrong
      try:
          bucket = os.environ['S3_BUCKET']
          s3.upload_fileobj(photo_file, bucket, key)
          # build the full url string
          url = f"https://{bucket}.{os.environ['S3_BASE_URL']}{key}"
          # we can assign to content_id or content (if you have a content object)
          Photo.objects.get(url=url, content_id=content_id)
          s3.Objects.delete(Bucket=bucket, Key=key, url=url, content_id=content_id)
      except botocore.exceptions.ClientError as error:
            print('An error occurred uploading file to S3')
            # Put your error handling logic here
            raise error
      except botocore.exceptions.ParamValidationError as error:
            raise ValueError('The parameters you provided are incorrect: {}'.format(error))
      except:
          print('An error occurred uploading file to S3')
  return redirect('detail', content_id=content_id)
#signup -auth-
