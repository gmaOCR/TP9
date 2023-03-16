import authentication.views
import ticket.views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView)
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True),
         name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', PasswordChangeView.as_view(
        template_name='authentication/password_change_form.html'),
         name='password_change'
         ),
    path('change-password-done/', PasswordChangeDoneView.as_view(
        template_name='authentication/password_change_done.html'),
         name='password_change_done'
         ),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('ticket/my_posts/', ticket.views.my_posts, name='my_posts'),
    path('ticket/create/', ticket.views.create_ticket,
         name='create_ticket'),
    path('ticket/<int:ticket_id>/edit', ticket.views.edit_ticket, name='edit_ticket'),
    path('ticket_and_review/create/', ticket.views.create_review_and_ticket, name='create_ticket_and_review'),
    path('review/<int:review_id>/edit', ticket.views.edit_review, name='edit_review'),
    path('ticket/<int:ticket_id>/review/create/', ticket.views.create_review, name='create_review'),
    path('followed-users/', ticket.views.follow_index, name='followed_users'),
    path('followed-users/<int:user_id>/unfollow', ticket.views.unfollow, name='unfollow_user'),
    path('feed/', ticket.views.feed, name='feed'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
