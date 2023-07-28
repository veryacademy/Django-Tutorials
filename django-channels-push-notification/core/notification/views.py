from django.shortcuts import render

# Create your views here.

def notification_page_view(request):
    return render(request, "notification_page.html")