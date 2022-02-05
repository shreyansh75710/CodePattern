from django.db import models
from django.contrib.auth.models import User

class codeSnippet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField(null=False, blank=False)
    solution = models.TextField(null=False, blank=False)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.question

class comment(models.Model):
    codeSnippet = models.ForeignKey(codeSnippet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(null=False, blank=False)

# class questionQuery(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     question = models.TextField(null=False, blank=False)
#     isSolved = models.BooleanField(default=False)
#     solution = models.ForeignKey(codeSnippet, null=True)
#     created = models.DateTimeField(auto_now=True)

#     def __Str__(self):
#         return self.question

class theoryNote(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length = 100)
    link = models.CharField(max_length = 100)
    created = models.DateField(auto_now=True)

    def __Str__(self):
        return self.title