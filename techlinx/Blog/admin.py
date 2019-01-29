from django.contrib import admin
from .models import Post, Categories, Comment
from techlinx.Staff.models import Staff
# Register your models here.
from django_summernote.admin import SummernoteModelAdmin


class PostAdmin(SummernoteModelAdmin):
    summer_note_fields = ('contenido',)
    fields = ('titulo', 'contenido', 'cover', 'categoria')
    list_display = ('titulo', 'categoria', 'publicado', 'fecha_creacion')

    def _editor_or_superuser(self, request):
        editor = Staff.objects.filter(user=request.user, editor=True).exists()
        if request.user.is_superuser or editor:
            return True
        return False

    def get_form(self, request, obj=None, **kwargs):
        editor_fields = ('publicado', )
        if self._editor_or_superuser(request):
            self.fields = self.fields + editor_fields
        else:
            self.fields
        return super(PostAdmin, self).get_form(request, obj, **kwargs)

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        if self._editor_or_superuser(request):
            return qs
        return qs.filter(autor__user=request.user)

    def save_model(self, request, obj, form, change):
        print("Cambios??? " + str(change))
        if not change:
            obj.autor = Staff.objects.get(user__id=request.user.id)
        super().save_model(request, obj, form, change)

    def author(self, instance):
        return instance.autor

    def time_estimate(self, instance):
        return instance.tiempo_estimados

    author.short_description = "Autor del post"
    time_estimate.short_description = "Tiempo estimado de lectura"


class CategorieAdmin(admin.ModelAdmin):
    fields = ('nombre', 'imagen')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user','email','created','approved_comment')

admin.site.register(Post, PostAdmin)
admin.site.register(Categories, CategorieAdmin)
admin.site.register(Comment, CommentAdmin)
