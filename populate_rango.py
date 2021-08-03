import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tango_with_django_project.settings")

import django
django.setup()
from rango.models import Category,Page
from django.contrib.sites.models import Site
from tango_with_django_project import settings

from allauth.socialaccount.models import SocialApp

def populate():

    # Auto set up google oAuth settings
    CLIENT_ID="271337839963-5tjqabnae2nsu7tuvvr7i1024ru1e3u4.apps.googleusercontent.com"
    SECRET="IqPFhlg-flEat7bdIXI8CPna"

    one = Site.objects.get_or_create(domain="127.0.0.1:8000", name="127.0.0.1:8000")[0]
    one.save()

    app = SocialApp.objects.get_or_create(provider="google", name="SourceRank")[0]
    app.client_id=CLIENT_ID
    app.secret=SECRET

    app.sites.set({Site.objects.all()[0]})

    settings.SITE_ID = Site.objects.all()[0].id

    app.save()

    python_pages = [
        {"title": "Official Python Tutorial", "url": "http://docs.python.org/3/tutorial/", "views": 5},
        {"title": "How to Think like a Computer Scientist", "url": "http://www.greenteapress.com/thinkpython/", "views": 12},
        {"title": "Learn Python in 10 Minutes", "url": "http://www.korokithakis.net/tutorials/python/", "views": 4}
    ]

    django_pages = [
        {'title':'Official Django Tutorial','url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/', "views": 55},
        {'title':'Django Rocks','url':'http://www.djangorocks.com/', "views": 16},
        {'title':'How to Tango with Django','url':'http://www.tangowithdjango.com/', "views": 18}
    ]

    other_pages = [
        {'title':'Bottle','url':'http://bottlepy.org/docs/dev/', "views": 45}, 
        {'title':'Flask', 'url':'http://flask.pocoo.org', "views": 61} ]

    cats = {'Python': {'pages': python_pages, "views": 128, "likes": 64},
            'Django': {'pages': django_pages, "views": 64, "likes": 32},
            'Other Frameworks': {'pages': other_pages, "views": 32, "likes": 16} }

    # The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated pages for that category.
    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data["views"], cat_data["likes"])
        for p in cat_data['pages']:
            add_page(c, p["title"], p["url"], p["views"])

    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'-{c}: {p}')


def add_page(cat, title, url, views):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name, views=views, likes=likes)[0]
    c.save()
    return c

# STart execution here
if __name__ == "__main__":
    print("Starting Rango population script...")
    populate()



