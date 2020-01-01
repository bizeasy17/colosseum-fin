from .models import Comment
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _


class CommentForm(ModelForm):
    url = forms.URLField(label=_('网址'), required=False)
    email = forms.EmailField(label=_('电子邮箱'), required=True)
    name = forms.CharField(label=_('姓名'), widget=forms.TextInput(attrs=
                                                              {'value': "", 'size': "30", 'maxlength': "245",
                                                               'aria-required': 'true'}
                                                              ))
    parent_comment_id = forms.IntegerField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Comment
        fields = ['body']
