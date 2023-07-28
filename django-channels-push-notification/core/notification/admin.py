from django.contrib import admin
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.urls import path

from django import forms
from django.http import HttpResponseRedirect
from .models import Notification

class SendNoficiationForm(forms.Form):
    message = forms.CharField(label="Notification Message", max_length=200)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    add_form_template = "admin/custom_add_form.html"

    def add_view(self, request, form_url="", extra_context=None):
        if request.method == "POST":
            form = SendNoficiationForm(request.POST)
            if form.is_valid():
                message = form.cleaned_data["message"]

                notification = Notification.objects.create(message=message)

                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    "notifications",
                    {
                        "type": "send_notification",
                        "message": message
                    }
                )

                return HttpResponseRedirect("../{}/".format(notification.pk))
        else:
            form = SendNoficiationForm()

        context = self.get_changeform_initial_data(request)
        context["form"] = form
        return super().add_view(request, form_url, extra_context=context)
    
    def get_urls(self):
        urls = super().get_urls()
        custom_url = [
            path("send-notification/", self.admin_site.admin_view(self.add_view), name="send-notification"),
        ]
        return custom_url + urls