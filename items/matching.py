import re
from difflib import SequenceMatcher

def clean_text(text):
    if not text:
        return ""
    # Lowercase and remove punctuation
    cleaned = re.sub(r'[^\w\s]', ' ', text.lower())
    return " ".join(cleaned.split())

def calculate_token_overlap(text1, text2):
    tokens1 = set(clean_text(text1).split())
    tokens2 = set(clean_text(text2).split())
    if not tokens1 or not tokens2:
        return 0.0
    common = tokens1.intersection(tokens2)
    # Jaccard index similarity
    return len(common) / len(tokens1.union(tokens2))

def compute_item_similarity(item1, item2):
    # Rule 1: Category Match (30%)
    if item1.category_id == item2.category_id:
        category_score = 30.0
    else:
        category_score = 0.0

    # Rule 2: Campus Location Match (25%)
    if item1.location == item2.location:
        location_score = 25.0
    elif clean_text(item1.location) in clean_text(item2.specific_location_details) or clean_text(item2.location) in clean_text(item1.specific_location_details):
        location_score = 15.0
    else:
        location_score = 0.0

    # Rule 3: Date Proximity (15%)
    # Items found or lost within 10 days of each other
    date_score = 0.0
    if item1.date_occurred and item2.date_occurred:
        day_diff = abs((item1.date_occurred - item2.date_occurred).days)
        if day_diff == 0:
            date_score = 15.0
        elif day_diff <= 3:
            date_score = 12.0
        elif day_diff <= 7:
            date_score = 8.0
        elif day_diff <= 14:
            date_score = 4.0
        else:
            date_score = 0.0

    # Rule 4: Text Similarity across Title & Description (30%)
    title_seq = SequenceMatcher(None, clean_text(item1.title), clean_text(item2.title)).ratio()
    title_overlap = calculate_token_overlap(item1.title, item2.title)
    title_combined = max(title_seq, title_overlap)

    desc_seq = SequenceMatcher(None, clean_text(item1.description), clean_text(item2.description)).ratio()
    desc_overlap = calculate_token_overlap(item1.description, item2.description)
    desc_combined = max(desc_seq, desc_overlap)

    text_similarity_raw = (title_combined * 0.7) + (desc_combined * 0.3)
    text_score = text_similarity_raw * 30.0

    total_score = round(category_score + location_score + date_score + text_score, 1)

    return {
        'total_score': min(total_score, 100.0),
        'category_score': category_score,
        'location_score': location_score,
        'date_score': date_score,
        'text_score': round(text_score, 1),
    }

def find_candidate_matches(target_item, min_score=45.0, limit=10):
    from .models import Item

    # Opposite type candidates (LOST searches FOUND, FOUND searches LOST)
    target_opposite = 'FOUND' if target_item.item_type == 'LOST' else 'LOST'
    
    candidates = Item.objects.filter(
        item_type=target_opposite,
        category=target_item.category
    ).exclude(id=target_item.id).exclude(status='RETURNED')

    matched_results = []
    for cand in candidates:
        match_data = compute_item_similarity(target_item, cand)
        if match_data['total_score'] >= min_score:
            matched_results.append({
                'item': cand,
                'score': match_data['total_score'],
                'details': match_data
            })

    matched_results.sort(key=lambda x: x['score'], reverse=True)
    return matched_results[:limit]
