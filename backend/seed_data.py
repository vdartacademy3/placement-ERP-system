"""
Seed script — populates PlacementRecord and PlacementDrive with realistic data.
Run: python seed_data.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placement_backend.settings')
django.setup()

from placement.models import PlacementRecord, PlacementDrive, Company

# ── Clear existing seed data (safe — only deletes if records exist) ──
print("Clearing existing data...")
PlacementRecord.objects.all().delete()
PlacementDrive.objects.all().delete()
Company.objects.all().delete()

# ── Companies ──
print("Creating companies...")
companies_data = [
    {"name": "TCS",          "industry": "IT Services",    "location": "Pan India",   "website": "https://tcs.com"},
    {"name": "Infosys",      "industry": "IT Services",    "location": "Bangalore",   "website": "https://infosys.com"},
    {"name": "Wipro",        "industry": "IT Services",    "location": "Hyderabad",   "website": "https://wipro.com"},
    {"name": "Cognizant",    "industry": "IT Services",    "location": "Chennai",     "website": "https://cognizant.com"},
    {"name": "Accenture",    "industry": "Consulting",     "location": "Mumbai",      "website": "https://accenture.com"},
    {"name": "Capgemini",    "industry": "IT Services",    "location": "Pune",        "website": "https://capgemini.com"},
    {"name": "HCLTech",      "industry": "IT Services",    "location": "Noida",       "website": "https://hcltech.com"},
    {"name": "Tech Mahindra","industry": "IT Services",    "location": "Pune",        "website": "https://techmahindra.com"},
    {"name": "Zoho",         "industry": "SaaS",           "location": "Chennai",     "website": "https://zoho.com"},
    {"name": "IBM",          "industry": "Technology",     "location": "Bangalore",   "website": "https://ibm.com"},
    {"name": "Deloitte",     "industry": "Consulting",     "location": "Hyderabad",   "website": "https://deloitte.com"},
    {"name": "Microsoft",    "industry": "Technology",     "location": "Hyderabad",   "website": "https://microsoft.com"},
    {"name": "Amazon",       "industry": "E-Commerce",     "location": "Bangalore",   "website": "https://amazon.com"},
    {"name": "Google",       "industry": "Technology",     "location": "Bangalore",   "website": "https://google.com"},
]
companies = {}
for c in companies_data:
    obj = Company.objects.create(**c)
    companies[c["name"]] = obj
print(f"  Created {len(companies)} companies")

# ── Placement Drives ──
print("Creating placement drives...")
drives_data = [
    {"title": "TCS NQT 2025",           "company": "TCS",          "drive_date": "2025-07-10", "job_role": "System Engineer",           "package": "3.36 LPA", "status": "upcoming",  "eligibility_criteria": "CGPA >= 6.0, No active backlogs"},
    {"title": "Infosys Instep 2025",    "company": "Infosys",      "drive_date": "2025-07-15", "job_role": "Systems Engineer",          "package": "3.6 LPA",  "status": "upcoming",  "eligibility_criteria": "CGPA >= 6.5, 60% throughout"},
    {"title": "Wipro WILP 2025",        "company": "Wipro",        "drive_date": "2025-06-28", "job_role": "Project Engineer",          "package": "3.5 LPA",  "status": "ongoing",   "eligibility_criteria": "CGPA >= 6.0, No backlogs"},
    {"title": "Cognizant GenC 2025",    "company": "Cognizant",    "drive_date": "2025-06-20", "job_role": "Programmer Analyst",        "package": "4.0 LPA",  "status": "ongoing",   "eligibility_criteria": "CGPA >= 6.5, 60% in X & XII"},
    {"title": "Accenture ASE 2025",     "company": "Accenture",    "drive_date": "2025-05-30", "job_role": "Associate Software Eng",    "package": "4.5 LPA",  "status": "completed", "eligibility_criteria": "CGPA >= 7.0, No backlogs"},
    {"title": "Capgemini Analyst 2025", "company": "Capgemini",    "drive_date": "2025-05-18", "job_role": "Analyst",                   "package": "3.8 LPA",  "status": "completed", "eligibility_criteria": "CGPA >= 6.0, 60% throughout"},
    {"title": "HCLTech GET 2025",       "company": "HCLTech",      "drive_date": "2025-07-22", "job_role": "Graduate Engineer Trainee", "package": "3.5 LPA",  "status": "upcoming",  "eligibility_criteria": "CGPA >= 6.0, No active backlogs"},
    {"title": "Tech Mahindra SWE 2025", "company": "Tech Mahindra","drive_date": "2025-06-25", "job_role": "Software Engineer",         "package": "3.25 LPA", "status": "ongoing",   "eligibility_criteria": "CGPA >= 5.5, 55% throughout"},
    {"title": "Zoho MTS 2025",          "company": "Zoho",         "drive_date": "2025-05-10", "job_role": "Member Technical Staff",    "package": "6.0 LPA",  "status": "completed", "eligibility_criteria": "CGPA >= 7.5, Strong DSA skills"},
    {"title": "IBM AppDev 2025",        "company": "IBM",          "drive_date": "2025-07-05", "job_role": "Application Developer",     "package": "4.5 LPA",  "status": "upcoming",  "eligibility_criteria": "CGPA >= 7.0, No backlogs"},
    {"title": "Deloitte Analyst 2025",  "company": "Deloitte",     "drive_date": "2025-06-15", "job_role": "Analyst",                   "package": "7.0 LPA",  "status": "ongoing",   "eligibility_criteria": "CGPA >= 7.5, 65% throughout"},
    {"title": "Microsoft SDE 2025",     "company": "Microsoft",    "drive_date": "2025-05-05", "job_role": "Software Development Eng",  "package": "40.0 LPA", "status": "completed", "eligibility_criteria": "CGPA >= 8.5, Exceptional coding"},
    {"title": "Amazon SDE1 2025",       "company": "Amazon",       "drive_date": "2025-05-20", "job_role": "SDE-1",                     "package": "32.0 LPA", "status": "completed", "eligibility_criteria": "CGPA >= 8.0, Strong DSA"},
    {"title": "Google SWE 2025",        "company": "Google",       "drive_date": "2025-04-28", "job_role": "Software Engineer",         "package": "45.0 LPA", "status": "completed", "eligibility_criteria": "CGPA >= 9.0, Top competitive coders"},
]
for d in drives_data:
    PlacementDrive.objects.create(
        title=d["title"],
        company=companies[d["company"]],
        drive_date=d["drive_date"],
        job_role=d["job_role"],
        package=d["package"],
        status=d["status"],
        eligibility_criteria=d["eligibility_criteria"],
    )
print(f"  Created {len(drives_data)} placement drives")

# ── Placement Records ──
print("Creating placement records...")
records = [
    # TCS — placed/joined
    {"student_name": "Arun Kumar",      "register_number": "STU2026001", "department": "CSE", "year": 4, "email": "arun@college.edu",      "phone": "9876543201", "cgpa": 7.8, "company_name": "TCS",          "job_role": "System Engineer",           "package": "3.36 LPA", "placement_type": "fulltime", "work_mode": "onsite",  "status": "placed",      "hiring_status": "closed", "location": "Chennai"},
    {"student_name": "Priya Sharma",    "register_number": "STU2026002", "department": "ECE", "year": 4, "email": "priya@college.edu",      "phone": "9876543202", "cgpa": 8.1, "company_name": "Infosys",      "job_role": "Systems Engineer",          "package": "3.6 LPA",  "placement_type": "fulltime", "work_mode": "hybrid",  "status": "joined",      "hiring_status": "closed", "location": "Bangalore"},
    {"student_name": "Rahul Verma",     "register_number": "STU2026003", "department": "CSE", "year": 4, "email": "rahul@college.edu",      "phone": "9876543203", "cgpa": 9.2, "company_name": "Google",       "job_role": "Software Engineer",         "package": "45.0 LPA", "placement_type": "fulltime", "work_mode": "onsite",  "status": "joined",      "hiring_status": "closed", "location": "Bangalore"},
    {"student_name": "Sneha Patel",     "register_number": "STU2026004", "department": "IT",  "year": 4, "email": "sneha@college.edu",      "phone": "9876543204", "cgpa": 8.5, "company_name": "Amazon",       "job_role": "SDE-1",                     "package": "32.0 LPA", "placement_type": "fulltime", "work_mode": "onsite",  "status": "placed",      "hiring_status": "closed", "location": "Bangalore"},
    {"student_name": "Karthik Raja",    "register_number": "STU2026005", "department": "CSE", "year": 4, "email": "karthik@college.edu",    "phone": "9876543205", "cgpa": 8.9, "company_name": "Microsoft",    "job_role": "Software Development Eng",  "package": "40.0 LPA", "placement_type": "fulltime", "work_mode": "onsite",  "status": "joined",      "hiring_status": "closed", "location": "Hyderabad"},
    {"student_name": "Divya Nair",      "register_number": "STU2026006", "department": "EEE", "year": 4, "email": "divya@college.edu",      "phone": "9876543206", "cgpa": 7.2, "company_name": "Wipro",        "job_role": "Project Engineer",          "package": "3.5 LPA",  "placement_type": "fulltime", "work_mode": "onsite",  "status": "selected",    "hiring_status": "open",   "location": "Hyderabad"},
    {"student_name": "Manoj Singh",     "register_number": "STU2026007", "department": "MECH","year": 4, "email": "manoj@college.edu",      "phone": "9876543207", "cgpa": 6.8, "company_name": "Cognizant",    "job_role": "Programmer Analyst",        "package": "4.0 LPA",  "placement_type": "fulltime", "work_mode": "hybrid",  "status": "shortlisted", "hiring_status": "open",   "location": "Chennai"},
    {"student_name": "Anitha Reddy",    "register_number": "STU2026008", "department": "CSE", "year": 4, "email": "anitha@college.edu",     "phone": "9876543208", "cgpa": 8.3, "company_name": "Deloitte",     "job_role": "Analyst",                   "package": "7.0 LPA",  "placement_type": "fulltime", "work_mode": "hybrid",  "status": "placed",      "hiring_status": "closed", "location": "Hyderabad"},
    {"student_name": "Vijay Mohan",     "register_number": "STU2026009", "department": "IT",  "year": 4, "email": "vijay@college.edu",      "phone": "9876543209", "cgpa": 7.5, "company_name": "Accenture",    "job_role": "Associate Software Eng",    "package": "4.5 LPA",  "placement_type": "fulltime", "work_mode": "hybrid",  "status": "joined",      "hiring_status": "closed", "location": "Mumbai"},
    {"student_name": "Lakshmi Devi",    "register_number": "STU2026010", "department": "ECE", "year": 4, "email": "lakshmi@college.edu",    "phone": "9876543210", "cgpa": 7.9, "company_name": "Capgemini",    "job_role": "Analyst",                   "package": "3.8 LPA",  "placement_type": "fulltime", "work_mode": "onsite",  "status": "placed",      "hiring_status": "closed", "location": "Pune"},
    {"student_name": "Suresh Babu",     "register_number": "STU2026011", "department": "CSE", "year": 4, "email": "suresh@college.edu",     "phone": "9876543211", "cgpa": 7.1, "company_name": "HCLTech",      "job_role": "Graduate Engineer Trainee", "package": "3.5 LPA",  "placement_type": "fulltime", "work_mode": "onsite",  "status": "applied",     "hiring_status": "open",   "location": "Noida"},
    {"student_name": "Meena Kumari",    "register_number": "STU2026012", "department": "IT",  "year": 4, "email": "meena@college.edu",      "phone": "9876543212", "cgpa": 6.5, "company_name": "Tech Mahindra", "job_role": "Software Engineer",         "package": "3.25 LPA", "placement_type": "fulltime", "work_mode": "onsite",  "status": "shortlisted", "hiring_status": "open",   "location": "Pune"},
    {"student_name": "Ravi Shankar",    "register_number": "STU2026013", "department": "CSE", "year": 4, "email": "ravi@college.edu",       "phone": "9876543213", "cgpa": 8.7, "company_name": "Zoho",         "job_role": "Member Technical Staff",    "package": "6.0 LPA",  "placement_type": "fulltime", "work_mode": "onsite",  "status": "joined",      "hiring_status": "closed", "location": "Chennai"},
    {"student_name": "Pooja Iyer",      "register_number": "STU2026014", "department": "ECE", "year": 4, "email": "pooja@college.edu",      "phone": "9876543214", "cgpa": 7.6, "company_name": "IBM",          "job_role": "Application Developer",     "package": "4.5 LPA",  "placement_type": "fulltime", "work_mode": "hybrid",  "status": "applied",     "hiring_status": "open",   "location": "Bangalore"},
    {"student_name": "Deepak Raj",      "register_number": "STU2026015", "department": "MECH","year": 4, "email": "deepak@college.edu",     "phone": "9876543215", "cgpa": 6.2, "company_name": "TCS",          "job_role": "System Engineer",           "package": "3.36 LPA", "placement_type": "fulltime", "work_mode": "onsite",  "status": "rejected",    "hiring_status": "closed", "location": "Chennai"},
    {"student_name": "Kavitha Menon",   "register_number": "STU2026016", "department": "CSE", "year": 4, "email": "kavitha@college.edu",    "phone": "9876543216", "cgpa": 8.0, "company_name": "Infosys",      "job_role": "Systems Engineer",          "package": "3.6 LPA",  "placement_type": "fulltime", "work_mode": "hybrid",  "status": "placed",      "hiring_status": "closed", "location": "Bangalore"},
    {"student_name": "Arjun Das",       "register_number": "STU2026017", "department": "IT",  "year": 4, "email": "arjun@college.edu",      "phone": "9876543217", "cgpa": 7.3, "company_name": "Wipro",        "job_role": "Project Engineer",          "package": "3.5 LPA",  "placement_type": "fulltime", "work_mode": "onsite",  "status": "selected",    "hiring_status": "open",   "location": "Hyderabad"},
    {"student_name": "Nithya Priya",    "register_number": "STU2026018", "department": "EEE", "year": 4, "email": "nithya@college.edu",     "phone": "9876543218", "cgpa": 7.7, "company_name": "Cognizant",    "job_role": "Programmer Analyst",        "package": "4.0 LPA",  "placement_type": "fulltime", "work_mode": "hybrid",  "status": "joined",      "hiring_status": "closed", "location": "Chennai"},
    {"student_name": "Sathish Kumar",   "register_number": "STU2026019", "department": "CSE", "year": 4, "email": "sathish@college.edu",    "phone": "9876543219", "cgpa": 9.0, "company_name": "Amazon",       "job_role": "SDE-1",                     "package": "32.0 LPA", "placement_type": "fulltime", "work_mode": "onsite",  "status": "placed",      "hiring_status": "closed", "location": "Bangalore"},
    {"student_name": "Revathi Suresh",  "register_number": "STU2026020", "department": "ECE", "year": 4, "email": "revathi@college.edu",    "phone": "9876543220", "cgpa": 6.9, "company_name": "Capgemini",    "job_role": "Analyst",                   "package": "3.8 LPA",  "placement_type": "fulltime", "work_mode": "onsite",  "status": "pending",     "hiring_status": "on_hold","location": "Pune"},
    {"student_name": "Harish Babu",     "register_number": "STU2026021", "department": "CSE", "year": 4, "email": "harish@college.edu",     "phone": "9876543221", "cgpa": 8.4, "company_name": "Deloitte",     "job_role": "Analyst",                   "package": "7.0 LPA",  "placement_type": "fulltime", "work_mode": "hybrid",  "status": "shortlisted", "hiring_status": "open",   "location": "Hyderabad"},
    {"student_name": "Sangeetha Raj",   "register_number": "STU2026022", "department": "IT",  "year": 4, "email": "sangeetha@college.edu",  "phone": "9876543222", "cgpa": 7.4, "company_name": "Accenture",    "job_role": "Associate Software Eng",    "package": "4.5 LPA",  "placement_type": "fulltime", "work_mode": "hybrid",  "status": "placed",      "hiring_status": "closed", "location": "Mumbai"},
    {"student_name": "Murugan Pillai",  "register_number": "STU2026023", "department": "MECH","year": 4, "email": "murugan@college.edu",    "phone": "9876543223", "cgpa": 6.6, "company_name": "HCLTech",      "job_role": "Graduate Engineer Trainee", "package": "3.5 LPA",  "placement_type": "fulltime", "work_mode": "onsite",  "status": "applied",     "hiring_status": "open",   "location": "Noida"},
    {"student_name": "Janani Krishnan", "register_number": "STU2026024", "department": "CSE", "year": 4, "email": "janani@college.edu",     "phone": "9876543224", "cgpa": 8.6, "company_name": "Zoho",         "job_role": "Member Technical Staff",    "package": "6.0 LPA",  "placement_type": "fulltime", "work_mode": "onsite",  "status": "selected",    "hiring_status": "open",   "location": "Chennai"},
    {"student_name": "Balaji Raman",    "register_number": "STU2026025", "department": "ECE", "year": 4, "email": "balaji@college.edu",     "phone": "9876543225", "cgpa": 7.0, "company_name": "IBM",          "job_role": "Application Developer",     "package": "4.5 LPA",  "placement_type": "fulltime", "work_mode": "hybrid",  "status": "shortlisted", "hiring_status": "open",   "location": "Bangalore"},
]

for r in records:
    PlacementRecord.objects.create(
        student_name     = r["student_name"],
        register_number  = r["register_number"],
        department       = r["department"],
        year             = r["year"],
        email            = r["email"],
        phone            = r["phone"],
        cgpa             = r["cgpa"],
        company_name     = r["company_name"],
        job_role         = r["job_role"],
        package          = r["package"],
        placement_type   = r["placement_type"],
        work_mode        = r["work_mode"],
        status           = r["status"],
        hiring_status    = r["hiring_status"],
        location         = r["location"],
    )

print(f"  Created {len(records)} placement records")
print("\n✅ Seed complete!")
print(f"   Companies      : {Company.objects.count()}")
print(f"   Drives         : {PlacementDrive.objects.count()}")
print(f"   Records        : {PlacementRecord.objects.count()}")
print(f"   Placed/Joined  : {PlacementRecord.objects.filter(status__in=['placed','joined']).count()}")
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from transport.models import Route, Stop, Driver, Bus, StudentProfile, Trip, Maintenance, FuelLog, Notification
from datetime import date, time, timedelta
import random

print("Seeding database...")

# Superuser / Manager
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser('admin', 'admin@college.edu', 'admin123')
    admin.first_name = 'Transport'
    admin.last_name = 'Manager'
    admin.save()
    print("Created admin user: admin / admin123")

# Routes
routes_data = [
    ('Route A - City Center', 12.5, 45, time(7, 30), time(17, 0)),
    ('Route B - North Campus', 8.2, 30, time(7, 45), time(17, 15)),
    ('Route C - East Zone', 15.0, 55, time(7, 15), time(16, 45)),
    ('Route D - West Hills', 10.8, 40, time(7, 20), time(17, 30)),
    ('Route E - South Bay', 18.3, 65, time(7, 0), time(16, 30)),
]
routes = []
for name, dist, time_min, morning, evening in routes_data:
    r, _ = Route.objects.get_or_create(
        name=name,
        defaults={'distance_km': dist, 'estimated_time_min': time_min, 'morning_timing': morning, 'evening_timing': evening}
    )
    routes.append(r)

# Stops
stops_data = {
    routes[0]: [('Main Gate', 'College Entrance', 11.0168, 76.9558), ('City Bus Stand', 'Near Clock Tower', 11.0200, 76.9600), ('Market Square', 'Big Bazaar', 11.0250, 76.9650), ('Railway Station', 'Platform 1', 11.0300, 76.9700)],
    routes[1]: [('North Gate', 'North Entrance', 11.0100, 76.9500), ('Tech Park', 'IT Hub', 11.0050, 76.9450), ('Residential Area', 'Block C', 11.0000, 76.9400)],
    routes[2]: [('East Stop 1', 'Near Hospital', 11.0200, 77.0000), ('East Stop 2', 'School Road', 11.0250, 77.0050), ('East Stop 3', 'Park Junction', 11.0300, 77.0100)],
    routes[3]: [('West Gate', 'Hills Entrance', 10.9900, 76.9300), ('West Market', 'Shopping Mall', 10.9850, 76.9250)],
    routes[4]: [('South Bay 1', 'Beach Road', 10.9700, 76.9100), ('South Bay 2', 'Fishing Harbor', 10.9650, 76.9050), ('South Bay 3', 'Lighthouse', 10.9600, 76.9000)],
}
all_stops = []
for route, stops in stops_data.items():
    for i, (name, landmark, lat, lng) in enumerate(stops):
        s, _ = Stop.objects.get_or_create(
            route=route, name=name,
            defaults={'landmark': landmark, 'latitude': lat, 'longitude': lng, 'order': i}
        )
        all_stops.append(s)

# Drivers
drivers_data = [
    ('Rajesh Kumar', 'DL-TN-2019-001234', '9876543210', 8),
    ('Murugan S', 'DL-TN-2018-005678', '9876543211', 12),
    ('Selvam P', 'DL-TN-2020-009012', '9876543212', 5),
    ('Arjun Nair', 'DL-TN-2017-003456', '9876543213', 15),
    ('Venkat R', 'DL-TN-2021-007890', '9876543214', 3),
]
drivers = []
for name, lic, mob, exp in drivers_data:
    d, _ = Driver.objects.get_or_create(
        license_number=lic,
        defaults={'name': name, 'mobile': mob, 'experience_years': exp, 'emergency_contact': '9000000000'}
    )
    drivers.append(d)

# Buses
buses_data = [
    ('TN-01-AB-1234', 'KA-01-F-1234', 45, 'available'),
    ('TN-01-AB-5678', 'KA-01-F-5678', 40, 'running'),
    ('TN-01-AB-9012', 'KA-01-F-9012', 50, 'running'),
    ('TN-01-AB-3456', 'KA-01-F-3456', 35, 'maintenance'),
    ('TN-01-AB-7890', 'KA-01-F-7890', 45, 'available'),
]
buses = []
for i, (bus_num, reg, cap, status) in enumerate(buses_data):
    b, _ = Bus.objects.get_or_create(
        bus_number=bus_num,
        defaults={
            'registration_number': reg, 'capacity': cap, 'status': status,
            'driver': drivers[i] if i < len(drivers) else None,
            'route': routes[i] if i < len(routes) else None,
            'insurance_expiry': date.today() + timedelta(days=180),
            'pollution_certificate_expiry': date.today() + timedelta(days=90),
            'last_service_date': date.today() - timedelta(days=random.randint(10, 60)),
            'next_service_date': date.today() + timedelta(days=random.randint(5, 30)),
            'total_mileage_km': random.uniform(5000, 50000),
            'latitude': 11.0168 + random.uniform(-0.05, 0.05),
            'longitude': 76.9558 + random.uniform(-0.05, 0.05),
        }
    )
    buses.append(b)

# Students
student_names = [
    ('Arun', 'Prasad', 'CS2021001', 'Computer Science', 3),
    ('Priya', 'Sharma', 'EC2022002', 'Electronics', 2),
    ('Karthik', 'M', 'ME2021003', 'Mechanical', 3),
    ('Divya', 'R', 'CS2023004', 'Computer Science', 1),
    ('Suresh', 'K', 'EE2022005', 'Electrical', 2),
    ('Anitha', 'V', 'CS2021006', 'Computer Science', 3),
    ('Ravi', 'S', 'ME2023007', 'Mechanical', 1),
    ('Lakshmi', 'P', 'EC2022008', 'Electronics', 2),
]
for i, (fn, ln, roll, dept, year) in enumerate(student_names):
    username = f'student{i+1}'
    if not User.objects.filter(username=username).exists():
        u = User.objects.create_user(username, f'{username}@college.edu', 'student123', first_name=fn, last_name=ln)
        route = routes[i % len(routes)]
        stop = Stop.objects.filter(route=route).first()
        StudentProfile.objects.create(user=u, roll_number=roll, department=dept, year=year, route=route, stop=stop)

# Trips
for bus in buses[:3]:
    for i in range(5):
        trip_date = date.today() - timedelta(days=i)
        from datetime import datetime
        Trip.objects.get_or_create(
            bus=bus, date=trip_date, trip_type='morning',
            defaults={
                'driver': bus.driver, 'route': bus.route,
                'status': random.choice(['completed', 'completed', 'delayed', 'completed']),
                'scheduled_start': datetime.combine(trip_date, time(7, 30)),
                'fuel_used_liters': random.uniform(8, 15),
                'distance_covered_km': random.uniform(10, 20),
            }
        )

# Maintenance
for bus in buses:
    Maintenance.objects.get_or_create(
        bus=bus, scheduled_date=bus.next_service_date or date.today() + timedelta(days=10),
        defaults={
            'maintenance_type': 'routine',
            'description': 'Regular service and oil change',
            'status': 'scheduled',
            'cost': random.uniform(2000, 8000),
        }
    )

# Fuel Logs
for bus in buses:
    for i in range(3):
        liters = round(random.uniform(30, 60), 2)
        cost_per_liter = 95.50
        FuelLog.objects.create(
            bus=bus, liters=liters,
            cost_per_liter=cost_per_liter,
            total_cost=round(liters * cost_per_liter, 2),
            odometer_reading=bus.total_mileage_km + i * 100,
        )

# Notifications
Notification.objects.get_or_create(
    title='Bus Arriving in 10 Minutes',
    defaults={'message': 'Route A bus will arrive at City Bus Stand in 10 minutes.', 'notification_type': 'arrival', 'is_broadcast': True}
)
Notification.objects.get_or_create(
    title='Route B Delayed',
    defaults={'message': 'Route B bus is delayed by 15 minutes due to traffic.', 'notification_type': 'delay', 'is_broadcast': True}
)
Notification.objects.get_or_create(
    title='Holiday Notice',
    defaults={'message': 'No bus service on 26th January (Republic Day).', 'notification_type': 'holiday', 'is_broadcast': True}
)

print("✅ Seed data created successfully!")
print("Login: admin / admin123")
print("Student logins: student1 to student8 / student123")
