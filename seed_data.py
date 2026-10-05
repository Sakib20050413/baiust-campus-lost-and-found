import os
import django
from datetime import date, timedelta
from django.core.files.base import ContentFile
import io
from PIL import Image, ImageDraw

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_lostfound.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile
from items.models import Category, Item
from claims.models import ClaimRequest

def create_sample_image(color=(30, 80, 160), text="BAIUST Item"):
    img = Image.new('RGB', (600, 400), color=color)
    d = ImageDraw.Draw(img)
    # Draw simple bounding box
    d.rectangle([(20, 20), (580, 380)], outline=(255, 255, 255), width=4)
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    return ContentFile(buffer.getvalue())

def seed():
    print("Seeding BAIUST Campus Categories...")
    cats_data = [
        ('Electronics', 'bi-laptop', 'Laptops, mobile devices, chargers, calculators, flash drives'),
        ('Student ID & Cards', 'bi-card-heading', 'BAIUST student ID cards, library cards, bank ATM cards'),
        ('Books & Notebooks', 'bi-book', 'Textbooks, lab manuals, class lecture notebooks'),
        ('Wallets & Money', 'bi-wallet2', 'Wallets, purses, pouches, keys'),
        ('Bags & Backpacks', 'bi-backpack', 'Backpacks, laptop bags, side bags'),
        ('Keys', 'bi-key', 'Bike keys, room keys, locker keys'),
        ('Clothing & Accessories', 'bi-sunglasses', 'Jackets, spectacles, wristwatches, umbrellas'),
        ('Documents', 'bi-file-earmark-text', 'Official transcripts, certificates, admit cards'),
        ('Others', 'bi-box-seam', 'Water bottles, sports gear, general miscellaneous items'),
    ]

    cat_map = {}
    for name, icon, desc in cats_data:
        cat, _ = Category.objects.get_or_create(name=name, defaults={'icon': icon, 'description': desc})
        cat_map[name] = cat

    print("Creating demo users & profiles...")
    users_data = [
        ('tanvir', 'Tanvir', 'Ahmed', 'tanvir@baiust.edu.bd', '1102015', 'CSE', '01711223344', '01711223344'),
        ('sadia', 'Sadia', 'Sultana', 'sadia@baiust.edu.bd', '1102042', 'CSE', '01822334455', '01822334455'),
        ('rahim', 'Rahim', 'Uddin', 'rahim@baiust.edu.bd', '1202019', 'EEE', '01933445566', ''),
        ('admin_user', 'Campus', 'Admin', 'admin@baiust.edu.bd', 'STAFF-01', 'CSE', '01500000000', '01500000000'),
    ]

    user_objs = {}
    for uname, fname, lname, email, sid, dept, phone, wa in users_data:
        u, created = User.objects.get_or_create(username=uname, defaults={'email': email, 'first_name': fname, 'last_name': lname})
        if created:
            u.set_password('baiust123')
            u.is_staff = (uname == 'admin_user')
            u.is_superuser = (uname == 'admin_user')
            u.save()
        profile, _ = UserProfile.objects.get_or_create(user=u, defaults={'student_id': sid, 'department': dept, 'phone_number': phone, 'whatsapp_number': wa})
        user_objs[uname] = u

    print("Creating demo items...")
    # Item 1: Found Calculator
    item1, _ = Item.objects.get_or_create(
        title="Casio fx-991EX ClassWiz Calculator",
        defaults={
            'item_type': 'FOUND',
            'category': cat_map['Electronics'],
            'location': 'Academic Building 1',
            'specific_location_details': 'Room 304, 3rd floor back row bench near window',
            'date_occurred': date.today() - timedelta(days=1),
            'description': 'Black Casio scientific calculator with slightly scratched sliding cover. Has a tiny sticker on the back battery compartment.',
            'secret_mark_question': 'What character/sticker is on the back slide cover?',
            'current_custody': 'Deposited at Dept Office',
            'status': 'APPROVED',
            'reported_by': user_objs['tanvir']
        }
    )
    if not item1.primary_image:
        item1.primary_image.save('casio_fx991ex.jpg', create_sample_image((40, 70, 120), "Casio fx-991EX"), save=True)

    # Item 2: Lost Calculator (Matching Item 1)
    item2, _ = Item.objects.get_or_create(
        title="Casio fx-991EX Scientific Calculator",
        defaults={
            'item_type': 'LOST',
            'category': cat_map['Electronics'],
            'location': 'Academic Building 1',
            'specific_location_details': 'Left during CSE 311 Numerical Methods class in Room 304',
            'date_occurred': date.today() - timedelta(days=1),
            'description': 'Lost my Casio fx-991EX scientific calculator. It has a Batman sticker on the battery cover and faint pencil writing on the inside cover.',
            'status': 'MATCHED',
            'reported_by': user_objs['sadia']
        }
    )
    if not item2.primary_image:
        item2.primary_image.save('lost_casio.jpg', create_sample_image((160, 40, 40), "Lost Calculator"), save=True)

    # Item 3: Found BAIUST Student ID Card
    item3, _ = Item.objects.get_or_create(
        title="BAIUST Student ID Card (Roll 1102042)",
        defaults={
            'item_type': 'FOUND',
            'category': cat_map['Student ID & Cards'],
            'location': 'Main Cafeteria / Canteen',
            'specific_location_details': 'Found on corner dining table near juice counter',
            'date_occurred': date.today() - timedelta(days=2),
            'description': 'Official plastic ID card with green BAIUST ribbon lanyard.',
            'secret_mark_question': 'What is the full name and blood group printed on the card?',
            'current_custody': 'With Finder',
            'status': 'APPROVED',
            'reported_by': user_objs['rahim']
        }
    )
    if not item3.primary_image:
        item3.primary_image.save('student_id_card.jpg', create_sample_image((30, 110, 60), "Student ID Card"), save=True)

    # Item 4: Lost Dell Laptop Charger
    item4, _ = Item.objects.get_or_create(
        title="Dell 65W Type-C Laptop Charger",
        defaults={
            'item_type': 'LOST',
            'category': cat_map['Electronics'],
            'location': 'Computer Lab (Lab 1-4)',
            'specific_location_details': 'Lab 2, plugged into PC Station #14',
            'date_occurred': date.today() - timedelta(days=3),
            'description': 'Black original Dell 65W USB-C barrel charger with black velcro cable tie.',
            'status': 'APPROVED',
            'reported_by': user_objs['tanvir']
        }
    )
    if not item4.primary_image:
        item4.primary_image.save('dell_charger.jpg', create_sample_image((150, 60, 30), "Dell Charger"), save=True)

    print("Demo seed completed successfully!")

if __name__ == '__main__':
    seed()
