from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

CustomUser = get_user_model()
# Create your models here.
class Story(models.Model):
    INTERVIEW = 'Interview'
    PERSONAL_GROWTH = 'Personal Growth'
    CULTURE = 'Culture'
    TAG_CHOICES = [
        (INTERVIEW, 'Interview'),
        (PERSONAL_GROWTH, 'Personal Growth'),
        (CULTURE, 'Culture'),
    ]
    story_id = models.AutoField(primary_key=True)
    is_currently_featured = models.BooleanField(default=False, null =True, blank =True)
    is_approved = models.BooleanField(default = False)
    is_anonymous = models.BooleanField(default = False)
    featured_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    topic = models.CharField(max_length = 100)
    author = models.ForeignKey(CustomUser, on_delete = models.DO_NOTHING, null = True, blank = True)
    image = models.ImageField(upload_to = 'story_images')
    short_description = models.CharField(max_length = 255)
    body = models.TextField()
    tags = models.CharField(max_length=50, choices=TAG_CHOICES, blank=True, null = True)

    @classmethod
    def get_latest_featured_story(cls):
        return cls.objects.filter(is_currently_featured=True).order_by('-featured_date').first()

    @classmethod
    def get_previous_featured_stories(cls):
        return cls.objects.filter(is_currently_featured=False, featured_date__isnull=False).order_by('-featured_date')

    def save(self, *args, **kwargs):
        if self.is_currently_featured:
            # Check if there is a currently featured story, if so, set it to not featured
            previous_featured = Story.get_latest_featured_story()
            if previous_featured:
                previous_featured.is_currently_featured = False
                previous_featured.save()
            # Set the new story as the currently featured story
            self.is_currently_featured = True
            self.featured_date = timezone.now()

        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Stories"
        


class Comment(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser,null=True, on_delete=models.SET_NULL)
    comment_body = models.TextField()
    reply_to = models.ForeignKey("self", null=True, blank=True, on_delete = models.CASCADE)

    def likes_count(self):
        self.like.all().count()

class Like(models.Model):
    comment = models.OneToOneField('Comment', on_delete=models.CASCADE, related_name = 'like')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null = True, blank = True)

    class Meta:
        unique_together = ('comment', 'user')