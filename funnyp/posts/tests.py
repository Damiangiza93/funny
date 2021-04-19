from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post, Category, Comment


User = get_user_model()

class ViewsTestCase(TestCase):
    
    def setUp(self):
        self.category1 = Category.objects.create(name='category1')
        self.user1 = User.objects.create_user('testuser', 'testuser@invalid.com', 'passwordtest')
        self.post1 = Post.objects.create(title='post', content='content', author=self.user1, category=self.category1, image='posts_pics/2/2_post_moska-IMG_20160726_203431.jpg', status='Zaakceptowane')
        

    def test_post_list_view(self):
        response = self.client.get(reverse('blog-home'))
        posts = response.context['posts']
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/home.html')
        self.assertEqual(list(posts), list(Post.objects.all()))
    
    def test_user_post_list_view(self):
        response = self.client.get(reverse('user-posts', args=['testuser']))
        posts = response.context['posts']
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/user_posts.html')
        self.assertEqual(list(posts), list(Post.objects.all()))

    # def test_post_create_view(self):
    #     self.client.login(username=self.user1.username, password='passwordtest')
    #     response = self.client.post(reverse('post-create'), data)
    #     print(data)
    #     self.assertEquals(response.status_code, 200)
        



