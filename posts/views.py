from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

from .models import Post
from .forms import CommentForm


class PostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    paginate_by = 4
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'



@login_required
def post_detail_view(request, pk):
    # Get post object
    post = get_object_or_404(Post, pk=pk)

    # Get post comments
    post_comments = post.comments.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user

            new_comment.save()
            comment_form = CommentForm()

    else:
        comment_form = CommentForm()


    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comments': post_comments,
        'comment_form': comment_form,    
        }
    )

