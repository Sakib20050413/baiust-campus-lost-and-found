# Module: Item Management & Campus Search
# Contributor: Nesar Uddin Ifag (Ifag-codes)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Item, Category, CAMPUS_LOCATIONS
from .forms import ItemForm
from .matching import find_candidate_matches, compute_item_similarity

def home(request):
    recent_lost = Item.objects.filter(item_type='LOST').exclude(status='RETURNED')[:6]
    recent_found = Item.objects.filter(item_type='FOUND').exclude(status='RETURNED')[:6]
    recent_returned = Item.objects.filter(status='RETURNED')[:4]
    
    return render(request, 'items/home.html', {
        'recent_lost': recent_lost,
        'recent_found': recent_found,
        'recent_returned': recent_returned,
    })

def item_list(request):
    items_qs = Item.objects.all().select_related('category', 'reported_by')

    # Filters
    q = request.GET.get('q', '').strip()
    item_type = request.GET.get('type', '').strip()
    category_id = request.GET.get('category', '').strip()
    location = request.GET.get('location', '').strip()
    status = request.GET.get('status', '').strip()

    if q:
        items_qs = items_qs.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(specific_location_details__icontains=q)
        )

    if item_type in ['LOST', 'FOUND']:
        items_qs = items_qs.filter(item_type=item_type)

    if category_id:
        items_qs = items_qs.filter(category_id=category_id)

    if location:
        items_qs = items_qs.filter(location=location)

    if status:
        items_qs = items_qs.filter(status=status)
    else:
        # By default exclude returned items from active exploration
        if not request.GET.get('include_returned'):
            items_qs = items_qs.exclude(status='RETURNED')

    paginator = Paginator(items_qs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, 'items/item_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'locations': CAMPUS_LOCATIONS,
        'selected_q': q,
        'selected_type': item_type,
        'selected_category': category_id,
        'selected_location': location,
        'selected_status': status,
    })

def item_detail(request, pk):
    item = get_object_or_404(Item.objects.select_related('category', 'reported_by__profile'), pk=pk)
    
    # Compute potential matches for this item
    matches = find_candidate_matches(item, min_score=45.0, limit=4)
    
    # Check if current user has already claimed this item
    user_has_claimed = False
    if request.user.is_authenticated:
        from claims.models import ClaimRequest
        user_has_claimed = ClaimRequest.objects.filter(item=item, claimant=request.user).exists()

    return render(request, 'items/item_detail.html', {
        'item': item,
        'matches': matches,
        'user_has_claimed': user_has_claimed,
    })

@login_required
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.reported_by = request.user
            new_item.save()

            messages.success(request, f"'{new_item.title}' has been successfully reported!")

            # Check matches immediately to alert student
            candidate_matches = find_candidate_matches(new_item, min_score=50.0, limit=3)
            if candidate_matches:
                new_item.status = 'MATCHED'
                new_item.save(update_fields=['status'])
                messages.warning(request, f"We found {len(candidate_matches)} potential match(es) for your item! Check the details below.")
                return redirect('items:match_suggestions', pk=new_item.pk)

            return redirect('items:detail', pk=new_item.pk)
    else:
        initial_type = request.GET.get('type', 'LOST')
        form = ItemForm(initial={'item_type': initial_type})

    return render(request, 'items/item_form.html', {
        'form': form,
        'title': 'Report an Item',
    })

@login_required
def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if item.reported_by != request.user and not request.user.is_staff:
        messages.error(request, "You do not have permission to edit this listing.")
        return redirect('items:detail', pk=pk)

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item listing updated successfully.")
            return redirect('items:detail', pk=item.pk)
    else:
        form = ItemForm(instance=item)

    return render(request, 'items/item_form.html', {
        'form': form,
        'title': f"Edit: {item.title}",
        'item': item,
    })

@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if item.reported_by != request.user and not request.user.is_staff:
        messages.error(request, "You cannot delete this item.")
        return redirect('items:detail', pk=pk)

    if request.method == 'POST':
        title = item.title
        item.delete()
        messages.success(request, f"Item '{title}' was removed.")
        return redirect('accounts:dashboard')

    return render(request, 'items/item_confirm_delete.html', {'item': item})

def match_suggestions(request, pk):
    item = get_object_or_404(Item, pk=pk)
    matches = find_candidate_matches(item, min_score=40.0, limit=8)

    return render(request, 'items/matches.html', {
        'target_item': item,
        'matches': matches,
    })
