from django.contrib import admin
from polls.models import Choice, Question

class ChoiceInline(admin.TabularInline):
#class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

#admin.site.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fieldsets=[
        ('First block',  {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes':['collapse']}),
        #(None, {'fields': ['pub_date']})
    ]
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
#admin.site.register(Choice)

# Register your models here.
