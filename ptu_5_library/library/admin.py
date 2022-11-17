from django.contrib import admin
from . import models
# Register your models here.

class BookInstanceInline(admin.TabularInline):
    model = models.BookInstance
    extra = 0
    readonly_fields = ('unique_id',)
    can_delete = False


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn','author', 'display_genre')
    inlines = (BookInstanceInline, )


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('unique_id', 'book', 'status', 'due_back', 'reader' )
    list_filter = ('status', 'due_back')
    readonly_fields = ('unique_id', 'is_overdue')
    # foreign key __ laukas (apacioj) DJANGI look-ups
    search_fields = ('unique_id', 'book__title', 'book__author__last_name__exact', 'reader__last_name')
    # dajngo select2 admin filters
    list_editable = ('status', 'due_back', 'reader')

    fieldsets = (
                ('General', {'fields': ('unique_id', 'book')}),
                ('Availability', {'fields': (('status', 'due_back'), 'reader', 'is_overdue')}),
    )
 

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'display_books')
    list_display_links = ('last_name',)


admin.site.register(models.Author, AuthorAdmin)
admin.site.register(models.Genre)
admin.site.register(models.Book, BookAdmin)
# nurodom koki modeli registruojam i registruiojam modeli i admina ir tada jam galetume uzdeti 
admin.site.register(models.BookInstance, BookInstanceAdmin)

