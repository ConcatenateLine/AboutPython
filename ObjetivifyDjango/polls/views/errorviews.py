from django.http import HttpResponseNotFound
from django.shortcuts import render

def custom_404_view(request, exception):
    try:
        return render(request, 'errors/404.html', status=404)
    except Exception as e:
        return HttpResponseNotFound('404 Not Found', status=404)