from django.http import JsonResponse
import jdatetime
from django.shortcuts import render, get_object_or_404, redirect
from . import models
from .forms import blogForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Count, Q
from .models import Blog, Comment
from .forms import CommentForm
from django.utils.timezone import now
from .models import Comment, Reply
from .forms import ReplyForm
import json

def blog_list_view(request):
    search_query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'newest')  # مقدار پیش‌فرض 'newest' تنظیم شد

    blogs = models.Blog.objects.all()

    # اعمال جستجو
    if search_query:
        blogs = blogs.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

    # اعمال فیلتر
    if sort_by == 'newest':
        blogs = blogs.order_by('-created_at')
    elif sort_by == 'oldest':
        blogs = blogs.order_by('created_at')
    elif sort_by == 'most_commented':
        blogs = blogs.annotate(comment_count=Count('comments')).order_by('-comment_count')
    elif sort_by == 'most_liked':
        blogs = blogs.annotate(like_count=Count('likes')).order_by('-like_count')
    elif sort_by == 'most_viewed':
        blogs = blogs.order_by('-views')

    paginator = Paginator(blogs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for blog in page_obj:
        blog.created_at_jalali = jdatetime.datetime.fromgregorian(datetime=blog.created_at).strftime('%Y/%m/%d')

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'sort_by': sort_by
    }
    return render(request, 'blog/blog_list.html', context)



def blog_detail_view(request, pk):
    blog = get_object_or_404(Blog, pk=pk)

    # افزایش تعداد بازدید
    blog.views += 1
    blog.save()

    # تبدیل تاریخ وبلاگ به جلالی
    blog.created_at_jalali = jdatetime.datetime.fromgregorian(datetime=blog.created_at).strftime('%Y/%m/%d')
    blog.updated_at_jalali = jdatetime.datetime.fromgregorian(datetime=blog.updated_at).strftime('%Y/%m/%d')

    # گرفتن کامنت‌های اصلی و تبدیل تاریخ‌ها به جلالی
    comments = blog.comments.filter(is_active=True, parent__isnull=True).order_by('-datetime_created')
    for comment in comments:
        comment.datetime_created_jalali = jdatetime.datetime.fromgregorian(datetime=comment.datetime_created).strftime('%Y/%m/%d')


    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            parent_id = request.POST.get("parent")
            new_comment = comment_form.save(commit=False)
            new_comment.blog = blog
            new_comment.user = request.user
            # اگر پاسخ به یک کامنت باشد
            if parent_id:
                parent_comment = get_object_or_404(Comment, id=parent_id)
                new_comment.parent = parent_comment
            new_comment.save()
            return redirect(f'{blog.get_absolute_url()}#comment-{new_comment.id}')
    else:
        comment_form = CommentForm()

    context = {
        'blog': blog,
        'comments': comments,
        'comment_form': comment_form,
        'is_liked': request.user in blog.likes.all(),
    }
    return render(request, 'blog/blog_detail.html', context)





@login_required
def like_blog_view(request, pk):
    blog = get_object_or_404(models.Blog, pk=pk)
    if request.user in blog.likes.all():
        blog.likes.remove(request.user)
    else:
        blog.likes.add(request.user)
    return redirect('blog_detail', pk=pk)

@login_required
def blog_create_view(request):
    if request.method == 'POST':
        form = blogForm(request.POST, request.FILES)
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.author = request.user  # نویسنده رو به کاربر وارد شده تنظیم کنید
            new_blog.save()
            return redirect('blog_list')
    else:
        form = blogForm()
    return render(request, 'blog/blog_create.html', { 'form': form } )


@login_required
def blog_update_view(request, pk):
    blog = get_object_or_404(models.Blog, pk=pk)

    # چک کردن اینکه آیا کاربر همان نویسنده پست است
    if blog.author != request.user:
        return HttpResponseForbidden("شما اجازه ویرایش این پست را ندارید.")
    
    if request.method == 'GET':
        form = blogForm(instance=blog)
        return render(request, 'blog/blog_update.html', { 'form': form , 'blog': blog})
    elif request.method == 'POST':
        form = blogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog_list')


@login_required
def blog_delete_view(request, pk):
    blog = get_object_or_404(models.Blog, pk=pk)

    # چک کردن اینکه آیا کاربر همان نویسنده پست است
    if blog.author != request.user:
        return HttpResponseForbidden("شما اجازه حذف این پست را ندارید.")
    
    if request.method == 'POST':
        blog.delete()
        return redirect('blog_list')
    return render(request, 'blog/blog_delete.html', { 'blog': blog })

@login_required
def comment_edit_view(request, pk):
    comment = get_object_or_404(models.Comment, pk=pk)
    if comment.user != request.user:
        return JsonResponse({'success': False, 'error': 'شما اجازه ویرایش این کامنت را ندارید.'})

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_text = data.get('text')
            if new_text:
                comment.text = new_text
                comment.save()
                return JsonResponse({
                    'success': True,
                    'comment': {
                        'id': comment.id,
                        'text': comment.text,
                        'user': comment.user.username,
                        'datetime_created_jalali': jdatetime.datetime.fromgregorian(
                            datetime=comment.datetime_created
                        ).strftime('%Y/%m/%d')
                    }
                })
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
def comment_delete_view(request, pk):
    comment = get_object_or_404(models.Comment, pk=pk)
    if comment.user != request.user:
        return JsonResponse({'success': False, 'error': 'شما اجازه حذف این کامنت را ندارید.'})

    if request.method == "POST":
        comment.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def like_blog_view(request, pk):
    blog = get_object_or_404(models.Blog, pk=pk)
    if request.user in blog.likes.all():
        blog.likes.remove(request.user)
        liked = False
    else:
        blog.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'total_likes': blog.total_likes})

@login_required
def like_comment_view(request, pk):
    comment = get_object_or_404(models.Comment, pk=pk)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
        liked = False
    else:
        comment.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'total_likes': comment.total_likes})


@login_required
def create_reply(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            text = data.get('text')
            if text:
                reply = Reply.objects.create(
                    comment=comment,
                    user=request.user,
                    text=text
                )
                return JsonResponse({
                    'success': True,
                    'reply': {
                        'id': reply.id,
                        'text': reply.text,
                        'user': reply.user.username,
                        'datetime_created_jalali': jdatetime.datetime.fromgregorian(
                            datetime=reply.datetime_created
                        ).strftime('%Y/%m/%d')
                    }
                })
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def edit_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id, user=request.user)
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            text = data.get('text')
            if text:
                reply.text = text
                reply.save()
                return JsonResponse({
                    'success': True,
                    'reply': {
                        'id': reply.id,
                        'text': reply.text,
                        'user': reply.user.username,
                        'datetime_created_jalali': jdatetime.datetime.fromgregorian(
                            datetime=reply.datetime_created
                        ).strftime('%Y/%m/%d')
                    }
                })
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def delete_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id, user=request.user)
    if request.method == "POST":
        reply.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def like_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)
    if request.user in reply.likes.all():
        reply.likes.remove(request.user)
        liked = False
    else:
        reply.likes.add(request.user)
        liked = True
    return JsonResponse({"liked": liked, "total_likes": reply.likes.count()})

@login_required
def comment_create_view(request, pk):
    if request.method == "POST":
        blog = get_object_or_404(Blog, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.blog = blog
            new_comment.user = request.user
            new_comment.save()
            
            # Convert datetime to Jalali for the response
            new_comment.datetime_created_jalali = jdatetime.datetime.fromgregorian(
                datetime=new_comment.datetime_created
            ).strftime('%Y/%m/%d')
            
            return JsonResponse({
                'success': True,
                'comment': {
                    'id': new_comment.id,
                    'user': new_comment.user.username,
                    'text': new_comment.text,
                    'datetime_created_jalali': new_comment.datetime_created_jalali
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
