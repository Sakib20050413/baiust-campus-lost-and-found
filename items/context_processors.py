from .models import Item, Category

def campus_stats(request):
    total_items = Item.objects.count()
    lost_count = Item.objects.filter(item_type='LOST', status__in=['PENDING', 'APPROVED', 'MATCHED']).count()
    found_count = Item.objects.filter(item_type='FOUND', status__in=['PENDING', 'APPROVED', 'MATCHED']).count()
    returned_count = Item.objects.filter(status='RETURNED').count()
    categories = Category.objects.all()
    
    return {
        'stat_total': total_items,
        'stat_lost': lost_count,
        'stat_found': found_count,
        'stat_returned': returned_count,
        'nav_categories': categories,
    }
