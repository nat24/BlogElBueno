from django.db import models
from uuid import uuid4
from django.utils.text import slugify
from datetime import datetime
# Create your models here.

def path_save_images(instance,filname): #TODO DRY
    return "{0}/{1}".format(instance.slug,filname)

class Categories(models.Model):
    id = models.UUIDField(primary_key = True,
        unique = True,
        default = uuid4,
        editable = False)

    nombre =  models.CharField(max_length = 150,
        help_text="Nombre de la categoria")

    slug = models.SlugField(max_length = 200,
        unique = True,
        help_text = "Slug de url del post")

    imagen = models.ImageField(upload_to=path_save_images,
        help_text="Imagen de la categoria")



    def _get_unique_slug(self):
        slug = slugify(self.nombre)
        unique_slug = slug
        num = 1
        while Categories.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
    def _get_published_date(self):
        return datetime.now()

    @models.permalink
    def get_absolute_url(self):
        return 'blog:category', (self.slug,)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save()

    def __str__(self):
        return "Categoria: {}".format(self.nombre)

class Post(models.Model):

    id = models.AutoField(primary_key = True,
        unique = True)
    titulo = models.CharField(max_length = 150,
        help_text="Titulo del Post")
    slug = models.SlugField(max_length = 200,
        unique = True,
        help_text = "Slug de url del post")
    contenido = models.TextField(help_text="Contenido del Post")
    cover = models.ImageField(upload_to=path_save_images,
    help_text = "Imagen de cover del post")
    categoria = models.ForeignKey(Categories,
        on_delete = models.SET_NULL,
        blank = True,
        null = True,
        help_text = "Categoria del post",
        related_name = "publicaciones")
    publicado = models.BooleanField(default=False,
        verbose_name = "¿Post publicado?",
        help_text = "Check si post esta publicado")
    fecha_creacion = models.DateField(auto_now_add=True,
        help_text = "Fecha en que se creo el post")
    fecha_publicacion = models.DateField(null=True,
        blank=True,
        help_text = "Fecha en la que se publico el post"
    )
    tiempo_estimado = models.IntegerField(
        help_text = "Tiempo aproximado de lectura del post",
        default = 0
    )
    autor = models.ForeignKey("Staff.Staff",
        on_delete=models.CASCADE,
        help_text="Usuario Autor",
        null=True,
        related_name="publicaciones")

    def _get_unique_slug(self):
        slug = slugify(self.titulo)
        unique_slug = slug
        num = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def _get_published_date(self):
        return datetime.now()

    def _get_average_reading(self):
        WPM = 180 #Tiempo aproximado en el que una persona lee palabras
        num_words = len(self.contenido.split(" ")) #TODO Checar si hay tags u otro tipo de cosas que afecten el calculo
        return int(num_words/WPM)

    @models.permalink
    def get_absolute_url(self):
        return 'blog:post', (self.slug,)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        if self.publicado and not self.fecha_publicacion:
            self.fecha_publicacion = self._get_published_date()
        self.tiempo_estimado = self._get_average_reading()
        super().save()

    def __str__(self):
        return "Post: {0}".format(self.titulo)

#Aqui van los Comentarios 11/11/2018
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    user = models.CharField(max_length=200)
    email = models.EmailField()
    text = models.TextField(max_length=160)
    created = models.DateTimeField(auto_now_add=True)
    approved_comment = models.BooleanField(default=False)

    def approved(self):
        self.approved = True
        self.save()

    def __str__(self):
        return '{}-{}'.format(self.post.title. str(self.username))

#Caja de Comentario 08/11/
#class Comment(models.Model):
#        Post= models.ForeignKey('blog.Post', on_delete=models.CASCADE, releated_name="comments")
#        author= models.CharField(max_length=200)
#        text = models.TextField()
#        create_date = models.DateTimeField(default=tiemezone.now)
#        approved_comment = models.BooleanField(default=False)

#        def approve(self):
#            self.approved_comment = True
#            self.save()

#        def __str__(self):
#            return self.text
