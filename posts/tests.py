from datetime import datetime

from django.test import TestCase
from django.test.client import Client
from django.utils.timezone import utc, now as tz_now

from .models import Post


class PostUnitTest(TestCase):
    def test_get_absolute_url(self):
        post = Post(slug='test-post')
        self.assertEqual(post.get_absolute_url(), '/posts/test-post/')

    def test_unicode(self):
        title = "My Test Title"
        post = Post(title=title)
        self.assertEqual(post.__unicode__(), title)


class PostManagerTest(TestCase):
    fixtures = ['test-data.json']

    def test_get_published(self):
        """
        Make sure the posts come back in the right order.
        """
        posts = Post.objects.published()
        now = tz_now()

        # We should have three posts, since the third isn't published until
        # the year 2030.
        self.assertEqual(len(posts), 2)

        # Make sure that, for each post, it's older than the one before it,
        # and that it isn't supposed to be published in the future.
        previous_published_date = datetime(2030, 1, 1).replace(tzinfo=utc)
        for p in posts:

            # The current post's published date should be less than the one
            # before it.
            self.assertLessEqual(p.published, previous_published_date)

            # The published date should be less than the current time as well.
            self.assertLessEqual(p.published, now)

    def test_get_published_by_tag(self):
        """
        Ensure that only tags containing the right tag are returned.
        """
        tag = 'blog'
        num_posts_expected = 1
        posts = Post.objects.published_by_tag(tag)

        # Only one should have matched.
        self.assertEqual(len(posts), num_posts_expected,
                         msg="We got too many posts ({}) when we asked for "
                         "those with the tag {}. There should have only been "
                         "{}.".format(len(posts), tag, num_posts_expected))

        # Make sure that one has the correct tag.
        self.assertIn(tag, [t.slug for t in posts[0].tags.all()])


class PostViewTest(TestCase):
    fixtures = ['test-data.json']

    def setUp(self):
        self.client = Client()

    def test_all_posts_page(self):
        response = self.client.get('/posts/')

        # Make sure the page resolved correctly.
        self.assertEqual(response.status_code, 200)

        # Make sure the content contained the context we'd expect.
        posts = response.context['object_list']
        self.assertEqual(len(posts), 2)
        self.assertEqual(type(posts[0]), Post)

        # Make sure it used the default template.
        self.assertIn('posts/all-posts.html',
                      [t.name for t in response.templates])

        # Make sure the post's title appears in the rendered content.
        self.assertIn(posts[0].title, response.content)

    def test_posts_by_tag_page(self):
        response = self.client.get('/tags/blog/')

        # Make sure the page resolved correctly.
        self.assertEqual(response.status_code, 200)

        # Make sure the content contained the context we'd expect.
        posts = response.context['object_list']
        self.assertEqual(len(posts), 1)
        self.assertEqual(type(posts[0]), Post)

        # Make sure it used the default template.
        self.assertIn('posts/posts-by-tag.html',
                      [t.name for t in response.templates])

        # Make sure the post's title appears in the rendered content.
        self.assertIn(posts[0].title, response.content)

    def test_post_page(self):
        response = self.client.get('/posts/my-first-post/')

        # Make sure the page resolved correctly.
        self.assertEqual(response.status_code, 200)

        # Make sure the content contained the context we'd expect.
        post = response.context['object']
        self.assertEqual(type(post), Post)
        self.assertEqual(post.title, "My First Post")

        # Make sure it used the default template.
        self.assertIn('posts/post.html', [t.name for t in response.templates])
