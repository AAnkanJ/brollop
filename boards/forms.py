from django import forms
from .models import Topic, Post, Gift

class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'What is on your mind?'}
        ),
        max_length=4000,
        help_text='The max length of the text is 4000.'
    )

    class Meta:
        model = Topic
        fields = ['subject', 'message']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message','topic' ]

class BuyGiftForm(forms.ModelForm):
    boughtBy_1 = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'Skriv ditt namn och gärna ett meddelande till brudparet'}
        ),
        max_length=4000,
        help_text='The max length of the text is 4000.',
        label = ''
    )
    costPayed = forms.IntegerField(
        label = 'Välj hur mycket du vill betala'
    )
    class Meta:
        model = Gift
        fields = ['costPayed', 'boughtBy_1']

class BuyGiftFormOnskelista(forms.ModelForm):
    boughtBy_1 = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'Tack för att du bestämt dig för att köpa en present till Alfred. Skriv ditt namn och gärna ett meddelande till Alfred'}
        ),
        max_length=4000,
        help_text='The max length of the text is 4000.',
        label = ''
    )
    class Meta:
        model = Gift
        fields = ['boughtBy_1']
