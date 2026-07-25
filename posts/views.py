from django.shortcuts import render
from posts.models import Post,Category
from django.contrib.auth.decorators import login_required
from posts.forms import PostCreationForm
# Create your views here.

def post_list_view(request):
     try:
          posts =Post.objects.all()

          post_summary_list = []

          for post in posts:
               post_summary_list.append(
                    {
                         "id":post.id,
                    "title":post.title,
                    "content":post.content[:100]
                    }
               )
          return render(
               request=request,
               template_name='post_list.html',
               context={'post_summary':post_summary_list}
          )
     except Exception as e:
          return render(
               request=request,
               template_name='error.html',
               context={'erroe':e}
          )
     

def post_detail_view(request,pk):
     # try:
        post =Post.objects.get(id=pk)
        return render(
               request=request,
               template_name='post_detail.html',
               context={'post':post}
        )
     # except Exception as e:
        return render(
          request=request,
          template_name='error.html',
          context={'error':e}
        )
@login_required
def post_create_view(request):
     try:
         form =PostCreationForm()
         if request.method =="POST":
              form =PostCreationForm(request.POST)
              category_id =request.POST.get('category')
              category =Category.objects.get(id=category_id)
              if form.is_valid():
                   Post.objects.create(
                        title=request.POST.get('title'),
                        content=request.POST.get('title'),
                        category = category,
                        author= request.user
                   )
         return render(
               request=request,
               template_name='post_creation.html',
               context={'form':form}
          ) 
     
     except Exception as e:
          return render(
               request=request,
               template_name='error.html',
               context={'erroe':e}
          )