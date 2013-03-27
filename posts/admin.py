from django.contrib import admin

from flexible_content.admin import ContentAreaAdmin

from .models import Post


def get_preview_link(obj):
    return """<a href="%s">%s</a>""" % (obj.get_absolute_url(),
                                        obj.get_absolute_url())
get_preview_link.short_description = u"Preview Link"
get_preview_link.allow_tags = True


class PostAdmin(ContentAreaAdmin):
    list_display = (
        'title',
        get_preview_link,
        'published',
    )
    prepopulated_fields = {
        'slug': ('title',),
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'author':
            kwargs['initial'] = request.user.id
            return db_field.formfield(**kwargs)
        return super(MyModelAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    def get_fieldsets(self, request, obj=None):
        """
        If they're not a superuser, don't let them chooose the author.
        """
        fieldsets = super(PostAdmin, self).get_fieldsets(request, obj)

        # If they're not a superuser, troll the fieldsets var for the author
        # field and remove it.
        if not request.user.is_superuser:
            for fs in fieldsets:
                fields = fs[1]['fields']
                if 'author' in fields:
                    fields.remove('author')

        return fieldsets

    def get_form(self, request, obj=None, **kwargs):
        # If they're not a superuser and they're submitting the form, they
        # weren't shown the author field, so hack in their username so the form
        # finds it.
        if request.method == 'POST' and not request.user.is_superuser:
            request.POST = request.POST.copy()
            request.POST['author'] = request.user.pk

        return super(PostAdmin, self).get_form(request, obj, **kwargs)

admin.site.register(Post, PostAdmin)
