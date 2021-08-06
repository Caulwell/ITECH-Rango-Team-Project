from django.test import TestCase

# Create your tests here.
from django.http import response
from django.test import TestCase
from django.urls import reverse
from rango.models import Category, Subcategory, Page, Review
from django.contrib.auth.models import User


def create_user_object():
    """
    Helper function to create a User object.
    """
    user = User.objects.get_or_create(username='testuser',
                                      first_name='Test',
                                      last_name='User',
                                      email='test@test.com')[0]
    user.set_password('testabc123')
    user.save()

    return user


class CategoryMethodTests(TestCase):
    
    def setUp(self):
        """
        create Category object in database
        """
        Category.objects.get_or_create(user=create_user_object(), name='test', views=-1, likes=-1)
        
    
    def test_ensure_views_are_positive(self):
        """
        Ensures the number of views received for a Category are positive or zero.
        """
        category = Category.objects.get(name='test')

        category.save()
    
        self.assertEqual((category.views >= 0), True)
        

    def test_ensure_likes_are_positive(self):
        """
        Ensures the number of likes received for a Category are positive or zero.
        """
        category = Category.objects.get(name='test')

        category.save()

        self.assertEqual((category.likes >=0), True)
        
        
class SubcategoryMethodTests(TestCase):
     def setUp(self):
        """
        create Category & Subcategory objects in database
        """
        Category.objects.get_or_create(user=create_user_object(), name='test', views=1, likes=0)
        Subcategory.objects.get_or_create(user=create_user_object(), name='test subcategory', category=Category.objects.get(name='test'), views=1, likes=0)
        
     def test_ensure_category_is_correct(self):
        """
        Ensures the Category of a Subcategory  is linked correctly
        """
        subcategory = Subcategory.objects.get(name='test subcategory')
        self.assertEqual(subcategory.category.name, 'test')
        
    
     def test_ensure_views_are_positive(self):
        """
        Ensures the number of views received for a Subcategory are positive or zero.
        """
        subcategory = Subcategory.objects.get(name='test subcategory')
        subcategory.save()
    
        self.assertEqual((subcategory.views >= 0), True)
        

     def test_ensure_likes_are_positive(self):
        """
        Ensures the number of likes received for a Subcategory are positive or zero.
        """
        subcategory = Subcategory.objects.get(name='test subcategory')
        subcategory.save()

        self.assertEqual((subcategory.likes >=0), True)
    
class ReviewMethodTests(TestCase):
    def setUp(self):
        """
        create Category, Subcategory, Page and Review objects in database
        """
        Category.objects.get_or_create(user=create_user_object(), name='test', views=1, likes=0)
        Subcategory.objects.get_or_create(user=create_user_object(), name='test subcategory', category=Category.objects.get(name='test'), views=1, likes=0)
        Page.objects.get_or_create(user=create_user_object(), name='test page', subcategory=Subcategory.objects.get(name='test subcategory'),  avg_rating=2 ,views=1)
        Review.objects.get_or_create(user=create_user_object(), title = "brief description", text="Review", rating=1, page=Page.objects.get(name='test page'), id="007")
        Review.objects.get_or_create(user=create_user_object(), title = "brief description", text="Review", rating=-1, page=Page.objects.get(name='test page'), id="420")
        
    def test_ensure_rating_is_positive(self):
        """
        Ensures the rating of a page is not zero.
        """
        review1 = Review.objects.get(id="007")
        review2 = Review.objects.get(id="420")
        review2.save()
        
        self.assertEqual((review1.rating >=1), True)
        self.assertEqual((review2.rating >=1), True)
        
        
        
    
class IndexViewTests(TestCase):
    def setUp(self):
        """
        create Category objects in database
        """
        Category.objects.get_or_create(user=create_user_object(), name='test', views=1, likes=0)
        Category.objects.get_or_create(user=create_user_object(), name='Rust', views=1, likes=0)
        Category.objects.get_or_create(user=create_user_object(), name='Java', views=1, likes=0)
        Category.objects.get_or_create(user=create_user_object(), name='Python', views=1, likes=0)
        
        """
        create Subcategory object in database
        """
        Subcategory.objects.get_or_create(user=create_user_object(), name='test subcategory', category=Category.objects.get(name='test'), views=1, likes=0)
        
         
        """
        create page objects in database
        """
        Page.objects.get_or_create(user=create_user_object(), name='test page', subcategory=Subcategory.objects.get(name='test subcategory'), views=1)
        Page.objects.get_or_create(user=create_user_object(), name='Rust page', subcategory=Subcategory.objects.get(name='test subcategory'), views=1)
        Page.objects.get_or_create(user=create_user_object(), name='Java page', subcategory=Subcategory.objects.get(name='test subcategory'), views=1)
        Page.objects.get_or_create(user=create_user_object(), name='Python page', subcategory=Subcategory.objects.get(name='test subcategory'), views=1)
   
    
    def add_category(self, title, views=0, likes=0):
        """
        helperfunction to add category
        """
        
        category = Category.objects.get(name=title)
        category.views = views
        category.likes = likes
        
        category.save()
        return category
    
    
    def add_page(self, title, views=0):
        """
        helperfunction to add page
        """
        page = Page.objects.get(name=title)
        page.views = views
        
        page.save()
        return page
       
       
    def test_index_view_with_categories(self):
        """
        Checks whether categories are displayed correctly when present.
        """
        self.add_category('Rust', 1, 1)
        self.add_category('Java', 1, 1)
        self.add_category('Python', 1, 1)
    
        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rust")
        self.assertContains(response, "Java")
        self.assertContains(response, "Python")
        
    def test_index_view_with_pages(self):
        """
        Checks whether pages are displayed correctly when present.
        """
        
        self.add_page('Rust page', 1)
        self.add_page('Java page', 1)
        self.add_page('Python page', 1)
    
        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rust page")
        self.assertContains(response, "Java page")
        self.assertContains(response, "Python page")
        


class IndexViewTestsWithoutCategories(TestCase):
    def test_index_view_with_no_categories(self):
        """
        If no categories exist, the appropriate message should be displayed.
        """
        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no categories present.', html=True)
        self.assertQuerysetEqual(response.context['categories'], [])
            
        
    def test_index_view_with_no_pages(self):
        """
        If no pages exist, the appropriate message should be displayed.
        """
        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no pages present.', html=True)
        self.assertQuerysetEqual(response.context['categories'], [])
                
    



