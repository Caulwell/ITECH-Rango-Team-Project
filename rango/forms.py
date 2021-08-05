from django import forms
from django.contrib.auth.models import User
from django.forms import fields
from rango.models import LikedPage, Page, Category, UserProfile, Review, Subcategory

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=Category.NAME_MAX_LENGTH, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to privde additional information on the form.
    class Meta:
        #Provide and associated between the ModelForm and a model
        model=Category
        fields=("name",)

class SubcategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=Subcategory.NAME_MAX_LENGTH, help_text="Please enter the subcategory name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to privde additional information on the form.
    class Meta:
        #Provide and associated between the ModelForm and a model
        model=Subcategory
        fields=("name",)

class PageForm(forms.ModelForm):
    NAME = forms.CharField(max_length=Page.NAME_MAX_LENGTH, help_text="Please enter the title of the page.")
    url=forms.URLField(max_length=Page.URL_MAX_LENGTH, help_text="Please enter the URL of the page.")
    views=forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        #Provide and association between the ModelForma and a model
        model = Page

        # What fields do we want to include in our form?
        # This way we dont need every field in the model present.
        # Some fields may allow NULl values; we may not want to include them
        # Here, we are hiding the foreign key
        # We can either exclude the category field from the form
        exclude = ("category",)
        # or specify the fields to inlcude and don't include the category field - fields = ("title", "url", "views")

        def clean(self):
            cleaned_data = self.cleaned_data
            url = cleaned_data.get("url")

            #if url is not empty and doesn't start with "http://", prepend with it
            if url and not url.startswith("http://"):
                url = f"http://{url}"
                cleaned_data["url"] = url
            
            return cleaned_data

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "email", "password",)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("website", "picture")


class ReviewForm(forms.ModelForm):

    Stars = forms.IntegerField(help_text="Give some stars 1-5 integers only")
    BriefDescription = forms.CharField(max_length=Review.BriefDescription_Max_Length, help_text='please give a brief description')
    ReviewText= forms.CharField(max_length=Review.ReviewText_Max_Length, help_text='Please give a longer explanation.')
    class Meta :
        model= Review
        fields = ("Stars","BriefDescription","ReviewText")
        
class URLForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("website",)

class PictureForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("picture",)
class PasswordChangeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ("password", "password")

class LikedPageForm(forms.ModelForm):
    class Meta:
        model = LikedPage
        fields = ("user", "page")
