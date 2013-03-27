from django.views.generic import DetailView, ListView

from .models import Post


class PostListView(ListView):
    def get_queryset(self):
        """
        List only published pages, optionally by a tag in the URL.
        """
        queryset = None

        tag_slug = self.kwargs.get('tag_slug', None)
        # If 'tag_slug' was passed, use that to filter the list of posts.
        if tag_slug is not None:
            queryset = Post.objects.published_by_tag(tag_slug)
        # Otherwise, return all of the published posts.
        else:
            queryset = Post.objects.published()

        return queryset
all_posts = PostListView.as_view(template_name='posts/all-posts.html')
posts_by_tag = PostListView.as_view(template_name='posts/posts-by-tag.html')


class PostView(DetailView):
    queryset = Post.objects.published()
post = PostView.as_view(template_name='posts/post.html')
