from django import forms
from .models import RatingReview

class RatingReviewForm(forms.ModelForm):
    score = forms.ChoiceField(choices=[(i, str(i)) for i in range(1, 6)], label="Rating")

    class Meta:
        model = RatingReview
        fields = ['score', 'content']

    def clean_score(self):
        score = self.cleaned_data.get('score')
        return int(score)  # Pastikan untuk mengembalikan nilai sebagai integer
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['score'].widget.attrs.update({
            'class': 'mt-1 border rounded-lg shadow-sm focus:outline-none focus:ring focus:ring-[#6B8E23] w-full',
            'style': 'font-size: 1.10rem; padding: 0.5rem;'
        })
        self.fields['content'].widget.attrs.update({
            'class': 'mt-1 border rounded-lg shadow-sm focus:outline-none focus:ring focus:ring-[#6B8E23] w-full',
            'style': 'font-size: 1.10rem; padding: 0.5rem;'
        })