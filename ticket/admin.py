from django.contrib import admin
from . import models

# Register your models here.
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title','user','description')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('headline','get_title','user')

    @admin.display(ordering='ticket__title', description='Titre du ticket')
    def get_title(self, Review):
        return Review.ticket.title

class UFAdmin(admin.ModelAdmin):
    list_display = ('user', 'followed_user')


admin.site.register(models.Ticket, TicketAdmin)
admin.site.register(models.Review, ReviewAdmin)
admin.site.register(models.UserFollows, UFAdmin)