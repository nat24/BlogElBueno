from django.core.management.base import BaseCommand,CommandError
from techlinx.Staff.models import Staff
from django.contrib.auth.models import User,Group
from django.core.files import File
from django.conf import settings
from faker import Faker



class Command(BaseCommand):
    help = "Crea 10 autores o 2 Editores"
    fake = Faker('es_MX')

    def _create_new_user(self,editor):
        name = self.fake.name().split(' ')[0:1]
        user = User.objects.create_user(
            username=self.fake.user_name(),
            password="techlinx2017",
            first_name=name,
            last_name=self.fake.last_name(),
            email = self.fake.email(),
            is_staff = True
        )
        grupo = Group.objects.get(name="Editores") if editor else Group.objects.get(name="Autores")
        grupo.user_set.add(user)

        return user

    def _create_new_staff(self,editor=False):
     
        num_staff = 2 if editor else 5
        for x in range(0,num_staff):
            staff = Staff(
                user = self._create_new_user(editor=editor),
                biografia = self.fake.text(),
                autor = not editor,
                editor = editor
            )
            path = settings.BASE_DIR+'/temp/user.png'

            staff.imagen.save(self.fake.random_letter()+".png",File(open(path,'r')))
    


    def add_arguments(self,parser):
        parser.add_argument('-e','--Editor',dest="Editor")
    
    
    def handle(self,*args, **options):
        try:
            if options.get('Editor',None):
                self._create_new_staff(editor=True)
            else:
                self._create_new_staff()
        except Exception as e:
            raise CommandError("Error con mensaje: "+str(e))
        self.stdout.write(self.style.SUCCESS('Miembros de estaff creados correctamente'))