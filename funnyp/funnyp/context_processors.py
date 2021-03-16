from django.conf import settings
from django.shortcuts import get_object_or_404
from posts.models import Post
from users.models import User
from django.db.models import Count

def popularposts(request):
    return{
        'popularposts': Post.objects.filter(status='Zaakceptowane').annotate(like_count=Count('likes')-Count('unlikes')).order_by('-like_count')
    }

def userframe(request, *args, **kwargs):
    try:
        user = get_object_or_404(User, username=request.user)
        userposts = Post.objects.filter(author=user, status='Zaakceptowane').aggregate(total_likes=Count('likes')-Count('unlikes'))['total_likes'] or 0

        return {
            'userlikes': userposts,
            'userimage': user.profile.image,
            'current_user': user
        } 
    except: 
        return {}