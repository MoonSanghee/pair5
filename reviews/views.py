from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Review
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm, CommentForm
from django.contrib import messages

# Create your views here.
def index(request):
    reviews = Review.objects.all()
    context = {'reviews':reviews}
    return render(request, 'reviews/index.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, '글 작성이 완료되었습니다.')
            return redirect('reviews:index')
    else:
        review_form = ReviewForm()
    context = {
        'review_form': review_form
    }
    return render(request, 'reviews/form.html', context=context)

def detail(request, pk):
    review = Review.objects.get(pk=pk)
    comment_form = CommentForm()
    context = {
        'review': review,
        'comments': review.comment_set.all(),
        'comment_form': comment_form,
    }
    return render(request, 'reviews/detail.html', context)

@login_required
def update(request, pk):
    review = Review.objects.get(pk=pk)
    if request.user == review.user:
        if request.method == 'POST':
            review_form = ReviewForm(request.POST, request.FILES, instance=review)
            if review_form.is_valid():
                review_form.save()
                messages.success(request, '글이 수정되었습니다.')
                return redirect('reviews:detail', review.pk)
        else:
            review_form = ReviewForm()
        context = {
            'review_form': review_form
        }
        return render(request, 'reviews/form.html', context)
    else:
        messages.warning(request, '작성자만 수정할 수 있습니다.')
        return redirect('reviews:detail', review.pk)

@login_required
def comment_create(request, pk):
    review = get_object_or_404(Review, pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
    context = {
        'content': comment.content,
        'userName': comment.user.username
    }
    return JsonResponse(context)

def likes(request, reviews_pk):
    review = get_object_or_404(Review, pk = reviews_pk)
    if request.user in review.like_user.all():
        review.like_user.remove(request.user)
        is_liked = False
    else:
        review.like_user.add(request.user)
        is_liked = True
    context = {'isLiked': is_liked, 'likeCount': review.like_user.count()}
    return JsonResponse(context)