from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username

class Country(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='country')
    short_description = models.TextField(default=None)
    overview = models.TextField()
    quick_facts = models.TextField()

    def __str__(self) -> str:
        return self.name

class University(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='universities')
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

class Institute(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='institutes', default=None)
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)
    fees = models.TextField()
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name='courses', default=None)

    def __str__(self) -> str:
        return self.name

class CourseMaterial(models.Model):
    name=models.CharField(max_length=200,default=None)
    description = models.TextField()
    textbooks = models.FileField(upload_to='textbooks/')
    video_tutorial = models.FileField(upload_to='course_videos/')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class TestCenter(models.Model):
    name = models.CharField(max_length=100,default=None)
    location = models.CharField(max_length=255,default=None)
    country = models.CharField(max_length=100,default=None)
    website = models.URLField(blank=True,default=None)
    contact_email = models.EmailField(blank=True,default=None)
    contact_phone = models.CharField(max_length=20, blank=True,default=None)
    operating_hours = models.TextField(blank=True,default=None)
    def __str__(self) -> str:
        return self.name

class TestData(models.Model):
    exam_name = models.CharField(max_length=200)
    exam_type = models.CharField(max_length=200)
    purpose = models.CharField(max_length=200)
    eligibility_criteria = models.CharField(max_length=200)
    format = models.CharField(max_length=200)
    test_center = models.ForeignKey(TestCenter, on_delete=models.CASCADE)
    resources = models.ForeignKey(CourseMaterial, on_delete=models.CASCADE)
    validity_period = models.CharField(max_length=200)
    exam_date = models.DateField()
    def __str__(self) -> str:
        return self.exam_name

class Accommodation(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone_number = models.CharField(max_length=10)
    type = models.CharField(max_length=200)
    room_type = models.CharField(max_length=200)
    facilities = models.TextField()
    room_description = models.TextField()
    rate = models.CharField(max_length=150)
    nearby_attractions = models.CharField(max_length=200)
    photos = models.ImageField(upload_to='accommodation/')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, default=None)

    def __str__(self) -> str:
        return self.name


class JobVacancy(models.Model):
    job_title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    job_type = models.CharField(max_length=200)
    job_description = models.TextField()
    salary_range = models.CharField(max_length=200)
    application_deadline = models.DateField()
    contact_info = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.job_title

class Scholarship(models.Model):
    name = models.CharField(max_length=200)
    purpose = models.CharField(max_length=200)
    eligibility_criteria = models.CharField(max_length=200)
    application_deadline = models.DateField()
    award_amount = models.CharField(max_length=200)
    contact_info = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Visa(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    passport_number = models.CharField(max_length=200)
    contact_info = models.IntegerField()
    nationality = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    visa_type = models.CharField(max_length=100)
    passport_copy = models.FileField(upload_to='visa/passport')
    financial_status = models.FileField(upload_to='visa/financial_status')
    letter_of_acceptance = models.FileField(upload_to='visa/letter')
    def __str__(self):
        return self.name

class BankLoan(models.Model):
    bank_name = models.CharField(max_length=200)
    eligible_courses = models.CharField(max_length=200)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2,default=None)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2,default=None)
    loan_term_years = models.IntegerField(default=None)
    loan_type = models.CharField(max_length=50, choices=[
    ('secured', 'Secured'),
        ('unsecured', 'Unsecured'),
    ],default=None)
    def __str__(self):
        return self.bank_name

class Batch(models.Model):
    title =models.CharField(max_length=200)
    image=models.ImageField(upload_to='test/', blank=True)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration = models.CharField(max_length=100)
    online = models.BooleanField(default=True)
    location=models.CharField(max_length=100,default=None,blank=True)
     
    def __str__(self) -> str:
         return self.title

class BatchReg(models.Model):
    batch=models.ForeignKey(Batch,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.CharField(max_length=10)
    location=models.CharField(max_length=200)
    message=models.TextField()
    def __str__(self):
        return self.batch
    
    
class ExamRegistration(models.Model):
    name = models.CharField(max_length=100)
    candidate_id = models.CharField(max_length=50, blank=True, null=True)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    dob = models.DateField()
    mother_tongue = models.CharField(max_length=50)
    education = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=50)
    passport_expiry = models.DateField()
    country_preferred = models.CharField(max_length=50)
    study_plan = models.CharField(max_length=100)
    nationality = models.CharField(max_length=50)
    exam_type = models.CharField(max_length=10)
    test_location = models.CharField(max_length=100)
    test_date = models.DateField()
    time_slot = models.CharField(max_length=20)
    pte_id = models.CharField(max_length=50, blank=True, null=True)
    ielts_id = models.CharField(max_length=50, blank=True, null=True)
    passport_upload = models.FileField(upload_to='passports/')
    address = models.TextField()
    comments = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name


    


class Experience(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=200,blank=True)
    phone = models.CharField(max_length=20,blank=True)
    message = models.TextField()

    def __str__(self):
        return f"{self.name}:{self.phone}"


class Comment(models.Model):
    name=models.ForeignKey(User,on_delete=models.CASCADE)
    body=models.TextField()
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}: {self.date.strftime('%d-%m-%y')}"


class Reply(models.Model):
    name=models.ForeignKey(User,on_delete=models.CASCADE)
    comment=models.ForeignKey(Comment,on_delete=models.CASCADE,related_name='replies')
    body=models.TextField()
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}: {self.date.strftime('%d-%m-%y')}"
