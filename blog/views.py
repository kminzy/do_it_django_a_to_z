# from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Post, Category, Tag
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin # 로그인 했을 때만 정상적으로 페이지 출력

# Create your views here.


class PostCreate(LoginRequiredMixin, CreateView): 
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    def form_valid(self, form):
        current_user = self.request.user # 웹 사이트의 방문자
        if current_user.is_authenticated: # 로그인 한 상태라면
            form.instance.author = current_user # 새로 생성한 포스트(instance)의 author에 user 담는다
            return super(PostCreate, self).form_valid(form) # 현재 form을 인자로 보내 처리
        else:
            return redirect('/blog/')


class PostList(ListView):
    model = Post
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context


def category_page(request, slug):
    #category = Category.objects.get(slug=slug) # category_page() 함수의 인자로 받은 slug와 동일한 slug를 갖는 카테고리를 불러온다
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(request, 'blog/post_list.html', # PostList 클래스에서 context로 정의했던 부분 직접 정의
                {
                    'post_list': post_list, # (slug=slug)로 필토링한 카테고리만 가져온다
                    'categories': Category.objects.all(), # 카테고리 카드 채워준다
                    'no_category_post_count': Post.objects.filter(category=None).count(), # 미분류 포스트, 개수 알려줌
                    'category': category, # 페이지 타이틀 옆에 카테고리 이름 알려준다
                })


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug) # url에서 인자로 넘어온 slug와 동일한 slug 가진 태그
    post_list = tag.post_set.all()

    return render(request, 'blog/post_list.html',
                  {
                      'post_list': post_list,
                      'tag': tag,
                      'categories': Category.objects.all(),
                      'no_category_post_count': Post.objects.filter(category=None).count(),
                  })


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

# def index(request):
#     posts = Post.objects.all().order_by('-pk')
#
#     return render(request, 'blog/post_list.html', {'posts': posts,})
#
# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)
#
#     return render(request, 'blog/post_detail.html', {'post':post,})


