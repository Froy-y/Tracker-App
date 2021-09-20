# Tracker-App
Created an app that helps you track your favorite Tv Shows!

## Technologies Used
- HTML, CSS, Materialize, Python, Django, PostgresQL

## Code Snippet
-These delete buttons TOOK ME OUT!!
``` Python
#DELETE_PHOTO INSTANCE
def delete_photo(bucket, model, aws_secret, aws_key, content_id):
    try:
        aws_key = os.environ['AWS_ACCESS_KEY_ID']
        aws_secret = os.environ['AWS_SECRET_ACCESS_KEY']
        s3 = boto3.client(
            "s3", aws_access_key_id=aws_key, aws_secret_access_key=aws_secret
        )
        s3.delete_object(Bucket=bucket, Key=model)
        return True
    except Exception as ex:
        print(str(ex))
    return redirect('detail', content_id=content_id)

def delete_photo(request, content_id):
    aws_key = os.environ['AWS_ACCESS_KEY_ID']
    aws_secret = os.environ['AWS_SECRET_ACCESS_KEY']
    photo_file = request.FILES.get('photo-file', None)
    print(photo_file)
    try:
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        print(f"delete photo key {key}")
        s3 = boto3.client(
            "s3", aws_key, aws_secret
        )
        bucket = os.environ['S3_BUCKET']
        url = f"https://{bucket}.{os.environ['S3_BASE_URL']}{key}"
        s3.delete_object(url=url, content_id=content_id)
    except Exception as ex:
        print(str(ex))
        print("ERROR", ex)
    return redirect('detail', content_id=content_id)

#DELETE ENTRY INSTANCE
def delete_all_entry(request, content_id):
    entry = get_object_or_404(Entry, content_id=content_id)
    if request.method == "POST":
        form = DeleteEntry(request.POST, instance=entry)
        if form.is_valid:
            entry.delete()
            return redirect('detail')
    else:
        form = DeleteEntry(instance=entry)
    return render(request, 'detail', {
        'form': form,
        'entry': entry
    })
```

## Stretch Goals For Later:
- DELETE BUTTONS (hard)
- Edit Entries (medium)
- Edit Photos (hard - this seems impoosible)
- User Profile (easy)
- using tv show API to auto generate show lists and platform list (APIS HARD HARD HARD)
