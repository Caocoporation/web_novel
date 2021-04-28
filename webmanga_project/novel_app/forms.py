from django import forms
from .models import (
    Novel, Novel_Illustration, Chapter, 
    Chapter_Illutrations, Comment, Author
)

# set input type for date input
class DateInput(forms.DateInput):
    input_type = "date"

class AuthorCreationForm(forms.ModelForm):
    dob = forms.DateField(
        required=False, 
        label = "Date of Birth",
        widget = DateInput,
    ) 

    class Meta: 
        model = Author
        fields = ["name", "dob", "description"]
       
class NovelCreationForm(forms.ModelForm):
    # title = forms.CharField(max_length=100)
    # content = forms.Textarea

    class Meta: 
        model = Novel
        fields = ["title", "genre", "content"]

class NovelUpdateForm(forms.ModelForm):
    posted_date = forms.DateField(
        required=False,
        label = "Posted Date",
        widget = DateInput,
    )

    class Meta:
        model = Novel
        fields = ["title", "posted_date", "content", "status"]
    
class NovelIllustrationForm(forms.ModelForm):
    image = forms.ImageField(allow_empty_file=True, label="Illustration", required=False)

    class Meta:
        model = Novel_Illustration
        fields = ["image"]

class ChapterCreationForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    content = forms.TextInput()

    class Meta: 
        model = Chapter
        fields = ["title", "content"]

class ChapterIllustrationForm(forms.ModelForm):
    illustrations = forms.ImageField(required=False, label="Illustration", allow_empty_file=True)

    class Meta:
        model = Chapter_Illutrations
        fields = ["illustrations"]

# class ChapterUpdateForm(forms.ModelForm):
#     content = forms.TextInput()

#     class Meta:
#         model = Comment
#         fields = ["content"]