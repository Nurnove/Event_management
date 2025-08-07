import os
import django
import random
from faker import Faker
from datetime import timedelta
from django.utils import timezone

# Step 1: Django environment setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

# Step 2: Import models after setup
from events.models import Category, Event, Participant

# Step 3: Initialize Faker
fake = Faker()

def populate():
    print("🧹 Deleting old data...")
    Participant.objects.all().delete()
    Event.objects.all().delete()
    Category.objects.all().delete()

    print("🌱 Creating categories...")
    categories = []
    for _ in range(5):
        cat = Category.objects.create(
            name=fake.word().capitalize(),
            description=fake.sentence()
        )
        categories.append(cat)

    print("📅 Creating events...")
    events = []
    for _ in range(30):
        event = Event.objects.create(
            name=fake.catch_phrase(),
            description=fake.text(max_nb_chars=150),
            date=fake.date_between(start_date='-10d', end_date='+20d'),
            time=fake.time(),
            location=fake.city(),
            category=random.choice(categories)
        )
        events.append(event)

    print("👥 Creating participants...")
    for _ in range(50):
        participant = Participant.objects.create(
            name=fake.name(),
            email=fake.unique.email()
        )
        participant.event.set(random.sample(events, random.randint(1, 5)))

    print("✅ Database populated with fake data!")

# Step 4: Run when executed directly
if __name__ == '__main__':
    populate()
