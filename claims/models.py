from django.db import models
from django.contrib.auth.models import User
from items.models import Item

CLAIM_STATUS_CHOICES = [
    ('PENDING', 'Pending Verification'),
    ('ACCEPTED', 'Accepted - Verification Succeeded'),
    ('REJECTED', 'Rejected - Proof Mismatch'),
]

class ClaimRequest(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='claims')
    claimant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_claims')
    answer_to_secret_mark = models.TextField(help_text="Detailed answer to the finder's verification question")
    proof_image = models.ImageField(upload_to='claims/proofs/', blank=True, null=True, help_text="Optional: Photo of receipt, matching sticker, ID, or old photo with the item")
    status = models.CharField(max_length=20, choices=CLAIM_STATUS_CHOICES, default='PENDING')
    finder_notes = models.TextField(blank=True, help_text="Notes from finder or meeting point instructions")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('item', 'claimant')

    def __str__(self):
        return f"Claim by {self.claimant.username} on {self.item.title} ({self.status})"
