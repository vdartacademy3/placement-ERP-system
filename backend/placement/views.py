from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count, Q, Avg
from django.db.models.functions import TruncMonth
import re
from .models import Company, Student, PlacementDrive, JobOpening, Application, Interview, Internship, Resume, PlacementRecord, Notification
from .serializers import (
    CompanySerializer, StudentSerializer, PlacementDriveSerializer,
    JobOpeningSerializer, ApplicationSerializer, InterviewSerializer,
    InternshipSerializer, ResumeSerializer, PlacementRecordSerializer, NotificationSerializer
)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all().order_by('-created_at')
    serializer_class = CompanySerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('-created_at')
    serializer_class = StudentSerializer


class PlacementDriveViewSet(viewsets.ModelViewSet):
    serializer_class = PlacementDriveSerializer

    def get_queryset(self):
        return PlacementDrive.objects.annotate(
            applied_count=Count(
                'company__interviews',
                filter=Q(company__interviews__status='scheduled'),
                distinct=True,
            ),
            selected_count=Count(
                'company__interviews',
                filter=Q(company__interviews__status='completed'),
                distinct=True,
            ),
        ).order_by('-created_at')

    @action(detail=False, methods=['get'], url_path='dashboard-stats')
    def dashboard_stats(self, request):
        qs = PlacementDrive.objects.all()
        total_drives    = qs.count()
        upcoming        = qs.filter(status='upcoming').count()
        ongoing         = qs.filter(status='ongoing').count()
        completed       = qs.filter(status='completed').count()
        total_companies = qs.values('company').distinct().count()

        pr = PlacementRecord.objects.all()
        total_students  = pr.count()
        placed_students = pr.filter(status__in=['placed', 'joined']).count()
        placement_pct   = round((placed_students / total_students * 100), 1) if total_students else 0

        packages = []
        for p in pr.exclude(package='').values_list('package', flat=True):
            nums = re.findall(r'[\d.]+', str(p))
            if nums:
                try: packages.append(float(nums[0]))
                except ValueError: pass
        highest_package = max(packages) if packages else 0

        return Response({
            'total_drives':     total_drives,
            'total_companies':  total_companies,
            'total_students':   total_students,
            'placed_students':  placed_students,
            'placement_pct':    placement_pct,
            'highest_package':  highest_package,
            'upcoming':         upcoming,
            'ongoing':          ongoing,
            'completed':        completed,
        })


class JobOpeningViewSet(viewsets.ModelViewSet):
    queryset = JobOpening.objects.all().order_by('-created_at')
    serializer_class = JobOpeningSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all().order_by('-applied_on')
    serializer_class = ApplicationSerializer

    @action(detail=False, methods=['get'], url_path='student/(?P<student_id>[^/.]+)')
    def by_student(self, request, student_id=None):
        apps = Application.objects.filter(student_id=student_id)
        return Response(self.get_serializer(apps, many=True).data)


class InterviewViewSet(viewsets.ModelViewSet):
    queryset = Interview.objects.all().order_by('-created_at')
    serializer_class = InterviewSerializer

    @action(detail=False, methods=['get'], url_path='student/(?P<student_id>[^/.]+)')
    def by_student(self, request, student_id=None):
        interviews = Interview.objects.filter(student_id=student_id)
        return Response(self.get_serializer(interviews, many=True).data)


class InternshipViewSet(viewsets.ModelViewSet):
    queryset = Internship.objects.all().order_by('-created_at')
    serializer_class = InternshipSerializer

    @action(detail=False, methods=['get'], url_path='student/(?P<student_id>[^/.]+)')
    def by_student(self, request, student_id=None):
        internships = Internship.objects.filter(student_id=student_id)
        return Response(self.get_serializer(internships, many=True).data)


class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all().order_by('-created_at')
    serializer_class = ResumeSerializer

    def create(self, request, *args, **kwargs):
        file = request.FILES.get('resume')
        if not file:
            return Response({'message': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        resume = Resume.objects.create(
            student_id=request.data.get('studentId'),
            file=file,
            file_name=file.name,
            version=request.data.get('version', 1),
        )
        return Response(ResumeSerializer(resume).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='student/(?P<student_id>[^/.]+)')
    def by_student(self, request, student_id=None):
        resumes = Resume.objects.filter(student_id=student_id)
        return Response(self.get_serializer(resumes, many=True).data)


class PlacementRecordPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PlacementRecordViewSet(viewsets.ModelViewSet):
    serializer_class   = PlacementRecordSerializer
    parser_classes     = [MultiPartParser, FormParser, JSONParser]
    filter_backends    = [filters.SearchFilter, filters.OrderingFilter]
    search_fields      = ['student_name', 'register_number', 'company_name', 'department', 'job_role']
    ordering_fields    = ['created_at', 'student_name', 'company_name', 'package', 'cgpa']
    ordering           = ['-created_at']
    pagination_class   = PlacementRecordPagination

    def get_queryset(self):
        qs = PlacementRecord.objects.all()
        dept    = self.request.query_params.get('department')
        company = self.request.query_params.get('company')
        status_ = self.request.query_params.get('status')
        ptype   = self.request.query_params.get('placement_type')
        hiring  = self.request.query_params.get('hiring_status')
        if dept:    qs = qs.filter(department__icontains=dept)
        if company: qs = qs.filter(company_name__icontains=company)
        if status_: qs = qs.filter(status=status_)
        if ptype:   qs = qs.filter(placement_type=ptype)
        if hiring:  qs = qs.filter(hiring_status=hiring)
        return qs

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        qs = PlacementRecord.objects.all()
        total       = qs.count()
        applied     = qs.filter(status='applied').count()
        shortlisted = qs.filter(status='shortlisted').count()
        selected    = qs.filter(status='selected').count()
        placed      = qs.filter(status='placed').count()
        joined      = qs.filter(status='joined').count()
        pending     = qs.filter(status='pending').count()
        rejected    = qs.filter(status='rejected').count()
        eligible    = total - rejected

        total_companies = qs.exclude(company_name='').values('company_name').distinct().count()
        placement_pct   = round(((placed + joined) / eligible * 100), 1) if eligible else 0

        packages = []
        for p in qs.exclude(package='').values_list('package', flat=True):
            nums = re.findall(r'[\d.]+', str(p))
            if nums:
                try: packages.append(float(nums[0]))
                except ValueError: pass
        avg_package     = round(sum(packages) / len(packages), 2) if packages else 0
        highest_package = max(packages) if packages else 0

        by_dept = list(
            qs.values('department')
              .annotate(
                  total=Count('id'),
                  applied=Count('id', filter=Q(status='applied')),
                  shortlisted=Count('id', filter=Q(status='shortlisted')),
                  selected=Count('id', filter=Q(status='selected')),
                  placed=Count('id', filter=Q(status='placed')),
                  joined=Count('id', filter=Q(status='joined')),
                  rejected=Count('id', filter=Q(status='rejected')),
              )
              .order_by('-total')
        )

        by_company = list(
            qs.exclude(company_name='')
              .values('company_name')
              .annotate(
                  total=Count('id'),
                  placed=Count('id', filter=Q(status__in=['placed', 'joined'])),
              )
              .order_by('-placed')[:10]
        )

        monthly = list(
            qs.annotate(month=TruncMonth('created_at'))
              .values('month')
              .annotate(count=Count('id'),
                        placed=Count('id', filter=Q(status__in=['placed', 'joined'])))
              .order_by('month')
        )
        monthly_data = [
            {'month': m['month'].strftime('%b %Y'), 'total': m['count'], 'placed': m['placed']}
            for m in monthly if m['month']
        ]

        by_status = list(qs.values('status').annotate(count=Count('id')))
        by_type   = list(qs.values('placement_type').annotate(count=Count('id')))

        return Response({
            'total': total,
            'total_companies': total_companies,
            'applied': applied,
            'shortlisted': shortlisted,
            'selected': selected,
            'placed': placed,
            'joined': joined,
            'pending': pending,
            'rejected': rejected,
            'eligible': eligible,
            'placement_percentage': placement_pct,
            'avg_package': avg_package,
            'highest_package': highest_package,
            'by_department': by_dept,
            'by_company': by_company,
            'by_status': by_status,
            'by_type': by_type,
            'monthly_trend': monthly_data,
        })


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all().order_by('-created_at')
    serializer_class = NotificationSerializer

    @action(detail=False, methods=['post'], url_path='mark-all-read')
    def mark_all_read(self, request):
        Notification.objects.filter(is_read=False).update(is_read=True)
        return Response({'message': 'All notifications marked as read'})


@api_view(['GET', 'PUT'])
def user_profile(request):
    if request.method == 'GET':
        return Response({'username': 'admin', 'name': 'Admin', 'email': 'admin@example.com', 'role': 'Admin'})
    return Response({'message': 'Profile updated'})
