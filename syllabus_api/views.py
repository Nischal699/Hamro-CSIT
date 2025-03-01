from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics,status,permissions
from .models import Subject,Syllabus,Chapter,Semester,Course,Note,PastQuestion
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .serializers import SubjectSerializer,SyllabusSerializer,ChapterSerializer,SemesterSerializer,CourseSerializer,NotesSerializer,PastQuestionsSerializer      
from django.urls import reverse
from user.models import CustomUser
from user_api.serializers import UserSerializer
from user_api.permissions import IsAdminUser, IsAdminOrReadOnly

#-----------------------------------------------------------------------------------------------------------------------------------------------
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

@api_view(['GET'])
@permission_classes([IsAuthenticated,IsAdminUser]) 
def apiOverview(request):
    api_urls = {
        "Courses": {
            "List": request.build_absolute_uri(reverse('course-list-api')),
            "Detail View": request.build_absolute_uri(reverse('course-detail-api', args=[1])),
            "Create": request.build_absolute_uri(reverse('course-create-api')),
            "Update": request.build_absolute_uri(reverse('course-update-api', args=[1])),
            "Delete": request.build_absolute_uri(reverse('course-delete-api', args=[1]))
        },
        "Semesters": {
            "List All": request.build_absolute_uri(reverse('semester-list-api')),
            "List by Course": request.build_absolute_uri(reverse('semester-list-by-course-api', args=[1])), 
            "Detail View": request.build_absolute_uri(reverse('semester-detail-api', args=[1])),
            "Create": request.build_absolute_uri(reverse('semester-create-api',args=[1])),
            "Update": request.build_absolute_uri(reverse('semester-update-api', args=[1])),
            "Delete": request.build_absolute_uri(reverse('semester-delete-api', args=[1]))
        },
        "Subjects": {
            "List": request.build_absolute_uri(reverse('subject-list-api')),
            "Detail View": request.build_absolute_uri(reverse('subject-detail-api', args=[1])),
            "Create": request.build_absolute_uri(reverse('subject-create-api',args=[1])),
            "Update": request.build_absolute_uri(reverse('subject-update-api', args=[1])),
            "Delete": request.build_absolute_uri(reverse('subject-delete-api', args=[1]))
        },
        "PastQuestions": {
            "List": request.build_absolute_uri(reverse('pastQuestion-list-api')),
            "Detail View": request.build_absolute_uri(reverse('pastQuestion-detail-api', args=[1])),
            "Create": request.build_absolute_uri(reverse('pastQuestion-create-api',args=[1])),
            "Update": request.build_absolute_uri(reverse('pastQuestion-update-api', args=[1])),
            "Delete": request.build_absolute_uri(reverse('pastQuestion-delete-api', args=[1]))
        },
        "Syllabus": {
            "List": request.build_absolute_uri(reverse('syllabus-list-api')),
            "Detail View": request.build_absolute_uri(reverse('syllabus-detail-api', args=[1])),
            "Create": request.build_absolute_uri(reverse('syllabus-create-api',args=[1])),
            "Update": request.build_absolute_uri(reverse('syllabus-update-api', args=[1])),
            "Delete": request.build_absolute_uri(reverse('syllabus-delete-api', args=[1]))
        },
        "Chapters": {
            "List": request.build_absolute_uri(reverse('chapter-list-api')),
            "Detail View": request.build_absolute_uri(reverse('chapter-detail-api', args=[1])),
            "Create": request.build_absolute_uri(reverse('chapter-create-api',args=[1])),
            "Update": request.build_absolute_uri(reverse('chapter-update-api', args=[1])),
            "Delete": request.build_absolute_uri(reverse('chapter-delete-api', args=[1]))
        },
        "Notes": {
            "List": request.build_absolute_uri(reverse('note-list-api')),
            "Detail View": request.build_absolute_uri(reverse('note-detail-api', args=[1])),
            "Create": request.build_absolute_uri(reverse('note-create-api',args=[1])),
            "Update": request.build_absolute_uri(reverse('note-update-api', args=[1])),
            "Delete": request.build_absolute_uri(reverse('note-delete-api', args=[1]))
        }
    }

    return Response(api_urls)

#-------------------------------------------------------------------------------------------------------------------------------

#-------------------------COURSE-----------------------------------

@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdminUser]) 
def courseCreate(request):
    serializer = CourseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrReadOnly])
def courseList(request):
    courses = Course.objects.all().order_by('id')  # Ensuring ordered query
    serializer = CourseSerializer(courses, many=True,context={'request':request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrReadOnly])
def courseDetail(request, pk):
    try:
        course = Course.objects.get(id=pk)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CourseSerializer(course)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdminUser])
def courseUpdate(request, pk):
    try:
        course = Course.objects.get(id=pk)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

    # Updating fields
    name = request.data.get("name")
    description = request.data.get("description")

    if name:
        course.name = name
    if description:
        course.description = description

    try:
        course.save()
    except Exception as e:
        return Response({'error': f"Failed to update course: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = CourseSerializer(course)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsAdminUser])
def courseDelete(request, pk):
    try:
        course = Course.objects.get(id=pk)
        course.delete()
        return Response({'message': 'Course successfully deleted!'}, status=status.HTTP_200_OK)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
#--------------------------------------------------------------------------------------------------------------------

#-------------------------SEMESTER-----------------------------------

@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdminUser])
def semesterCreate(request, course_id):
    serializer = SemesterSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrReadOnly])
def semesterList(request):
    """
    Retrieve all semesters.
    """
    semesters = Semester.objects.all().order_by('id')
    serializer = SemesterSerializer(semesters, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrReadOnly])
def semesterListByCourse(request, course_id):
    """
    Retrieve semesters by course ID.
    """
    # Ensure we filter semesters by course_id
    semesters = Semester.objects.filter(course_id=course_id).order_by('id')
    
    # If no semesters are found for that course, return an empty list or a message
    if not semesters.exists():
        return Response({"detail": "No semesters found for this course."}, status=404)
    
    serializer = SemesterSerializer(semesters, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([ IsAuthenticated,IsAdminOrReadOnly]) 
def semesterDetail(request, pk):
    try:
        semester = Semester.objects.get(id=pk)
    except Semester.DoesNotExist:
        return Response({'error': 'Semester not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = SemesterSerializer(semester, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdminUser]) 
def semesterUpdate(request, pk):
    try:
        # Fetch the semester object
        semester = Semester.objects.get(id=pk)
    except Semester.DoesNotExist:
        return Response({'error': 'Semester not found'}, status=status.HTTP_404_NOT_FOUND)

    # Get updated fields from the request data
    number = request.data.get("number")
    description = request.data.get("description")

    # Update the semester fields
    if number:
        semester.number = number
    if description:
        semester.description = description

    # Save the changes
    try:
        semester.save()
    except Exception as e:
        return Response({'error': f"Failed to update semester: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    # Return the updated data
    serializer = SemesterSerializer(semester)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsAdminUser]) 
def semesterDelete(request, pk):
    try:
        semester = Semester.objects.get(id=pk)
        semester.delete()
        return Response('Semester successfully deleted!')
    except Semester.DoesNotExist:
        return Response({'error': 'Semester not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
#--------------------------------------------------------------------------------------------------------------------

#-------------------------SUBJECT-----------------------------------    
    

@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdminUser])
def subjectCreate(request):
    # Get a mutable copy of the request data
    data = request.data.copy()

    # Get the semester_id from the request
    semester_id = data.get('semester')

    # Check if the semester_id exists
    try:
        semester = Semester.objects.get(id=semester_id)
    except Semester.DoesNotExist:
        return Response({'error': 'Semester not found'}, status=status.HTTP_400_BAD_REQUEST)

    # Assign the correct semester instance to data
    data['semester'] = semester.id

    # Serialize and save
    serializer = SubjectSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 

@api_view(['GET'])
@permission_classes([ IsAuthenticated,IsAdminOrReadOnly]) 
def subjectList(request):
    subjects = Subject.objects.all().order_by('id')  # Ensure queryset is ordered
    paginator = StandardResultsSetPagination()
    result_page = paginator.paginate_queryset(subjects, request)
    serializer = SubjectSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([ IsAuthenticated,IsAdminOrReadOnly]) 
def subjectDetail(request,pk):
    subjects = Subject.objects.get(id=pk)
    serializer= SubjectSerializer(subjects,many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdminUser]) 
def subjectUpdate(request,pk):
    subject = Subject.objects.get(id=pk)
    serializer=SubjectSerializer(instance=subject ,data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsAdminUser]) 
def subjectDelete(request,pk):
    subject = Subject.objects.get(id=pk)
    subject.delete()
    return Response('Subject successfully Deleted!')

#--------------------------------------------------------------------------------------------------------------------

#-------------------------NOTES-----------------------------------    
@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdminUser])
def noteCreate(request):
    if request.method == 'POST':
        data = request.data.copy()
        
        # Extract file from request.FILES
        file = request.FILES.get('file')

        # Ensure a file was uploaded
        if not file:
            return Response({'error': 'No file uploaded'}, status=400)
        
        # Create and save note
        serializer = NotesSerializer(data=data)
        if serializer.is_valid():
            serializer.save(file=file)
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrReadOnly]) 
def noteList(request):
    notes = Note.objects.all().order_by('id')
    serializer = NotesSerializer(notes, many=True,context={'request':request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrReadOnly]) 
def noteDetail(request,pk):
    note = Note.objects.get(id=pk)
    serializer= NotesSerializer(note,many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdminUser]) 
def noteUpdate(request,pk):
    note = Note.objects.get(id=pk)
    serializer=NotesSerializer(instance=note ,data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsAdminUser]) 
def noteDelete(request,pk):
    note = Note.objects.get(id=pk)
    note.delete()
    return Response('Note successfully Deleted!')

#--------------------------------------------------------------------------------------------------------------------

#-------------------------OLDQUESTIONS-----------------------------------   

@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdminUser])
def pastQuestionCreate(request):
    data = request.data.copy()
    subject_id = data.get('subject')

    # Check if the subject exists
    try:
        subject = Subject.objects.get(id=subject_id)
    except Subject.DoesNotExist:
        return Response({'error': 'Subject not found'}, status=status.HTTP_400_BAD_REQUEST)

    # Assign the subject instance
    data['subject'] = subject.id

    serializer = PastQuestionsSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrReadOnly]) 
def pastQuestionList(request):
    pastquestions = PastQuestion.objects.all().order_by('id')
    serializer = PastQuestionsSerializer(pastquestions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrReadOnly]) 
def pastQuestionDetail(request,pk):
    pastquestion = PastQuestion.objects.get(id=pk)
    serializer= PastQuestionsSerializer(pastquestion,many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdminUser]) 
def pastQuestionUpdate(request,pk):
    pastquestion = PastQuestion.objects.get(id=pk)
    serializer=PastQuestionsSerializer(instance=pastquestion ,data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsAdminUser]) 
def pastQuestionDelete(request,pk):
    pastquestion = PastQuestion.objects.get(id=pk)
    pastquestion.delete()
    return Response('Note successfully Deleted!')

#--------------------------------------------------------------------------------------------------------------------

#-------------------------SYLLABUS-----------------------------------    

@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdminUser])
def syllabusCreate(request):
    subject_id = request.data.get('subject')

    # Check if a syllabus for this subject already exists
    syllabus, created = Syllabus.objects.get_or_create(subject_id=subject_id)

    serializer = SyllabusSerializer(syllabus, data=request.data, partial=True)  # Allow partial updates

    if serializer.is_valid():
        serializer.save()
        if created:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_200_OK)  # Updated syllabus

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrReadOnly]) 
def syllabusList(request):
    syllabuses = Syllabus.objects.all().order_by('id')
    serializer = SyllabusSerializer(syllabuses, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrReadOnly]) 
def syllabusDetail(request, pk):
    try:
        syllabus = Syllabus.objects.get(id=pk)
    except Syllabus.DoesNotExist:
        return Response({'error': 'Syllabus not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = SyllabusSerializer(syllabus, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdminUser]) 
def syllabusUpdate(request, pk):
    try:
        syllabus = Syllabus.objects.get(id=pk)
    except Syllabus.DoesNotExist:
        return Response({'error': 'Syllabus not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = SyllabusSerializer(instance=syllabus, data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsAdminUser]) 
def syllabusDelete(request, pk):
    try:
        syllabus = Syllabus.objects.get(id=pk)
        syllabus.delete()
        return Response('Syllabus successfully deleted!')
    except Syllabus.DoesNotExist:
        return Response({'error': 'Syllabus not found'}, status=status.HTTP_404_NOT_FOUND)

#--------------------------------------------------------------------------------------------------------------------

#-------------------------CHAPTER-----------------------------------    

@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdminUser])
def chapterCreate(request):
    serializer = ChapterSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([ IsAuthenticated,IsAdminOrReadOnly]) 
def chapterList(request):
    chapters = Chapter.objects.all().order_by('id')
    serializer = ChapterSerializer(chapters, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrReadOnly]) 
def chapterDetail(request, pk):
    try:
        chapter = Chapter.objects.get(id=pk)
    except Chapter.DoesNotExist:
        return Response({'error': 'Chapter not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ChapterSerializer(chapter, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdminUser]) 
def chapterUpdate(request, pk):
    try:
        chapter = Chapter.objects.get(id=pk)
    except Chapter.DoesNotExist:
        return Response({'error': 'Chapter not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ChapterSerializer(instance=chapter, data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsAdminUser]) 
def chapterDelete(request, pk):
    try:
        chapter = Chapter.objects.get(id=pk)
        chapter.delete()
        return Response('Chapter successfully deleted!')
    except Chapter.DoesNotExist:
        return Response({'error': 'Chapter not found'}, status=status.HTTP_404_NOT_FOUND)

#-----------------------------------------------------------------------------------------------------------------------------

