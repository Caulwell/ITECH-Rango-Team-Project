from django.db.models.aggregates import Avg
from rango.models import Category, Page, Subcategory, UserProfile, LikedPage, Review
from django.urls import reverse
from django.http.response import HttpResponse
from rango.forms import CategoryForm, PageForm, SubcategoryForm, UserProfileForm, UserForm, PasswordChangeForm, URLForm, PictureForm, ReviewForm
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from datetime import datetime


def index(request):

    category_list = Category.objects.order_by("-likes")[:5]
    page_list1 = Page.objects.order_by("-views")[:3]
    page_list2 = Page.objects.order_by("-views")[3:6]
    review_list1 = Review.objects.order_by("-datetime")[:3]
    review_list2 = Review.objects.order_by("-datetime")[3:6]



    context_dict = {}
    context_dict["reviews1"] = review_list1
    context_dict["reviews2"] = review_list2
    context_dict["categories"] = category_list
    context_dict["pages1"] = page_list1
    context_dict["pages2"] = page_list2

    visitor_cookie_handler(request)
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
        category = Category.objects.get(slug=category_name_slug)
        subcategories = Subcategory.objects.filter(category=category)
        context_dict["subcategories"] = subcategories
        context_dict["category"] = category
    except Category.DoesNotExist:
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
            category = form.save(commit=False)
            category.user = request.user
            category.save()
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
                subcategory.user = request.user
                subcategory.save()
                return redirect(reverse("rango:show_category", kwargs={"category_name_slug": category_name_slug}))

        else:
            print(form.errors)

    context_dict = {"form": form, "category": category}
    return render(request, "rango/add_subcategory.html", context=context_dict)



def show_page(request, page_name_slug, category_name_slug, subcategory_name_slug):

    context_dict ={}
    userReviewed = False

    ## GET PAGE
    try:
        page=Page.objects.get(slug=page_name_slug)
        page.views += 1
        page.save()
    except Page.DoesNotExist:
        return HttpResponse("Page does not exist")

    ## GET ALL REVIEWS FOR THIS PAGE AND THE COUNT TOTAL THE COUNT OF REVIEWS FOR THIS PAGE.
    try:
        page_reviews = Review.objects.filter(page=page)
        page_reviews_count = Review.objects.filter(page=page).count()  
    except Review.DoesNotExist:
        page_reviews = None
        page_reviews_count=0


    ## FIND OUT IF CURRENT USER HAS REVIEWED THIS PAGE
    for review in page_reviews:
      if review.user == request.user:
          userReviewed=True
    
    ## determine if user has liked the page
    
    if request.user.is_authenticated and LikedPage.objects.filter(user=request.user, page=page).exists():
        like_status = True
    else:
        like_status = False


    ## GET AVERAGE OF THE REVIEW RATINGS
    Review_Stars_Sum = 0
    i = 0
    for review in page_reviews:
        Review_Stars_Sum += review.rating 
        i+=1
    if i>0 :
        Review_average = Review_Stars_Sum/i
    else: Review_average=0
    Review_average = round(Review_average,1)

    #Review_average= Review.objects.filter(Page=Page.objects.get(slug=page_name_slug)).aggregate(Avg(Stars))

    context_dict ["userReviewed"]=userReviewed
    context_dict ["Review_average"]=Review_average
    context_dict ["form"]=ReviewForm()
    context_dict["page"] = page
    context_dict["Reviews"]=page_reviews
    context_dict["like_status"]=like_status
    context_dict["page_reviews_count"]= page_reviews_count

    print(request)
    if request.method == "POST":

        if 'unlike' in request.POST:
            LikedPage.objects.filter(user=request.user, page=page).delete()
            return redirect(reverse("rango:show_page", kwargs={"category_name_slug": category_name_slug,
                                                            "subcategory_name_slug": subcategory_name_slug,
                                                            "page_name_slug": page_name_slug}))
        else:
            LikedPage.objects.get_or_create(user=request.user, page=page)[0].save()
            return redirect(reverse("rango:show_page", kwargs={"category_name_slug": category_name_slug,
                                                            "subcategory_name_slug": subcategory_name_slug,
                                                            "page_name_slug": page_name_slug}))

    else:
        print("not post")
    return render (request, "rango/page.html", context_dict)


def add_Review (request,page_name_slug):
    

    page= Page.objects.get(slug=page_name_slug)
    
    form=ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.page=page
        review.user=request.user
        review.save()
    
    return show_page(request, page_name_slug, page.subcategory.category.slug, page.subcategory.slug)





@login_required
def add_page(request, category_name_slug, subcategory_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
        print("cat slug")
        print(category_name_slug)
        print("subcat slug")
        print(subcategory_name_slug)
        subcategory = Subcategory.objects.get(slug=subcategory_name_slug)
    except Category.DoesNotExist:
        category = None
        subcategory = None

    if category is None or subcategory is None:
        return redirect("/rango/")

    form = PageForm()

    if request.method == "POST":
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.subcategory = subcategory
                page.views = 0
                page.save()

                return redirect(reverse("rango:show_subcategory", kwargs={"category_name_slug": category_name_slug,
                                                                        "subcategory_name_slug": subcategory_name_slug}))

        else:
            print(form.errors)

    context_dict = {"form": form, "category": category, "subcategory": subcategory}
    return render(request, "rango/add_page.html", context=context_dict)

def visitor_cookie_handler(request):
    
    visits = int(get_server_side_cookie(request, "visits", "1"))
    last_visit_cookie = get_server_side_cookie(request, "last_visit", str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], "%Y-%m-%d %H:%M:%S")

    if(datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session["last_visit"] = str(datetime.now())
    else:
        request.session["last_visit"] = last_visit_cookie

    request.session["visits"] = visits

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

@login_required
def profile(request):

    print(request.user)
    print(request.user.username)

    user_profile = UserProfile.objects.get_or_create(user=request.user)[0]
    categories = Category.objects.filter(user=request.user)
    subcategories = Subcategory.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)
    liked_pages = LikedPage.objects.filter(user=request.user)
    avg_ratings = {}

    print(liked_pages)
    
    # for liked_page in liked_pages:
    #     print("hi")
    #     all_reviews = Review.objects.filter(Page=liked_page.page)
    #     avg_rating = all_reviews.aggregate(Avg('Stars'))
    #     avg_ratings[liked_page.page] = avg_rating["Stars__avg"]
    #     print(avg_ratings[liked_page.page])
        
    # print(avg_ratings)



    context_dict = {}

    

    context_dict["user_profile"] = user_profile

    url_form = URLForm()
    pic_form = PictureForm()

    context_dict["URLForm"] = url_form
    context_dict["PictureForm"] = pic_form
    context_dict["categories"] = categories
    context_dict["subcategories"] = subcategories
    context_dict["reviews"] = reviews
    context_dict["liked_pages"] = liked_pages
   # context_dict["avg_ratings"] = avg_ratings

    if request.method == "POST":
        if 'url_update' in request.POST:
            url_form = URLForm(request.POST, instance=user_profile)
            if url_form.is_valid:
                url_form.save(commit=False)
                url_form.user = user_profile
                url_form.save()
        if 'pic_update' in request.POST:
            pic_form = PictureForm(request.POST, instance=user_profile)
            if pic_form.is_valid:
                pic_form.save(commit=False)
                pic_form.user = user_profile
                pic_form.save()


    return render(request, 'rango/profile.html', context_dict)


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

    return render(request, 'rango/register.html', context={'user_form': user_form,'profile_form':profile_form,'registered': registered})

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
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            passwordChanged = True
        else:
            print(form.errors)

    else: 
        form = PasswordChangeForm()

    return render(request, "rango/change_password.html", context={"form": form, "success": passwordChanged})





