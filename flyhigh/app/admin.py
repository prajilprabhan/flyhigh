from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Country)
admin.site.register(Course)
admin.site.register(Institute)
admin.site.register(University)
admin.site.register(Accommodation)
admin.site.register(CourseMaterial)
admin.site.register(JobVacancy)
admin.site.register(Scholarship)
admin.site.register(TestCenter)
admin.site.register(TestData)
admin.site.register(Visa)
admin.site.register(BankLoan)
admin.site.register(Profile)
admin.site.register(ExamRegistration)
admin.site.register(Experience)

class BatchRegInline(admin.TabularInline):
    model =BatchReg
    extra = 1 # Number of empty BatchReg forms to display

class BatchAdmin(admin.ModelAdmin):
    inlines = [BatchRegInline]

admin.site.register(Batch, BatchAdmin)

class ReplyInline(admin.TabularInline):
    model = Reply
    extra = 0

class CommentAdmin(admin.ModelAdmin):
    inlines = [ReplyInline]
    list_display = ('name', 'body', 'date')
    search_fields = ('name__username', 'body')

admin.site.register(Comment, CommentAdmin)
admin.site.register(Reply)
