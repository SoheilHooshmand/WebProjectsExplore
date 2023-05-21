from django.db import models
import uuid
from users.models import Profile
# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length = 200)
    owner = models.ForeignKey(Profile, null = True, blank = True, on_delete = models.SET_NULL)
    image = models.ImageField(null = True, blank = True, default = 'default.jpg')
    descriptions = models.TextField(null = True, blank = True)
    demo_link = models.CharField(max_length = 2000, null = True, blank = True)
    source_link = models.CharField(max_length = 200, null = True, blank = True)
    tags = models.ManyToManyField("Tag", blank = True)
    vote_total = models.IntegerField(default = 0, null = True, blank = True)
    vote_ratio = models.IntegerField(default = 0, null = True, blank = True)
    created = models.DateTimeField(auto_now_add = True)
    id = models.UUIDField(default = uuid.uuid4, unique = True, primary_key = True, editable = False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'name']
        #ordering = ['created']
        # to reverse list use this syntax:
        # ordering = ['-created']
    #This function returns all of the profiles that vote to a specific project
    @property
    def reviewers(self):
        queryset = self.reviews_set.all().values_list('owner__id', flat=True)
        return queryset
    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()
        ratio = (upVotes/totalVotes)*100
        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()


class Review(models.Model):
    VOTE_TYPE = (
        ('up', "Up Vote"),
        ('down', 'Down Vote'),
    )
    owner = models.ForeignKey(Profile, on_delete = models.CASCADE, null = True)
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    body = models.TextField(null = True, blank = True)
    value = models.CharField(max_length = 200, choices = VOTE_TYPE)
    created = models.DateTimeField(auto_now_add = True)
    id = models.UUIDField(default = uuid.uuid4, unique = True, primary_key = True, editable = False)

    class Meta:
        unique_together = [['owner', 'project']]

    def __str__(self):
        return self.value

class Tag(models.Model):
    name = models.CharField(max_length = 200)
    created = models.DateTimeField(auto_now_add = True)
    id = models.UUIDField(default = uuid.uuid4, unique = True, primary_key = True, editable = False)

    def __str__(self):
        return self.name
