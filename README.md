# BAIUST Campus Lost & Found System
**Department of Computer Science & Engineering (CSE)**  
**Bangladesh Army International University of Science and Technology (BAIUST)**

An automated campus web application built with Django and Bootstrap 5 to report, track, match, and securely claim lost and found items across BAIUST buildings, labs, halls, and buses.

---

## Key Features

1. **BAIUST Authentication & Profiles (`accounts` app)**
   - Student/Staff ID validation, academic department picker (CSE, EEE, CE, BBA, ENG, LAW), phone and WhatsApp contact numbers.
   - User Activity Dashboard showing:
     - My Reported Lost Items
     - My Reported Found Items
     - My Claims Filed
     - Incoming Claims from other students to review

2. **Campus Lost & Found Directory (`items` app)**
   - Item types: `LOST` vs `FOUND`.
   - Categories: Electronics, Student ID & Cards, Books & Notebooks, Wallets, Bags, Keys, Documents, Clothing, etc.
   - Specific BAIUST locations: Academic Building 1 & 2, Central Library, Main Cafeteria, Boys & Girls Halls, Computer Labs 1-4, EEE Lab, Campus Buses, Mosque Area, Gate/Reception.
   - Custody tracking (e.g. "Deposited at Dept Office", "With Finder", "Security Office").
   - Found item privacy verification question (e.g., "What sticker is on the back?").

3. **Multi-Factor Campus Matching Algorithm (`items/matching.py`)**
   - Automatically computes similarity between LOST and FOUND items using a weighted 0% - 100% scoring model:
     - **Category Match (30%)**: Must match item type.
     - **Location Match (25%)**: Exact or sub-spot text match.
     - **Date Proximity (15%)**: Items within 0-14 days.
     - **Keyword & Text Similarity (30%)**: Token overlap & sequence matching on title and description.
   - Instantly alerts students upon report submission if a match score >= 50% is detected.

4. **Claim Verification & Secure Handover (`claims` app)**
   - Claimants must answer the finder's secret question and can optionally upload a photo proof (e.g., matching receipt, previous photo, ID).
   - **Privacy Protection**: Contact phone numbers remain hidden until the finder accepts the claim.
   - Once verified, status updates to `RETURNED` and the item is archived from active public browsing.

5. **Production & Deployment Ready**
   - Configured with `whitenoise` for static file serving.
   - `python-dotenv` and `dj-database-url` for environment-driven database and secret keys.
   - Ready for Render, Railway, or PythonAnywhere.

---

## Quickstart Instructions

### 1. Requirements
Ensure Python 3.10+ is installed.

### 2. Setup Virtual Environment & Install Dependencies
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Run Migrations & Populate Campus Demo Data
```bash
python manage.py migrate
python seed_data.py
```

### 4. Run Development Server
```bash
python manage.py runserver
```
Visit: `http://127.0.0.1:8000/`

---

## Demo Accounts (Populated by `seed_data.py`)

| Role | Username | Password | Notes |
| :--- | :--- | :--- | :--- |
| **Admin / Staff** | `admin_user` | `baiust123` | Django Admin access at `/admin/` |
| **Student (CSE)** | `tanvir` | `baiust123` | Reported Casio calculator found in Room 304 |
| **Student (CSE)** | `sadia` | `baiust123` | Reported lost Casio calculator (Matches Tanvir's item) |
| **Student (EEE)** | `rahim` | `baiust123` | Reported Student ID card found in Cafeteria |
