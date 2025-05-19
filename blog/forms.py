from django.forms import ModelForm
from . import models


class blogForm(ModelForm):
    class Meta:
        model = models.Blog
        fields = ['title', 'description', 'cover']

class CommentForm(ModelForm):
    class Meta:
        model=models.Comment
        fields = ('text',)


class ReplyForm(ModelForm):
    class Meta:
        model = models.Reply
        fields = ('text',)