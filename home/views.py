

# Create your views here.
from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import render,HttpResponse,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django. contrib import messages
from django.utils import timezone




# Create your views here.



def homepage(request):
    views = {}
    views['blogs'] = Blog.objects.all()
    
    return render(request,'home.html',views)




def blog_single(request, id):
    blog = get_object_or_404(Blog, id=id)
    comments = Comment.objects.filter(blog=blog)

    context = {
        'blog_details': blog,
        'blog_comments': comments,
    }

    return render(request, 'blog-single.html', context)


def contact(request):
    if request.method == 'POST':
        na = request.POST['name']
        em = request.POST['email']
        sub = request.POST['subject']
        mes = request.POST['message']
        data = Contact.objects.create(
            name = na,
            email = em,
            subject = sub,
            message = mes
        )
        data.save()

    return render(request,'contact.html')



def about(request):
    return render(request,'about.html')

def category_view(request, category_name):
    category = Category.objects.get(name=category_name)
    blogs = Blog.objects.filter(category=category)

    context = {
        'blogs': blogs,
        'category': category,
    }
    return render(request, 'category.html', context)


def search_view(request):
    if request.method == 'GET':
        search_query = request.GET.get('search_query', '')

        # Perform the search query on the Blog model
        blogs = Blog.objects.filter(title__icontains=search_query)

        context = {
            'search_query': search_query,
            'blogs': blogs
        }
        return render(request, 'search.html', context)


def register(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('confirm_password')
        profile_picture = request.FILES.get('profilepicture')  # Get the uploaded file
        fn = request.POST.get('fullname')
        
        if pass1 != pass2:
            messages.error(request, "Your password and confirm password are not the same!")
        else:
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()

            # Create a Customer instance and associate it with the User
            customer = Customer.objects.create(username=uname, email=email, profilepicture=profile_picture, fullname=fn )
            customer.save()
            messages.success(request, 'Registration successful. You can now log in.')

            return redirect('login')

    return render(request, 'registration.html')


def loginview(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('password')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('home')


@login_required
def profile(request):
    customer = Customer.objects.get(username=request.user.username)
    context = {'customer': customer}
    return render(request, 'profile.html', context)





@login_required
def edit_profile(request):
    message = messages.get_messages(request)
    customer = Customer.objects.get(username=request.user.username)

    if request.method == 'POST':
        customer.fullname = request.POST.get('fullname')
        customer.email = request.POST.get('email')

        # Update the profile picture if provided
        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            customer.profilepicture = profile_picture

        # Save the updated customer object
        customer.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')

    context = {'customer': customer}
    return render(request, 'editprofile.html', context)


@login_required
def post_comment(request):
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        blog_id = request.POST.get('blog_id')

        # Verify that blog_id is not empty or None
        if blog_id:
            comment = Comment.objects.create(
                text=comment_text,
                user=request.user,
                created_at=timezone.now(),
                blog_id=blog_id
            )

            return redirect('blog_single', id=int(blog_id))

    return redirect('blog_single', id=int(blog_id))