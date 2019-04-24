from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from comments.forms import CommentForm
from django.views.generic import ListView,DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import markdown
# Create your views here.


#def index(request):
 #   post_list = Post.objects.all()
  #  return render(request, 'blog/index.html', context={'post_list': post_list})

class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    # 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 5

def detail(request, pk):

    post = get_object_or_404(Post, pk=pk)
    
    post.increase_views()

    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    # 记得在顶部导入 CommentForm
 
    form = CommentForm()
    # 获取这篇 post 下的全部评论
    comment_list = post.comment_set.all()

    # 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
    context = {'post': post,
               'form': form,
               'comment_list': comment_list
               }
    return render(request, 'blog/detail.html', context=context)




def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

#def category(request, pk):
 #   cate = get_object_or_404(Category, pk=pk)
  #  post_list = Post.objects.filter(category=cate)
   # return render(request, 'blog/index.html', context={'post_list': post_list})

class CategoryView(IndexView):

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)

def listing(request):
    contact_list = Contacts.objects.all()
    paginator = Paginator(contact_list, 25) # 每页显示 25 个联系人

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
    # 如果用户请求的页码号不是整数，显示第一页
        contacts = paginator.page(1)
    except EmptyPage:
    # 如果用户请求的页码号超过了最大页码号，显示最后一页
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'blog/index.html', {'contacts': contacts})

class TagView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)

def video(request):
    return render(request,'blog/video.html')

def about(request):
    return render(request,'blog/about.html')

def coutact(request):
    return render(request,'blog/contact.html')
