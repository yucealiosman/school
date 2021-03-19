from collections import defaultdict

from django.contrib import admin
from django.views.decorators.cache import never_cache


class AdminSite(admin.AdminSite):
    @never_cache
    def index(self, request, extra_context=None):
        """
        Display the main admin index page, which lists all of the installed
        apps that have been registered in this site.
        """

        notifications = request.user.received_notifications.filter(
            is_read=False).select_related("sender")

        not_context = []
        for notification in notifications:
            not_context.append({"sender": notification.sender.first_name,
                                  "text": notification.text})
        extra_context = {"notifications": not_context}

        notifications.update(is_read=True)

        return super().index(request, extra_context=extra_context)
