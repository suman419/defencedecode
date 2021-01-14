
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
from embed_video.fields import EmbedVideoField


class Category(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

class Post(models.Model):
    category = models.ForeignKey(Category,related_name='category',on_delete=models.CASCADE)
    STATUS_CHOICES=(
                   ('draft','Draft'),
                   ('published','Published')
                   )
    title=models.CharField(max_length=256)
    slug=models.SlugField(max_length=264,unique_for_date='publish')
    user=models.ForeignKey(User,related_name='defence_posts',on_delete=models.CASCADE)
    body=models.TextField()
    post_likes=models.ManyToManyField(User,related_name='likes',blank=True)
    likes = models.PositiveIntegerField(default = 0)
    image = models.ImageField(default='default.jpg',upload_to='pics')
    publish=models.DateTimeField(default=timezone.now)
    post_views=models.IntegerField(default=0)
    #hit_count_generic = GenericRelation(HitCount, object_id_field='object_p',related_query_name='hit_count_generic_relation')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    objects=CustomManager()
    tags=TaggableManager()

    class Meta:
        ordering=('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self, *args,**kwargs):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def total_likes(self):
        return self.post_likes.count()

class VideoItem(models.Model):
    video = EmbedVideoField()  # same like models.URLField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.post.title

#model related to comments section
class Comment(models.Model):
    post=models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE,)
    name=models.CharField(max_length=64)
    reply=models.ForeignKey('Comment',null=True,related_name="replies",on_delete=models.CASCADE,)
    email=models.EmailField()
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)

    class Meta:
        ordering=('-created',)

    def __str__(self):
        return 'Commented By {} on {}'.format(self.name,self.post)

class AboutCompany(models.Model):
    company_name=models.CharField(max_length=256)
    company_email=models.EmailField()
    image = models.ImageField(default='default.jpg',upload_to='company')
    mobile=models.IntegerField()
    address = models.CharField(max_length=256)
    details=models.TextField()
    created = models.DateField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.company_name

class Contact(models.Model):
    name=models.CharField(max_length=256)
    email=models.EmailField()
    phone=models.IntegerField(blank=True)
    address = models.CharField(max_length=256, blank=True)
    body=models.TextField(blank=True)

    def __str__(self):
        return self.name