from django.shortcuts import render


def index(request):
    context = {}
    return render(request, 'presets/index.html', context)
