from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('note/<int:pk>/', views.noteView, name='noteView'),
    path('code/<int:pk>/', views.codeView, name='codeView'),
    path('codeCreate/', views.codeCreate, name='codeCreate'),
    path('codeUpdate/<int:pk>/', views.codeUpdate, name='codeUpdate'),
    path('codeDelete/<int:pk>/', views.codeDelete, name='codeDelete'),
    path('deleteComment/<int:pk>/', views.deleteComment, name="deleteComment"),
    path('feedback/', views.feedback, name='feedback'),
]
