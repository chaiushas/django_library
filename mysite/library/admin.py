from django.contrib import admin
from .models import Author, Genre, Book, BookInstance


# Register your models here.
class BookInstanceInLine(admin.TabularInline):
    model = BookInstance
    extra = 0  # isjungia placeholderius
    can_delete = False
    readonly_fields = ('uuid',)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'display_books')


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'author', 'display_genre')
    inlines = [BookInstanceInLine]


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'book', 'due_back', 'reader')
    list_filter = ('status', 'due_back')
    fieldsets = (
        ("General", {"fields": ('uuid', 'book')}),
        ("Availability", {"fields": ('status', 'due_back', 'reader')})
    )
    search_fields = ('uuid', 'book__title')


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
admin.site.register(BookInstance, BookInstanceAdmin)
