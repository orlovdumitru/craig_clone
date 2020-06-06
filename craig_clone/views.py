import requests
from bs4 import BeautifulSoup
from requests.compat import quote_plus # in case of "used bike" => "used%20bike"
from django.shortcuts import render
from . import models


BASE_CRAIGSLIST_URL = 'https://chicago.craigslist.org/search/sss?query='
BASE_CRAIGSLIST_IMG = 'https://images.craigslist.org/'

def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search) #store search in db

    response = requests.get(f"{BASE_CRAIGSLIST_URL}{quote_plus(search)}")
    # get text out of response
    data = response.text

    # use of BeautifulSoup
    soup = BeautifulSoup(data, features='html.parser')
    
    # find all listings by li class is result-row
    post_listings = soup.find_all('li', {'class': 'result-row'})
    # post_title = post_listings[0].find(class_='result-title').text
    # post_url = post_listings[0].find('a').get('href')
    # post_price = post_listings[0].find(class_='result-price').text
    
    final_postings = []
    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        
        price = 'No price'
        if post.find(class_='result-price').text: # if is has a price
            post_price = post.find(class_='result-price').text
        
        post_image = '/static/images/no_image.jpg'
        if post.find(class_='result-image').get('data-ids'):
            post_image = post.find(class_='result-image').get('data-ids')
            post_image = f"{BASE_CRAIGSLIST_IMG}{(post_image.split(',')[0]).split(':')[1]}_300x300.jpg"


        final_postings.append({
            'post_title': post_title, 
            'post_url': post_url, 
            'post_price': post_price,
            'post_image': post_image
            })
    
    find_items = {'search': search, 'final_postings': final_postings}
    return render(request, 'craig_clone/new_search.html', find_items)