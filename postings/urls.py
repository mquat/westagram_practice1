from django.urls import path

from .views import PostingView, CommentsView

urlpatterns = [
    path('/post', PostingView.as_view()),
    path('/comment', CommentsView.as_view())
]