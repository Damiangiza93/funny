from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import (ListView, DetailView, CreateView,
                                UpdateView, DeleteView, FormView)
from django.views.generic.edit import FormMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .models import Post, Category, Comment
from .forms import PostCreateForm, CommentForm


class PostListView(ListView):
    model = Post
    template_name = 'posts/home.html'
    context_object_name = 'posts'
    paginate_by = 15

    def get_queryset(self):
        return Post.objects.filter(status='Zaakceptowane').order_by('-date_posted')

class UserPostListView(ListView):
    model = Post
    template_name = 'posts/user_posts.html' 
    context_object_name = 'posts'
    paginate_by = 15
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user, status='Zaakceptowane').order_by('-date_posted')

class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    success_message = "Twój post został utworzony i oczekuje na akceptację"

    def form_valid(self, form):
        form.instance.author = self.request.user
        try:
            form.instance.image = self.request.FILES.get("image_id")
            return super().form_valid(form)
        except:
            return super().form_invalid(form)

class PostDetailView(FormMixin, DetailView):
    model = Post
    form_class = CommentForm

    def get_object(self):
        obj = super().get_object()
        if obj.status == 'Zaakceptowane':
            obj.view_count += 1
            obj.save()
        return obj

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        
        total_likes = stuff.total_likes()
        total_unlikes = stuff.total_unlikes()

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        
        unliked = False
        if stuff.unlikes.filter(id=self.request.user.id).exists():
            unliked = True

        context["total_likes"]  = total_likes - total_unlikes
        context["liked"]        = liked
        context["unliked"]      = unliked
        context["comment_form"] = self.get_form()
        context["comments"]     = self.object.comments.filter()
        context["views_count"]  = self.object.view_count

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.post = self.object
        form.instance.author = self.request.user

        try:
            parent_id = self.request.POST.get("parent_id")
        except:
            parent_id = None
        parent_obj = None
        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists():
                parent_obj = parent_qs.first()
        form.instance.parent = parent_obj
        form.save()
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'category', 'content', 'zajawka']
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user.is_superuser:
            return True
        return False
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    
    def test_func(self):
        post = self.get_object()
        if self.request.user.is_superuser:
            return True
        return False

def LikeView(request, pk):
    post = Post.objects.get(id=pk)
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    post.unlikes.remove(request.user)
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))

def UnlikeView(request, pk):
    post = Post.objects.get(id=pk)
    unliked = False
    if post.unlikes.filter(id=request.user.id).exists():
        post.unlikes.remove(request.user)
        unliked = False
    else:
        post.unlikes.add(request.user)
        unliked = True
    post.likes.remove(request.user)
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))

# def CategoryView(request, categories):
#     category_posts = Post.objects.filter(category=categories, status='Zaakceptowane').order_by('-date_posted')
#     return render(request, 'posts/category.html', {'categories':categories, 'category_posts':category_posts})

class CategoryListView(ListView):
    model = Post
    template_name = 'posts/category.html'
    context_object_name = 'category_posts'
    paginate_by = 15

    def get_queryset(self, **kwargs):
        return Post.objects.filter(category=self.kwargs['categories'] ,status='Zaakceptowane').order_by('-date_posted')

# def SearchBarView(request):
#     if request.method == 'GET':
#         search = request.GET.get('search')
#         posts = Post.objects.filter(
#                             Q(title__icontains=search) |
#                             Q(content__icontains=search), status='Zaakceptowane').order_by('-date_posted').distinct()
#         paginator = Paginator(posts, 2)
#         page_number = request.GET.get('page', num)
#         posts = paginator.page(page_number)
#         page_obj = paginator.get_page(page_number)
#         return render(request, 'posts/search.html', {'searched_posts': posts, 'page_obj': page_obj})

class SearchBarView(ListView):
    model = Post
    template_name = 'posts/search.html'
    context_object_name = 'searched_posts'
    paginate_by = 15

    def get_queryset(self):
        search = self.request.GET['search']
        return Post.objects.filter(
                            Q(title__icontains=search) |
                            Q(content__icontains=search), status='Zaakceptowane').order_by('-date_posted').distinct()