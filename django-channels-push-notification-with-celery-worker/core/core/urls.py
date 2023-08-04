from django.contrib import admin
from django.urls import path
from notification import views
from notification.consumers import NotificationConsumer
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.notification_page_view, name="notification_page")
]

websocket_urlpatterns = [
    path("ws/notifications/", NotificationConsumer.as_asgi())
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
