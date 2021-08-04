from django.http.response import HttpResponse
from rango.forms import CategoryForm, PageForm,  SubcategoryForm, UserProfileForm, UserForm, PasswordChangeForm
from django.shortcuts import redirect, render
from rango.models import Category, Page, Subcategory
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm



def index(request):

    category_list = Category.objects.order_by("-likes")[:5]
    page_list = Page.objects.order_by("-views")[:5]

    context_dict = {}
    context_dict["boldmessage"] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict["categories"] = category_list
    context_dict["pages"] = page_list

    visitor_cookie_handler(request)
    context_dict["visits"] = request.session["visits"]

    response = render(request, "rango/index.html", context=context_dict)
    return response

def about(request):
    context_dict = {}
    visitor_cookie_handler(request)
    context_dict["visits"] = request.session["visits"]
    
    return render(request, 'rango/about.html', context=context_dict)

def show_category(request, category_name_slug):

    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # The .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        # Retrieve all of the associated pages.
        # The filter() will return a list of page objects or an empty list
        subcategories = Subcategory.objects.filter(category=category)
        # Adds our results list to the template context under name pages.
        context_dict["subcategories"] = subcategories
        # We also add the category object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict["category"] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything -
        # the template will display the "no category" message for us.
            context_dict["category"] = None
            context_dict["subcategories"] = None

    return render(request, "rango/category.html", context=context_dict)

@login_required
def add_category(request):
    form = CategoryForm()
    # HTTP POST?
    if request.method == "POST":
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save thew new category to the database
            form.save(commit=True)
            ## Now that the category is saved, we could confirm this.
            # For now, just redirect the user back to the index view
            return redirect("/rango/")
        else:
            # This supplied form contained errors - just print them to the terminal
            print(form.errors)
    # Will handle the bad form, new form, or no form supplied cases - render the form with error messages ( if any)
    return render(request, "rango/add_category.html", {"form": form})

def show_subcategory(request, category_name_slug, subcategory_name_slug):

    context_dict = {}

    try:
       
        # there may be multiple subcategories of the correct name belonging to different parent categories
        # get the correct category based on the slug
        category = Category.objects.get(slug=category_name_slug)

        # filter to get only subcategories belonging to the correct category
        subcategories = Subcategory.objects.filter(category=category)

        subcategory = subcategories.get(slug=subcategory_name_slug)
     
        pages = Page.objects.filter(subcategory=subcategory)

        context_dict['category'] = category
        context_dict["subcategory"] = subcategory
        context_dict["pages"] = pages

    except Subcategory.DoesNotExist:

            context_dict["subcategory"] = None
            context_dict["pages"] = None

    return render(request, "rango/subcategory.html", context=context_dict)


@login_required
def add_subcategory(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect("/rango/")

    
    form = SubcategoryForm()

    if request.method == "POST":
        form = SubcategoryForm(request.POST)

        if form.is_valid():
            if category:
                subcategory = form.save(commit=False)
                subcategory.category = category
                subcategory.views = 0
                subcategory.save()
                return redirect(reverse("rango:show_category", kwargs={"category_name_slug": category_name_slug}))

        else:
            print(form.errors)

    context_dict = {"form": form, "category": category}
    return render(request, "rango/add_subcategory.html", context=context_dict)


@login_required
def add_page(request, category_name_slug, subcategory_name_slug):
    try:

        #subcategory = Subcategory.objects.get(slug=subcategory_name_slug)
        category = Category.objects.get(slug=category_name_slug)

        # filter to get only subcategories belonging to the correct category
        subcategories = Subcategory.objects.filter(category=category)

        subcategory = subcategories.get(slug=subcategory_name_slug)

    except Category.DoesNotExist:
        subcategory = None

    if subcategory is None:
        return redirect("/rango/")

    
    form = PageForm()

    if request.method == "POST":
        form = PageForm(request.POST)

        if form.is_valid():
            if subcategory:
                page = form.save(commit=False)
                page.subcategory = subcategory
                page.views = 0
                page.save()

                return redirect(reverse("rango:show_subcategory", kwargs={"category_name_slug": category_name_slug,
                                                                            "subcategory_name_slug": subcategory_name_slug}))

        else:
            print(form.errors)

    context_dict = {"form": form, "subcategory": subcategory, "category": category}
    return render(request, "rango/add_page.html", context=context_dict)

@login_required
def restricted(request):
    return render(request, "rango/restricted.html")

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html', context={'user_form': user_form,
                                                            'profile_form':profile_form,
                                                            'registered': registered})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your SourceRank account is disabled")
        else:
            print(f"Invalid login details: {username}, {password}")
            return render(request, "rango/login.html", context={
                "invalid": True
            })
    else:
        return render(request, "rango/login.html")

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse("rango:index"))

@login_required
def change_password(request):
    passwordChanged = False

    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            passwordChanged = True
        else:
            print(form.errors)

    else: 
        form = PasswordChangeForm(request.user)

    return render(request, "rango/change_password.html", context={"form": form, "success": passwordChanged})

