
from techlinx.Blog.models import Post, Categories
from techlinx.Staff.models import Staff
from faker import Faker
from random import randint
from django.core.files import File
from django.conf import settings


def generate_paragraphs():
    fake = Faker()
    num_paragraphs = randint(2,8)
    paragraphs = list()
    for x in range(0,num_paragraphs):
        paragraph = "{0} {1} {2}".format('<p>',fake.text(max_nb_chars=700),'</p>')
        paragraphs.append(paragraph)
    return "".join(paragraphs)




def generate_random_post(num):

    autors = Staff.objects.filter(autor=True)
    categories = Categories.objects.all()
    fake = Faker('es_MX')
    path = settings.BASE_DIR+'/temp/user.png'
    for x in range(0,num):
        random_autor = autors[randint(0,(len(autors)-1))]
        random_category = categories[randint(0,(len(categories)-1))]
        try:
            Post.objects.create(
            titulo = fake.sentence(nb_words=5),
            contenido = generate_paragraphs(),
            cover = fake.image_url(width=1400,height=780),
            autor = random_autor,
            categoria=random_category,
            publicado = True

        )
        except Exception as e:
            print("Error: {}".format(e))
       

