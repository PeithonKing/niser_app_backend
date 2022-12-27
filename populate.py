import sys
import os
import django

sys.path.append('niser_app')
os.environ['DJANGO_SETTINGS_MODULE'] = 'niser_app.settings'
django.setup()


# CANTEEN MENU

from canteen_menu.models import Canteen, FoodItem

canteens = ['Mahanadi', 'Brahmaputra', 'Kaveri', 'Rushikulya']
if not Canteen.objects.all():
    print("Adding canteens in the database:")
    for canteen in canteens:
        item = Canteen(name = canteen)
        item.save()
        print(f"\tAdded {item}")
else: print('There are already some Canteen objects in the database. Skipping...')

foods = [
    ('Biriyani', 75, Canteen.objects.get(name='Mahanadi')),
    ('Biriyani', 75, Canteen.objects.get(name='Kaveri')),
    ('Chhole Bhature', 30, Canteen.objects.get(name='Kaveri')),
]
if not FoodItem.objects.all():
    print("Adding FoodItem in the database:")
    for name, price, cooked_in in foods:
        item = FoodItem(name=name, price=price, cooked_in=cooked_in)
        item.save()
        print(f"\tAdded {item}")
else: print('There are already some FoodItem objects in the database. Skipping...')





# LISTINGS

from listings.models import Condition, Location, ListingType

conditions = ['Like New', 'Very Good', 'Good', 'Acceptable']
if not Condition.objects.all():
    print("Adding Conditions in the database:")
    for condition in conditions:
        item = Condition(condition = condition)
        item.save()
        print(f"\tAdded {item}")   
else:print('There are already some Condition objects in the database. Skipping...')

locations = [
    'Krishna Hostel (DoH 1)',
    'Bhagirathi Hostel (DoH 2)',
    'Brahmaputra Hostel (DoH 3)',
    'Ganga Hostel (DoH 4)',
    'Mahanadi Hostel (SoH 1)',
    'Rushikulya Hostel (SoH 2)',
    'Daya Hostel (SoH 3)',
    'Kaveri Hostel (SoH 4)',
    'Yamuna Hostel (SoH 5)',
]
if not Location.objects.all():
    print("Adding Locations in the database:")
    for location in locations:
        items = Location(location = location)
        items.save()
        print(f"\tAdded {items}")
else: print('There are already some Location objects in the database. Skipping...')

categories = [
    'Bags/Luggage',
    'Bicycles',
    'Books',
    'Electronics',
    'Furniture',
    'Gym Equipment',
    'Musical Instruments',
    'Pillow/Mattresses',
    'Sports Equipment',
    'Stationary'
]
if not ListingType.objects.all():
    print("Adding ListingTypes in the database:")
    for category in categories:
        item = ListingType(name = category)
        item.save()
        print(f"\tAdded {item}")
else: print('There are already some ListingType objects in the database. Skipping...')





# TIMETABLE
# ...





# USERs
from my_user.models import School, Batch

schools = [
    ("SPS", "School of Physical Sciences"),
    ("SBS", "School of Biological Sciences"),
    ("SCS", "School of Chemical Sciences"),
    ("SMS", "School of Mathematical Sciences"),
    ("CMRP", "Center for Medical and Radiational Physics"),
    ("SEPS", "School of Earth and Planetary Sciences"),
    ("SHSS", "School of Humanities and Social Sciences"),
    ("SCPS", "School of Computer Sciences")
]
if not School.objects.all():
    print("Adding Schools in the database:")
    for school in schools:
        item = School(abbr=school[0], name = school[1])
        item.save()
        print(f"\tAdded {item}")
else: print('There are already some School objects in the database. Skipping...')

batches = list(range(18, 24))
if not Batch.objects.all():
    print("Adding Batches in the database:")
    for batch in batches:
        item = Batch(name = batch)
        item.save()
        print(f"\tAdded {item}")
else: print('There are already some Batch objects in the database. Skipping...')