from django.utils import timezone
from django.views import generic
from django.core.paginator import Paginator
from django.contrib import messages
from .tasks import send_mail
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Blog, Category, Comment, Reply, quote, style
from django.utils.safestring import mark_safe
import json
from User.models import User, Message

# Create your views here.

def loginPage(request):
    if request.user.is_authenticated:
        
        return redirect('Profile:chat')
    else:
        if request.method == 'POST':

            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('Profile:chat', user)
            else:
                messages.error(request, 'Incorrect Username or password')
        return render(request, 'Profile/login.html')


def logoutUser(request):
    logout(request)
    return redirect('Profile:login')


def index(request):
    
    blog = Blog.objects.filter(
        date__lte=timezone.now(), publish=True
        ).order_by('-date')[:3]
    
    quotes = quote.objects.all()
    
    
    content = {'blog':blog, 'quotes':quotes}
    return render(request, 'Profile/index.html', content)

class ListView(generic.ListView):
    template_name = 'Profile/blog.html'
    context_object_name = 'Published_blogs'
    ordering = ['-date']
    paginate_by = 9

    def get_queryset(self):
        return Blog.objects.all()

    # def get_context_data(self, **kwargs):
    #     if 'q' in self.request.GET:
    #             q = self.request.GET['q']
    #             context['blog'] = Blog.objects.filter(title__icontains=q)
    #     return context

    
class DetailView(generic.DetailView):
    model = Blog
    template_name = 'Profile/blog-single.html'

    def get_context_data(self, **kwargs):
        pk = self.kwargs['slug']
        blog = Blog.objects.get(slug=pk)
        context = super().get_context_data(**kwargs)
    
        context['recent_blog'] = Blog.objects.filter(date__lte=timezone.now()).order_by('-date')[:5]
        context['tag'] = Category.objects.all()
        context['comments'] = Comment.objects.filter(blog=blog)
        context['comment'] = Paginator(context['comments'], 3)
        context['page_number'] = self.request.GET.get('page')
        context['page_obj'] = context['comment'].get_page(context['page_number'])
        context['count'] = context['comments'].count()
        # context['replys'] = Reply.objects.filter(comment=context['comment'])

        # if 'q' in self.request.GET:
        #     q = self.request.GET['q']
        #     context['blog'] = Blog.objects.filter(title__icontains=q)
        return context

class Profile(generic.DetailView):
    model = User
    template_name = "Profile/author_profile.html"

# def auth(request):
#     if request.user.is_autheticated:
#         user = request.user.username
#         return HttpResponseRedirect(reverse('Profile:chat', args=(user)))
#     return render(request, 'Profile/index.html')

def room(request, room_name):
    Users = User.objects.filter(is_superuser=False)

    if request.user.is_superuser == True:
        to = User.objects.get(username=room_name) 
        to = to.id
        
    else:
        to = User.objects.get(username='toluwani')
        to = to.id
    
    user = User.objects.get(id=to)
    return render(request, 'Profile/chatroom.html',{
        'user':user,
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
        'id': mark_safe(json.dumps(request.user.id)),
        'to': mark_safe(json.dumps(to)),
        'Users': Users}
        )

def error_404(request, exception):
    return render(request, 'Profile/404.html')

def contact(request):
    # Email ==========================================================================
    name = request.POST.get('name')
    email = request.POST.get('email')
    subject = request.POST.get('subject')
    message = request.POST.get('message')
    send_mail.delay(name, email, subject, message)
    messages.success(request, 'Your message is being sent')
    return HttpResponseRedirect(reverse('Profile:home'))

def comment(request, slug):

    name = request.POST.get('name')
    email = request.POST.get('email')
    comment = request.POST.get('message')

    Blog = Blog.objects.get(slug= slug)
    Comment = Comment.objects.create(blog=Blog.id, name=name, email=email, comment=comment)
    return HttpResponseRedirect(reverse('Profile:blog_single', args=(Blog.slug)))
