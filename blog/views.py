from django.shortcuts import render
from .models import Blog

# Create your views here.
def post_page(request):
    blogs = Blog.objects.filter(is_published=True).order_by('-upload_date')
    for blog in blogs:
        blog.first_line = blog.content.split('\n')[0]
    return render(request, 'blogpage.html', {'blog':blogs})


def blog(request,slug):
    blog = Blog.objects.get(slug=slug) 
    return render(request, 'blog.html', {'blog':blog})
