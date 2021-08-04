from django.conf.urls import include
from django.urls import path
from rango import views

app_name = 'rango'

urlpatterns = [
path('', views.index, name='index'),
path('about/', views.about, name='about'),
path("category/<slug:category_name_slug>/", views.show_category, name="show_category"),
path("add_category/", views.add_category, name="add_category"),
path("category/<slug:category_name_slug>/subcategory/<slug:subcategory_name_slug>/", views.show_subcategory, name="show_subcategory"),
path("category/<slug:category_name_slug>/add_subcategory", views.add_subcategory, name="add_subcategory"),
path("category/<slug:category_name_slug>/subcategory/<slug:subcategory_name_slug>/add_page/", views.add_page, name="add_page"),
path("restricted/", views.restricted, name="restricted"),
path("accounts/register/", views.register, name="register"),
path("accounts/login/", views.user_login, name="login"),
path("accounts/logout/", views.user_logout, name="logout"),
path("accounts/password/change", views.change_password, name="change_password"),
]
