from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from . models import *
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.db.models import Count
from django.contrib.auth.models import User
import re  # Regular expressions for validation

def is_valid_email(email):
    # Simple email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def is_strong_password(password):
    # Check for minimum length and complexity
    return len(password) >= 8 and any(char.isdigit() for char in password) and \
           any(char.isalpha() for char in password) and \
           any(char in "!@#$%^&*()-_=+" for char in password)

def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')

        # Validate input fields
        if not name or not email or not username or not password or not repassword:
            messages.error(request, "All fields are required.")
            return render(request, 'login.html')

        if not is_valid_email(email):
            messages.error(request, "Invalid email format.")
            return render(request, 'login.html')

        if password.strip() != repassword.strip():
            messages.error(request, "Passwords do not match.")
            return render(request, 'login.html')

        if not is_strong_password(password):
            messages.error(request, "Password must be at least 8 characters long, contain letters, numbers, and special characters.")
            return render(request, 'login.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'login.html')

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = name
            
            # Creating a profile for the user
            profile = Profile.objects.create(user=user, name=name, date_of_birth=date_of_birth, gender=gender)
            user.save()
            profile.save()

            messages.success(request, "Account created successfully!")
            return redirect('login')  # Redirect to login page after signup
        except Exception as e:
            messages.error(request, f"Error creating account: {e}")
            return render(request, 'login.html')

    return render(request, 'login.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f"Logged in successfully, {user.username}!")
            return redirect('home') 
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'login.html')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('login')

def home(request):
   
    if request.POST:
        search=request.POST.get('search')
        search=search.upper()
        print(search)
        if search=="":
           obj = Country.objects.annotate( 
            university_count=Count('universities', distinct=True),
            institute_count=Count('universities__institutes', 
            distinct=True),course_count=Count('universities__institutes__courses', distinct=True)).order_by('name')
           return render(request,'index.html',{'obj':obj}) 
        if search=='ALL':
            obj = Country.objects.annotate( 
            university_count=Count('universities', distinct=True),
            institute_count=Count('universities__institutes', 
            distinct=True),course_count=Count('universities__institutes__courses', distinct=True)).order_by('name')
            return render(request,'index.html',{'obj':obj})
        else:
             obj = Country.objects.annotate( 
            university_count=Count('universities', distinct=True),
            institute_count=Count('universities__institutes', 
            distinct=True),course_count=Count('universities__institutes__courses', distinct=True)).order_by('name')
             return render(request,'index.html',{'obj':obj})
    else:
        obj = Country.objects.annotate(
        university_count=Count('universities', distinct=True),
        institute_count=Count('universities__institutes', distinct=True),
        course_count=Count('universities__institutes__courses', distinct=True)
    ).order_by('name')

        
        return render(request,'index.html',{'obj':obj})
    
@login_required
def course(request,pk):
    obj=Country.objects.get(id=pk)
    courses=Course.objects.filter(institute__university__country_id=pk).order_by('name')




    return render(request,'courses.html',{'obj':obj,'courses':courses})

def contact(request):
    return render(request,'contact.html')

def blog(request):
    return render(request,'blog.html')




def about(request):
    return render(request,'about.html')

@login_required
def scholarship(request,pk):
    c=Country.objects.get(pk=pk)
    obj=Scholarship.objects.filter(country=pk)
    return render(request,'scholarship.html',{'obj':obj,'c':c})

@login_required
def visa(request,pk):
    c=Country.objects.get(id=pk)
    if request.POST:
         name = request.POST.get('name', '')
         address = request.POST.get('address', '')
         passport_number = request.POST.get('passport_number', '')
         contact_info = request.POST.get('contact_info', '')
         nationality = request.POST.get('nationality', '')
         date_of_birth = request.POST.get('date_of_birth', '')
         visa_type = request.POST.get('visa_type', '')
         passport_copy = request.FILES.get('passport_copy')
         financial_status = request.FILES.get('financial_status')
         letter_of_acceptance = request.FILES.get('letter_of_acceptance')

         visa_application=Visa(
         name=name,
         address=address, 
         passport_number=passport_number,
         contact_info=contact_info,
         nationality=nationality,
         date_of_birth=date_of_birth,
         visa_type=visa_type,
         passport_copy=passport_copy,
         financial_status=financial_status,
         letter_of_acceptance=letter_of_acceptance
            )
         visa_application.save()
            
         return redirect('success')
         
    return render(request,'visa.html',{'c':c})

@login_required
def job(request,pk):
    c  = Country.objects.get(pk=pk)
    job = JobVacancy.objects.filter(country=pk).order_by('application_deadline')
    return render(request,'job.html',{'job': job ,'c':c})

@login_required
def accomodation(request,pk):
    c=Country.objects.get(id=pk)
    obj1=Accommodation.objects.filter(country=pk)
    return render(request,'accomodation.html',{'c':c,'obj1':obj1})

@login_required
def batch(request):
    batch=Batch.objects.all().order_by('start_date')

    return render(request,'batch.html',{'batch':batch})

@login_required
def testcenter(request):
    obj=TestCenter.objects.all()
    return render(request,'testcenter.html',{'obj':obj })

@login_required
def coursematerials(request):
    obj=CourseMaterial.objects.all().order_by('-name')
    return render(request,'CM.html',{'obj':obj})

@login_required
def examreg(request):
    obj = Country.objects.all()

    if request.method == 'POST':
        # Collect form data from the POST request
        name = request.POST.get('name')
        candidate_id = request.POST.get('candidateId')
        contact_number = request.POST.get('contactNumber')
        email = request.POST.get('email')
        dob = request.POST.get('dob')
        mother_tongue = request.POST.get('motherTongue')
        education = request.POST.get('education')
        passport_number = request.POST.get('passportNumber')
        passport_expiry = request.POST.get('passportExpiry')
        country_preferred = request.POST.get('countryPreferred')
        study_plan = request.POST.get('studyPlan')
        nationality = request.POST.get('nationality')
        exam_type = request.POST.get('examType')
        test_location = request.POST.get('testLocation')
        test_date = request.POST.get('testDate')
        time_slot = request.POST.get('timeSlot')
        pte_id = request.POST.get('pteId')
        ielts_id = request.POST.get('ieltsId')
        address = request.POST.get('address')
        comments = request.POST.get('comments')

        # Handle file upload
        passport_upload = request.FILES.get('passportUpload')
        filename = None
        if passport_upload:
            fs = FileSystemStorage()
            filename = fs.save(passport_upload.name, passport_upload)
        else:
            return HttpResponse("No file uploaded.")

        # Create a new instance of ExamRegistration and save it to the database
        registration = ExamRegistration(
            name=name,
            candidate_id=candidate_id,
            contact_number=contact_number,
            email=email,
            dob=dob,
            mother_tongue=mother_tongue,
            education=education,
            passport_number=passport_number,
            passport_expiry=passport_expiry,
            country_preferred=country_preferred,
            study_plan=study_plan,
            nationality=nationality,
            exam_type=exam_type,
            test_location=test_location,
            test_date=test_date,
            time_slot=time_slot,
            pte_id=pte_id,
            ielts_id=ielts_id,
            passport_upload=filename,
            address=address,
            comments=comments
        )
        registration.save()

        return redirect('success')  # Redirect to a success page after registration

    return render(request, 'examreg.html', {'obj': obj})


@csrf_protect
def batchreg(request):
    if request.method == 'POST':
        batch_id = request.POST.get('object_id')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone_no')
        location = request.POST.get('location')
        message = request.POST.get('messages')
        
       
        if batch_id and name and email and phone and location and message:
          batchreg=BatchReg(
                batch = get_object_or_404(Batch, id=batch_id),
                name=name,
                email=email,
                phone=phone,
                location=location,
                message=message
            )
          batchreg.save()
        return redirect('success') 

    
    return render(request,'batch.html')

@login_required
def success(request):
    return render(request,'success.html')


@login_required
def bankloan(request,pk):
    c=Country.objects.get(id=pk)
    obj=BankLoan.objects.all()
    return render(request,'bankloan.html',{'obj':obj,"c":c})

@login_required
def testdata(request):
    obj=TestData.objects.all().order_by('exam_date')
    return  render(request,'testdata.html',{'obj':obj})

@login_required
def submit_response(request):
    if request.method == 'POST':
        # Extract data from the form submission
        name = request.POST.get('name')
        email = request.POST.get('email',)
        address = request.POST.get('address',"")
        phone = request.POST.get('phone',"")
        message = request.POST.get('message')
       
        
        response = Experience.objects.create(
            name=name,
            email=email,
            address=address,
            phone=phone,
            message=message,
           
        )
        
        return redirect('success') 

    return render(request, 'index.html')

@login_required
def blog2(request):
    comment=Comment.objects.all()
    obj1=comment.count()
    return render(request, 'blog-single.html',{'comments':comment,'obj1':obj1})
   
@login_required
def CM2(request,pk):
    obj=CourseMaterial.objects.filter(id=pk)
    return render(request,'CM2.html',{'obj':obj})



def add_comment(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(name=request.user, body=content)
    return redirect('blog2')


def add_reply(request,pk):
    comment = get_object_or_404(Comment, id=pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Reply.objects.create(name=request.user, comment=comment, body=content)
    return redirect('blog2')




