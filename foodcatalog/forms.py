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