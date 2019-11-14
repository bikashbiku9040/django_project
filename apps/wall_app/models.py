"""import"""
from __future__ import unicode_literals
from datetime import timedelta
from django.utils import timezone
from django.db import models
from apps.login_app.models import User


class MessageManager(models.Manager):
    """Message Manager Class"""

    def create_message(self, post_data, user_id):
        """Create Message"""
        user = User.objects.get(id=user_id)
        Message.objects.create(user=user, content=post_data['content'])
        return

    def remove_message(self, message_id):
        """Remove Message"""
        message = Message.objects.get(id=message_id)
        message.delete()
        return

    def check_time(self):
        """Check Message Time to determine if it is created more than 30 minutes."""
        time_check = {
            "True": [],
            "False": []
        }
        messages = Message.objects.all()
        check_time = timezone.now() - timedelta(minutes=30)
        for message in messages:
            if message.created_at > check_time:
                time_check["True"].append(message.id)
            else:
                time_check["False"].append(message.id)
        return time_check


class Message(models.Model):
    """Message class"""
    # id
    user = models.ForeignKey(User, related_name="messages")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()


class CommentManager(models.Manager):
    """Comment Manager Class"""

    def create_comment(self, post_data, user_id):
        """Create Comment"""
        user = User.objects.get(id=user_id)
        message = Message.objects.get(id=post_data['message_id'])
        Comment.objects.create(user=user, message=message, content=post_data['content'])
        return

    def remove_comment(self, comment_id):
        """Remove Comment"""
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return

    def check_time(self):
        """Check Comment Time to determine if it is created more than 30 minutes."""
        time_check = {
            "True": []
        }
        comments = Comment.objects.all()
        check_time = timezone.now() - timedelta(minutes=30)
        for comment in comments:
            if comment.created_at > check_time:
                time_check["True"].append(comment.id)
        return time_check


class Comment(models.Model):
    """Comment class"""
    # id
    user = models.ForeignKey(User, related_name="comments")
    message = models.ForeignKey(Message, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()
