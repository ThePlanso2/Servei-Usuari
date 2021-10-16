from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight


class User(models.Model):
    num = models.IntegerField(default= 1000,blank=True)
    email = models.TextField(blank=True,max_length = 50)
    password = models.TextField(blank=True)
    nickName = models.TextField(default = '' ,max_length = 50)
    token = models.TextField(default = 'xxx')

    class Meta:
        ordering = ['id']   

