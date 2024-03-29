from django.shortcuts import render, get_object_or_404
from .models import Post, MyAbout, Contact, Portfolio
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count

# Create your views here.

def portfolio_details(request, id):
    port = get_object_or_404(Portfolio, id=id)
    portfolio = Portfolio.objects.all()

    context = {
        'port': port,
        'portfolio': portfolio
    }

    return render(request, 'blog/post/portfolio-details.html', context)


def post_list(request, tag_slug=None):
    portfolio = Portfolio.objects.all()
    about = MyAbout.objects.all()
    post_list = Post.published.all()
    contacts = Contact.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    
    # har bir sahifada 3 ta post bilan sahifalash
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)

    try: 
        posts = paginator.page(page_number)

    except PageNotAnInteger:
        #Agar sahifa raqami butun son bo'lmasa, u holda birinchi sahifani ko'rsatish
        posts = paginator.page(1)

    except EmptyPage:
        # Agar sahifa_raqami diapazondan tashqarida bo'lsa
        # oxirgi sahifani ko'rsatish        
        posts = paginator.page(paginator.num_pages)

    context = {
        'portfolio': portfolio,
        'about': about,
        'posts': posts,
        'tag': tag,
        'contacts': contacts,
    }

    return render(request, 'blog/post/list.html', context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                            slug=post,
                            publish__year=year,
                            publish__month=month,
                            publish__day=day
    )
    
    # Ushbu post uchun faol sharhlar ro'yxati
    comments = post.comments.filter(active=True)
    # Foydalanuvchi sharhlar shakli
    form = CommentForm()

    # Shunga o'xshash postlar ro'yxati
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids) \
                                        .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')) \
                                        .order_by('-same_tags','-publish')[:4]
            
    context = {
        'post': post, 
        'comments': comments, 
        'form': form, 
        'similar_posts': similar_posts,
    }

    return render(request, 'blog/post/detail.html', context)


# Postlarni elektron poshta orqali yuborish
def post_share(request, post_id):
    # Identifikatori bo'yicha postni oling

    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        # shakl qayta ishlash uchun yuborildi
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Shakil maydonlari muvaffaqiyatli tasdiqlandi
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " f"{post.title}"
            message = f"Read {post.title} at {post_url} \n\n" f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'your_account@gmail.com', [cd['to']])

            sent = True
        # elektron pochta xabarini yuboring
    else:
        form = EmailPostForm()

    context = {
        'post': post, 
        'form': form, 
        'sent': sent
    }

    return render(request, 'blog/post/share.html', context)

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None

    # Izoh e'lon qilindi
    form = CommentForm(data=request.POST)
    
    if form.is_valid():
        # Ma'lumotlar bazasida saqlamasdan Comment sinfi ob'ektini yarating
        comment = form.save(commit=False)  # Use commit=False to get the instance without saving to the database
        # Fikr bildirish uchun post tayinlang
        comment.post = post
        # Fikrni ma'lumotlar bazasiga saqlang
        comment.save()

    context = {
        'post': post, 
        'form': form, 
        'comment': comment
    }

    return render(request, 'blog/post/comment.html', context)