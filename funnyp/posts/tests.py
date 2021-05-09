from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post, Category, Comment
from pprint import pprint


User = get_user_model()

class ViewsTestCase(TestCase):
    
    def setUp(self):
        self.category1 = Category.objects.create(name='category1')
        self.category2 = Category.objects.create(name='category2')
        self.user1 = User.objects.create_user('testuser', 'testuser@invalid.com', 'passwordtest')
        self.post1 = Post.objects.create(title='post', content='content', author=self.user1, category=self.category1, image='posts_pics/2/2_post_moska-IMG_20160726_203431.jpg', status='Zaakceptowane')
        self.post1.likes.set(self.user1)
        self.post2 = Post.objects.create(title='post2', content='content2', author=self.user1, category=self.category2, image='posts_pics/2/2_post_moska-IMG_20160726_203431.jpg', status='Zaakceptowane')

    def test_post_list_view(self):
        response = self.client.get(reverse('blog-home'))
        posts = response.context['posts']
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/home.html')
        self.assertEqual(list(set(posts)), list(Post.objects.all()))
    
    def test_user_post_list_view(self):
        response = self.client.get(reverse('user-posts', args=['testuser']))
        posts = response.context['posts']
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/user_posts.html')
        self.assertEqual(list(set(posts)), list(Post.objects.all()))

    def test_post_create_view(self):
        self.client.login(username=self.user1.username, password='passwordtest')
        data = {'title':'post', 'content':'content', 'author':self.user1, 'category':self.category1, 'image':'posts_pics/2/2_post_moska-IMG_20160726_203431.jpg', 'status':'Zaakceptowane'}
        response = self.client.post(reverse('post-create'), data, follow=True)
        # pprint(response.context)
        self.assertEquals(response.status_code, 200)

    def test_post_detail_view(self):
        pass

    def test_post_delete_view(self):
        pass

    def test_like_view(self):
        response = self.client.get(reverse('post-detail', args=[self.post1.id]))
        likes = response.context['total_likes']
        self.assertEquals(response.status_code, 200)
        self.assertEqual(likes, self.post1.total_likes())

    def test_unlike_view(self):
        pass

    def test_category_list_view(self):
        response = self.client.get(reverse('category', args=[self.category1.id]))
        posts = response.context['category_posts']
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/category.html')
        self.assertEqual(list(set(posts)), list(Post.objects.filter(category=self.category1)))

    def test_search_bar_view(self):
        response = self.client.get('/search/?search=content')
        posts = response.context['searched_posts']
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/search.html')
        self.assertIn('content', list(posts)[0].content)
        self.assertIn('content', list(posts)[1].content)
    
        



