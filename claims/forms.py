from django import forms
from .models import ClaimRequest

class ClaimSubmissionForm(forms.ModelForm):
    class Meta:
        model = ClaimRequest
        fields = ['answer_to_secret_mark', 'proof_image']
        widgets = {
            'answer_to_secret_mark': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Answer the secret question specifically with details only the authentic owner knows...'
            }),
            'proof_image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'answer_to_secret_mark': 'Answer to Secret Question / Ownership Details',
            'proof_image': 'Supporting Proof Photo (Optional)',
        }

class ClaimReviewForm(forms.ModelForm):
    class Meta:
        model = ClaimRequest
        fields = ['status', 'finder_notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'finder_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Leave a message for the claimant (e.g. Please meet me at Academic Bldg 1 Department Office at 2 PM to collect)...'
            }),
        }
