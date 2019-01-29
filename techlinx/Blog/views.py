from django.shortcuts import render,get_object_or_404, redirect
from .models import Post,Categories,Comment
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CommentForm

# Create your views here.

def index(request):
    imagen = "/static/img/sidebar.jpg"
    posts_list =  Post.objects.filter(publicado=True).select_related('autor').order_by('-fecha_publicacion')
    categories = Categories.objects.all()
    paginator = Paginator(posts_list, 5)
    page = request.GET.get('page',1)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)



    return render(request,'blog/index.html',{'image':imagen,'posts':posts, 'categories':categories})



def post(request,slug):

    post = get_object_or_404(Post,slug=slug)
    comments = Comment.objects.filter(post=post).order_by('-id')
    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            text = request.objects.create(post=post, text=text)
            comment = Comment.objects.create(pos=post, user=request.user, text=text)
            comment.save()
            return HttpResponseRedirect(post.get_absolute_url())
        else:
            comment_form= CommentForm()

    context = {
    'post': post,
    'comments':comments,
    
    }

    print('post: '+post.titulo)
    related = Post.objects.filter(Q(categoria=post.categoria) | Q(autor=post.autor), ~Q(titulo=post.titulo))[:3]
    return render(request,'blog/post/post.html',{'post':post,'related':related})

#def add_comment(request, slug):
#        post = get_object_or_404(Post, slug=slug)
#        if request.method == 'POST':
#            form =CommentForm(request.POST)
#            if form.is_valid():
#                comment = form.save(commit=False)
#                comment.post = post
#                comment.save()
#                return redirect('blog:post', slug=post.slug)
#        else:
#            form =CommentForm()
#        template = 'blog/post/add_comment.html'
#        context = {'form': form}
#        return render(request, template, context)

#13/11/2018 agregado este comando primera parte
#def categories(request, idcategory):
#    categories = Categories.objects.get(id=idcategories)
#    posts = categories.post_set.order_by("-creation_date")

#    return render_to_response(
#        "home.html",
#        {
#            "posts":posts,
#        },
#    )

#def categories(request):
#    categories = Categories.objects.all()
#    return render(request, 'blog/categorias/index.html',{'categories':categories})

#def categories(request, pk):
#    categories = get_object_or_404(Categories, pk=pk)
#    return render(request, 'blog/base.html',{'categories':categories})
def categories(request, slug):
    postt = Post.objects.all()
    slugg = slug
    return render(request,'blog/categorias/cate.html',{'postt':postt, 'slugg': slugg})
