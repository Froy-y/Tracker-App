from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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
@login_required
def content(request):
    content_ = Content.objects.filter(user=request.user)
    return render(request, 'content/index.html', {
        'content_': content_
    })

#detail (show)
@login_required
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
class ContentCreate(LoginRequiredMixin, CreateView):
    model = Content
    fields= ['name', 'description', 'seasons']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
#update
class ContentUpdate(LoginRequiredMixin, UpdateView):
    model = Content
    fields = ['name', 'description', 'seasons']
        

#delete
class ContentDelete(LoginRequiredMixin, DeleteView):
    model = Content
    success_url = '/content/'
        

#one to one
#create
@login_required
def add_entry(request, content_id):
    form = EntryForm(request.POST)
    if form.is_valid():
        new_entry = form.save(commit=False)
        new_entry.content_id = content_id
        new_entry.save()
    return redirect('detail', content_id=content_id)

# delete
@login_required
def delete_all_entry(request, content_id):
    entry = Entry.objects.filter(content_id=content_id)
    form = DeleteEntry(request.POST)
    if form.is_valid():
        entry.delete()
    return redirect('detail', content_id=content_id)

# def delete_all_entry(request, content_id):
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
class PlatformList(LoginRequiredMixin, ListView):
    model = Platform

    def platform_list(request):
        platform_ = Platform.objects.filter(user=request.user)
        return render(request, 'main_app/platform_list.html', {
            'platform_': platform_
        })

#detail (show)
class PlatformDetail(LoginRequiredMixin, DetailView):
    model = Platform

#create
class PlatformCreate(LoginRequiredMixin, CreateView):
    model = Platform
    fields = '__all__'

#update
class PlatformUpdate(LoginRequiredMixin, UpdateView):
    model = Platform
    fields = '__all__'

#delete
class PlatformDelete(LoginRequiredMixin, DeleteView):
    model = Platform
    success_url = '/platforms'

#associations
#assoc
@login_required
def assoc_platform(request, content_id, platform_id):
    Content.objects.get(id=content_id).platform.add(platform_id)
    return redirect('detail', content_id=content_id)
    
#unassoc
@login_required
def unassoc_platform(request, content_id, platform_id):
    Content.objects.get(id=content_id).platform.remove(platform_id)
    return redirect('detail', content_id=content_id)    

#photo -aws-
@login_required
def add_photo(request, content_id):
      # photo-file will be the "name" attribute on the <input type="file">
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
      s3 = boto3.client('s3')
      # need a unique "key" for S3 / needs image file extension too
      key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
      print(f"add photo key {photo_file}")
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
        
#signup -auth-

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('content')
        else:
            error_message = 'Invalid sign up - try again'
            
    form = UserCreationForm()
    context = { 'form': form, 'error_message': error_message }
    return render(request, 'registration/signup.html', context)

# delete photo
@login_required
def delete_photo(request, content_id):
      # photo-file will be the "name" attribute on the <input type="file">
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
      s3 = boto3.client('s3')
      # need a unique "key" for S3 / needs image file extension too
      key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
      print(f"the photo key {key}")
      # just in case something goes wrong
      try:
          bucket = os.environ['S3_BUCKET']
          s3.delete_object(photo_file, bucket, key)
          # build the full url string
          url = f"https://{bucket}.{os.environ['S3_BASE_URL']}{key}"
          # we can assign to content_id or content (if you have a content object)
          Photo.objects.delete(url=url, content_id=content_id)
          s3.delete_object(photo_file, bucket, key)
        #   s3.Objects.delete(Bucket=bucket, Key=key, url=url, content_id=content_id)
      except botocore.exceptions.ClientError as error:
            print('An error occurred uploading file to S3')
            # Put your error handling logic here
            raise error
      except botocore.exceptions.ParamValidationError as error:
            raise ValueError('The parameters you provided are incorrect: {}'.format(error))
      except:
          print('An error occurred uploading file to S3')
  return redirect('detail', content_id=content_id)

# def delete_photo(bucket, model, aws_secret, aws_key, content_id):
#     try:
#         aws_key = os.environ['AWS_ACCESS_KEY_ID']
#         aws_secret = os.environ['AWS_SECRET_ACCESS_KEY']
#         s3 = boto3.client(
#             "s3", aws_access_key_id=aws_key, aws_secret_access_key=aws_secret
#         )
#         s3.delete_object(Bucket=bucket, Key=model)
#         return True
#     except Exception as ex:
#         print(str(ex))
#     return redirect('detail', content_id=content_id)

# def delete_photo(request, content_id):
#     aws_key = os.environ['AWS_ACCESS_KEY_ID']
#     aws_secret = os.environ['AWS_SECRET_ACCESS_KEY']
#     photo_file = request.FILES.get('photo-file', None)
#     print(photo_file)
#     try:
#         key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
#         print(f"delete photo key {key}")
#         s3 = boto3.client(
#             "s3", aws_key, aws_secret
#         )
#         bucket = os.environ['S3_BUCKET']
#         url = f"https://{bucket}.{os.environ['S3_BASE_URL']}{key}"
#         s3.delete_object(url=url, content_id=content_id)
#     except Exception as ex:
#         print(str(ex))
#         print("ERROR", ex)
#     return redirect('detail', content_id=content_id)
        