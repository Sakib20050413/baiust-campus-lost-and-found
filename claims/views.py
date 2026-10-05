from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from items.models import Item
from .models import ClaimRequest
from .forms import ClaimSubmissionForm, ClaimReviewForm

@login_required
def submit_claim(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    # Cannot claim own item
    if item.reported_by == request.user:
        messages.warning(request, "You reported this item yourself.")
        return redirect('items:detail', pk=item.id)

    # Can only claim FOUND items
    if item.item_type != 'FOUND':
        messages.error(request, "Claims can only be filed against Found items.")
        return redirect('items:detail', pk=item.id)

    # Prevent duplicate claims by same user
    existing_claim = ClaimRequest.objects.filter(item=item, claimant=request.user).first()
    if existing_claim:
        messages.info(request, "You have already submitted a claim for this item. You can track its status below.")
        return redirect('claims:detail', pk=existing_claim.id)

    if request.method == 'POST':
        form = ClaimSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.item = item
            claim.claimant = request.user
            claim.save()
            messages.success(request, "Your claim request has been submitted to the finder for verification.")
            return redirect('claims:detail', pk=claim.id)
    else:
        form = ClaimSubmissionForm()

    return render(request, 'claims/claim_form.html', {
        'form': form,
        'item': item,
    })

@login_required
def claim_detail(request, pk):
    claim = get_object_or_404(ClaimRequest.objects.select_related('item', 'claimant__profile', 'item__reported_by__profile'), pk=pk)

    # Only claimant or item finder (or staff) can view claim details
    if request.user != claim.claimant and request.user != claim.item.reported_by and not request.user.is_staff:
        messages.error(request, "You are not authorized to view this claim.")
        return redirect('accounts:dashboard')

    is_finder = (request.user == claim.item.reported_by or request.user.is_staff)

    if request.method == 'POST' and is_finder:
        review_form = ClaimReviewForm(request.POST, instance=claim)
        if review_form.is_valid():
            updated_claim = review_form.save()
            
            # If accepted, update the Item status to RETURNED
            if updated_claim.status == 'ACCEPTED':
                item = updated_claim.item
                item.status = 'RETURNED'
                item.save(update_fields=['status'])
                messages.success(request, f"Claim accepted! The item is now marked as Returned/Resolved. Contact information has been unlocked for the claimant.")
            elif updated_claim.status == 'REJECTED':
                messages.info(request, "The claim has been rejected.")
            
            return redirect('claims:detail', pk=claim.id)
    else:
        review_form = ClaimReviewForm(instance=claim) if is_finder else None

    return render(request, 'claims/claim_detail.html', {
        'claim': claim,
        'is_finder': is_finder,
        'review_form': review_form,
    })
