from django import forms
from rango.models import Page, Category

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to privde additional information on the form.
    class Meta:
        #Provide and associated between the ModelForm and a model
        model=Category
        fields=("name",)


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    url=forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
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