from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from PIL import Image
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

# from django.db.models.signals import post_delete


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    image = models.ImageField(blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    IMAGE_MAX_SIZE = (400, 400)

    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()

# def delete_image(self, *args, **kwargs):
#     self.image.delete()
#     super(Ticket, self).delete(*args, **kwargs)
#
# def delete(self):
#     image = Ticket.objects.filter(product=self)
#     self.image.delete()
#     super(Ticket, self).delete()

# def _delete_file(path):
#    """ Deletes file from filesystem. """
#    if os.path.isfile(path):
#        os.remove(path)
#
# @receiver(pre_delete, sender=Ticket)
# def delete_file(sender, instance, *args, **kwargs):
#     """ Deletes image  files on `post_delete` """
#     if instance.image:
#         _delete_file(instance.image.path)


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollows(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following')
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followed_by')

    class Meta:
        pass
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs

        unique_together = ('user', 'followed_user', )
