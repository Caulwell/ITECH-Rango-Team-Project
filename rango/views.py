from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.shortcuts import redirect, render
from django.http import HttpResponse
from rango.models import Category, Page
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by the number of likes in descending order.
    # Retrieve the top 5 only -- or all if less than 5.
    # Place the list in our context_dict dictionary (with our boldmessage!)
    # that will be passed to the template engine.

    category_list = Category.objects.order_by("-likes")[:5]
    page_list = Page.objects.order_by("-views")[:5]
    context_dict = {}
    context_dict["boldmessage"] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict["categories"] = category_list
    context_dict["pages"] = page_list

    return render(request, 'rango/index.html', context =context_dict)

def about(request):
    return render(request, 'rango/about.html')

def show_category(request, category_name_slug):

    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # The .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        # Retrieve all of the associated pages.
        # The filter() will return a list of page objects or an empty list
        pages = Page.objects.filter(category=category)
        # Adds our results list to the template context under name pages.
        context_dict["pages"] = pages
        # We also add the category object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict["category"] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything -
        # the template will display the "no category" message for us.
            context_dict["category"] = None
            context_dict["pages"] = None

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

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect("/rango/")

    
    form = PageForm()

    if request.method == "POST":
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse("rango:show_category", kwargs={"category_name_slug": category_name_slug}))

        else:
            print(form.errors)

    context_dict = {"form": form, "category": category}
    return render(request, "rango/add_page.html", context=context_dict)

def register(request):
    # a boolean value for telling the template whether the registration was successful,
    # Set to false initially, code changes value to true when registration succeeds

    registered = False

    # if a HTTP POST, interested in processing form data.
    if request.method == "POST":
        ## attempt to grab information from the raw form information. Note - we make use of both UserForm and UserProfileForm
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # if the two forms are valid..
        if user_form.is_valid() and profile_form.is_valid():
            # save the user's form data to the database
            user = user_form.save()

            # Now we hash the password with the set_password method
            # Once hashed, we can update the user object
            user.set_password(user.password)
            user.save()

            ## Now sort the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False. this delays saving the model until we're ready to avoid integrity problems
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile mode
            if "picture" in request.FILES:
                profile.picture = request.FILES["picture"]

            # Now we save the UserProfile model instance
            profile.save()

            # Update the variable to indicate that the template registration was successful
            registered = True

        else:
            # Invalid form or forms - mistakes or something else - print problems to terminal
            print(user_form.errors, profile_form.errors)

    else:
        # Not HTTP POST - so we render our form using two ModelForm instances - blank, reading for user input
        user_form = UserForm()
        profile_form = UserProfileForm()


    # render the template depending on the context
    return render(request, "rango/register.html", context = {"user_form": user_form,
                                                            "profile_form": profile_form,
                                                            "registered": registered})

def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information
    if request.method == "POST":
        # Gather the username and password provided by the user. Obtained from the login form.
        # We use request.POST.get(<variable>) as opposed to request.POST['<variable>'] 
        # because the former returns None if the value does not exist while latter will reaise a KeyError exception

        username = request.POST.get("username")
        password = request.POST.get("password")

        # Use Django#s machinery to see if the username/password combination is valid - User object returned if it is
        user = authenticate(username=username, password=password)


        # If we have a User object, the details are correct.
        # If None, no user with matching credentials was found
        if user:
            # Is the account active? It could have been disabled
            if user.is_active:
                # If the account is valid and active, we can log the user in. Send back to homepage
                login(request, user)
                return redirect(reverse("rango:index"))
            else:
                # Inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details provided
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invlid login details supplied.")
    else:
        ## Request is not a HTTP Post, so display login form - likely GET
        return render(request, "rango/login.html")


@login_required
def restricted(request):
    return render(request, "rango/restricted.html")

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out
    logout(request)
    # Take the user back to the homepage
    return redirect(reverse("rango:index"))