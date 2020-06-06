import requests
from django.shortcuts import render
from bs4 import BeautifulSoup

def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    find_items = {'search': search}
    return render(request, 'craig_clone/new_search.html', find_items)