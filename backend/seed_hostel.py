import os, django, random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from hostel.models import Hostel, Room, HostelStudent, RoomAllocation, HostelFee, MaintenanceRequest, VisitorEntry
from datetime import date, timedelta, datetime
from django.utils import timezone

print("Seeding hostel data...")

# Hostels
hostels_data = [
    ('Nehru Boys Hostel', 'boys', 60, 4, 'Mr. Ramesh Kumar', '9876500001', 'ramesh@college.edu'),
    ('Sarojini Girls Hostel', 'girls', 50, 3, 'Mrs. Priya Devi', '9876500002', 'priya@college.edu'),
    ('Ambedkar Mixed Hostel', 'mixed', 40, 2, 'Mr. Suresh Babu', '9876500003', 'suresh@college.edu'),
]
hostels = []
for name, gender, rooms, floors, warden, mobile, email in hostels_data:
    h, _ = Hostel.objects.get_or_create(name=name, defaults={
        'gender': gender, 'total_rooms': rooms, 'floors': floors,
        'warden_name': warden, 'warden_mobile': mobile, 'warden_email': email,
        'address': 'College Campus, Main Road', 'amenities': 'WiFi,Hot Water,Laundry,Gym',
    })
    hostels.append(h)

# Rooms
blocks = ['A', 'B', 'C']
room_types = ['single', 'double', 'triple']
for hostel in hostels:
    for floor in range(1, hostel.floors + 1):
        for block in blocks[:2]:
            for num in range(1, 6):
                rnum = f"{block}{floor}{num:02d}"
                rtype = random.choice(room_types)
                cap = {'single': 1, 'double': 2, 'triple': 3}[rtype]
                Room.objects.get_or_create(hostel=hostel, room_number=rnum, defaults={
                    'block': block, 'floor': floor, 'room_type': rtype,
                    'capacity': cap, 'status': 'available',
                    'monthly_fee': random.choice([2500, 3000, 3500, 4000]),
                })

# Students
students_data = [
    ('Arun Kumar', 'H2021001', 'Computer Science', 3, '9876541001'),
    ('Priya Sharma', 'H2021002', 'Electronics', 3, '9876541002'),
    ('Karthik M', 'H2022003', 'Mechanical', 2, '9876541003'),
    ('Divya R', 'H2022004', 'Computer Science', 2, '9876541004'),
    ('Suresh K', 'H2023005', 'Electrical', 1, '9876541005'),
    ('Anitha V', 'H2021006', 'Computer Science', 3, '9876541006'),
    ('Ravi S', 'H2023007', 'Mechanical', 1, '9876541007'),
    ('Lakshmi P', 'H2022008', 'Electronics', 2, '9876541008'),
    ('Vijay T', 'H2021009', 'Civil', 3, '9876541009'),
    ('Meena G', 'H2023010', 'Computer Science', 1, '9876541010'),
]
students = []
for name, roll, dept, year, mobile in students_data:
    s, _ = HostelStudent.objects.get_or_create(roll_number=roll, defaults={
        'name': name, 'department': dept, 'year': year, 'mobile': mobile,
        'email': f"{roll.lower()}@college.edu",
        'emergency_contact_name': 'Parent', 'emergency_contact_mobile': '9000000000',
        'emergency_contact_relation': 'Father',
    })
    students.append(s)

# Allocations
rooms_list = list(Room.objects.filter(status='available'))
random.shuffle(rooms_list)
for i, student in enumerate(students[:8]):
    if not student.allocations.filter(is_active=True).exists() and i < len(rooms_list):
        room = rooms_list[i]
        if room.available_beds > 0:
            RoomAllocation.objects.get_or_create(student=student, room=room, is_active=True, defaults={
                'hostel': room.hostel, 'check_in_date': date.today() - timedelta(days=random.randint(10, 90)),
                'allocated_by': 'Admin',
            })
            room.status = 'occupied'
            room.save()

# Fees
months = ['January 2025', 'February 2025', 'March 2025', 'April 2025', 'May 2025', 'June 2025']
statuses = ['paid', 'paid', 'paid', 'pending', 'overdue', 'pending']
for student in students:
    alloc = student.allocations.filter(is_active=True).first()
    if alloc:
        for month, status in zip(months, statuses):
            HostelFee.objects.get_or_create(student=student, month=month, defaults={
                'hostel': alloc.hostel, 'amount': alloc.room.monthly_fee,
                'due_date': date.today() - timedelta(days=random.randint(0, 30)),
                'status': status,
                'paid_date': date.today() - timedelta(days=random.randint(1, 20)) if status == 'paid' else None,
            })

# Maintenance Requests
categories = ['fan', 'water', 'electricity', 'wifi', 'furniture', 'cleaning']
statuses_m = ['pending', 'in_progress', 'resolved', 'pending', 'resolved']
for i, student in enumerate(students[:6]):
    alloc = student.allocations.filter(is_active=True).first()
    if alloc:
        MaintenanceRequest.objects.get_or_create(
            student=student, category=categories[i % len(categories)],
            defaults={
                'hostel': alloc.hostel, 'room': alloc.room,
                'description': f'{categories[i % len(categories)].title()} issue in room {alloc.room.room_number}',
                'priority': random.choice(['low', 'medium', 'high']),
                'status': statuses_m[i % len(statuses_m)],
            }
        )

# Visitors
relations = ['Father', 'Mother', 'Brother', 'Sister', 'Uncle']
vstatus = ['approved', 'pending', 'checked_out', 'approved', 'pending']
for i, student in enumerate(students[:5]):
    alloc = student.allocations.filter(is_active=True).first()
    if alloc:
        VisitorEntry.objects.get_or_create(
            student=student, visitor_name=f"Visitor of {student.name.split()[0]}",
            defaults={
                'hostel': alloc.hostel, 'relation': relations[i],
                'visitor_mobile': '9000000001',
                'purpose': 'Family visit',
                'in_time': timezone.now() - timedelta(hours=random.randint(1, 5)),
                'status': vstatus[i],
                'approved_by': 'Warden' if vstatus[i] != 'pending' else '',
            }
        )

print("Hostel seed data created successfully!")
