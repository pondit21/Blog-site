from django.shortcuts import render
from posts.models import Post,Category
from django.contrib.auth.decorators import login_required
from posts.forms import PostCreationForm
from django.db.models import Q,Count
# Create your views here.

def post_list_view(request):
     try:
          query = request.GET.get('query','')
          category = request.GET.get('category_id','')
          status = request.GET.get('status','')
         
          posts =Post.objects.select_related('category','author')

# search ar jono
          if query:
               posts =posts.filter(
                 Q(title__icontains =query) |
                 Q(content__icontains =query) |
                 Q(author__username__icontains = query)
                )
# filter ar jono
          if category:
               posts=posts.filter(category__id=category)
          if status:
               posts=posts.filter(status=status)  

          post_summary_list = []

          for post in posts:
               post_summary_list.append(
                    {
                         "id":post.id,
                    "title":post.title,
                    "content":post.content[:100],
                    "category":post.category,
                    "created_at":post.created_at 
                    }
               )
          my_total = None
          my_categories =None
          if request.user.is_authenticated:
               my_total =Post.objects.filter(author=request.user).aggregate(
                    total = Count('id')
               )

               my_categories=Category.objects.annotate(post_count =Count('posts'))
               

          return render(
               request=request,
               template_name='post_list.html',
               context={
                    'post_summary':post_summary_list,
                    'category':Category.objects.all(),
                    'status_choices':Post.STATUS_CHOICES,
                    'query':query,
                    'selected_category':category,
                    'selected_status':status,
                    'my_total':my_total,
                    'my_categories':my_categories,
                    
                    }
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