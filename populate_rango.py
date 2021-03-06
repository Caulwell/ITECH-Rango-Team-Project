import os
from typing import Text

from django.db.models.query_utils import select_related_descend
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tango_with_django_project.settings")
import random

import django
django.setup()
from rango.models import Category,Page, Review, Subcategory
from django.contrib.sites.models import Site
from tango_with_django_project import settings
from django.contrib.auth.models import User

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

   ## ADD SOME USERS
    users = [
        {"username": "NabeelaFin15", "password": "password"},
        {"username": "jeff_p", "password": "password"},
        {"username": "HelenIsCool", "password": "password"},
        {"username": "Scottyx", "password": "password"},
        {"username": "Reviewman", "password": "password"},
        {"username": "Reviewoman", "password": "password"},
        {"username": "JorjaRayr", "password": "password"},
        {"username": "lolaflores", "password": "password"},
        {"username": "peperodriguez8", "password": "password"},
        {"username": "Greta_atta", "password": "password"},
    ]

    createdUsers = []

    for user in users:
        user = add_user(user["username"], user["password"])
        createdUsers.append(user) 


    testUser = User.objects.get_or_create(username="test_user", password="password")[0]
    
    rust_pages = [
        {'name':'Mozialla Rust Research','url':'https://research.mozilla.org/rust/', "views": 155},
        {'name':'Rust and WebAssembly','url':'https://rustwasm.github.io/book/', "views": 116},
    ]

    rust_designpattern = [
        {'name':'Rust unofficial Design Patterns','url':'https://rust-unofficial.github.io/patterns/', "views": 24},
        {'name':'MIT Design Patterns','url':'http://web.mit.edu/rust-lang_v1.25/arch/amd64_ubuntu1404/share/doc/rust/html/book/second-edition/ch17-03-oo-design-patterns.html', "views": 25},
    ]
    
    rust_learn = [
        {'name':'Rust Official Website','url':'https://www.rust-lang.org/learn', "views": 154},
        {'name':'Rust Docs','url':'https://doc.rust-lang.org/rust-by-example/', "views": 1661},
    ]


    java_pages = [
        {'name':'Java Docs','url':'https://docs.oracle.com/javase/8/docs/api/', "views": 155},
        {'name':'Spring Boot','url':'https://spring.io/projects/spring-boot', "views": 116},
        {'name':'JDCB Tutorial','url':'https://www.tutorialspoint.com/jdbc/index.htm', "views": 118}
    ]

    java_designpattern = [
        {'name':'Javapoint Design Patterns','url':'https://www.javatpoint.com/design-patterns-in-java#:~:text=Java%20Design%20Patterns,Pattern%20Flyweight%20Pattern%20proxy%20Pattern', "views": 14},
        {'name':'Refactoring Guru Design Patterns','url':'https://refactoring.guru/design-patterns/java', "views": 11},
    ]



    learn_python_pages = [
        {"name": "Official Python Tutorial", "url": "http://docs.python.org/3/tutorial/", "views": 5},
        {"name": "How to Think like a Computer Scientist", "url": "http://www.greenteapress.com/thinkpython/", "views": 12},
        {"name": "Learn Python in 10 Minutes", "url": "http://www.korokithakis.net/tutorials/python/", "views": 4}
    ]

    django_pages = [
        {'name':'Official Django Tutorial','url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/', "views": 55},
        {'name':'Django Rocks','url':'http://www.djangorocks.com/', "views": 16},
        {'name':'How to Tango with Django','url':'http://www.tangowithdjango.com/', "views": 18}
    ]



    java_subcats = {'Basics': {'pages': java_pages, "views": 165, "likes":165},
                        'Design Patterns': {'pages': java_designpattern, 'views': 90, 'likes' : 70}}

    rust_subcats = {'Rust': {'pages': rust_pages, "views": 1455, "likes":665},
                'Rust Design Patterns': {'pages': rust_designpattern, 'views': 126, 'likes' : 70},
                'Learn Rust': {'pages': rust_learn , 'views': 666, 'likes' : 555}}

    python_subcats = {'Django': {'pages': django_pages, "views": 55, "likes":65},
        'Learn Python': {'pages': learn_python_pages, 'views': 6, 'likes' : 7}}
    

    other_frameworks = [
        {'name':'Bottle','url':'http://bottlepy.org/docs/dev/', "views": 45}, 
        {'name':'Flask', 'url':'http://flask.pocoo.org', "views": 61} ]

    learning_sites = [
        {'name':'w3schools','url':'https://www.w3schools.com/', "views": 51}, 
        {'name':'geeksforgeeks', 'url':'https://www.geeksforgeeks.org/', "views": 81} ]

    misc_subcats =  {'Other Frameworks': {'pages': other_frameworks, "views": 16, "likes": 21},
                    'Learn': {'pages': learning_sites, 'views': 60, 'likes': 17}}
    


    cats = {'Rust': {'subcats': rust_subcats, "views": 82, "likes": 76},
            'Python': {'subcats': python_subcats, "views": 128, "likes": 64},
            'Misc': {'subcats': misc_subcats, "views": 32, "likes": 16},
            'Java': {'subcats': java_subcats, "views": 62, "likes": 26},
            }

    

    # The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated pages for that category.
    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data["views"], cat_data["likes"], testUser)
        for subcat, subcat_data in cat_data['subcats'].items():
            s = add_subcat(c, subcat, subcat_data["views"], subcat_data["likes"], testUser)
            for page in subcat_data["pages"]:
                p = add_page(s, page['name'], page['url'], page['views'],testUser)
                totalRating = 0
                numReviews = 0
                for user in createdUsers:
                    add_review(p, user)
                    totalRating += 4
                    numReviews += 1
                p.avg_rating = round(totalRating / numReviews, 2)
                p.save()
                
                
                   
                    
                

def add_user(username, password):
    u = User.objects.get_or_create(username=username)[0]
    u.password = password
    u.save()
    return u

def add_review(page, user):
    r = Review.objects.get_or_create(page=page, user=user, rating = 5)[0] # dummy rating needed to create object
    rating = random.randint(1,5)
    if rating == 1:
        title = "Page is awful"
    elif rating == 2:
        title = "Pretty bad page"
    elif rating == 3:
        title = "The page is quite average"
    elif rating == 4:
        title = "I really enjoy using this page"
    elif rating == 5:
        title = "This page is really great!"
    else:
        title = "Unsure what to think of this page"
        
    text=("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent ac nisi sit amet" +
    "sapien consectetur luctus. Aenean at sem id massa interdum egestas ac in lacus. Aliquam erat" +
    "volutpat. Aenean vel erat id justo dictum tempor. Curabitur blandit orci eu orci molestie euismod." + 
    "Maecenas eget ipsum congue, pretium nunc quis, aliquam ante. Aenean non vulputate nisi.")

    r.title = title
    r.text = text
    r.rating = rating
    r.save()
    return r

def add_page(subcat, name, url, views,testUser):
    p = Page.objects.get_or_create(subcategory=subcat, name=name,user=testUser)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name, views, likes, testUser):
    c = Category.objects.get_or_create(name=name, views=views, likes=likes, user=testUser)[0]
    c.save()
    return c

def add_subcat(cat, name, views, likes, testUser):
    s = Subcategory.objects.get_or_create(category=cat, name=name, views=views, likes=likes, user=testUser)[0]
    s.save()
    return s

# STart execution here
if __name__ == "__main__":
    print("Starting Rango population script...")
    populate()
