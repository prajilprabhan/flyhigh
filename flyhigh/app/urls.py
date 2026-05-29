
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name="home"),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('course/<int:pk>/',views.course,name='course'),
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
    path('blog/',views.blog,name='blog'),
    path('scholarship/<int:pk>',views.scholarship,name='scholarship'),
    path('visa/<int:pk>',views.visa,name='visa'),
    path('job-vaccancy/<int:pk>',views.job,name='job'),
    path('accomodation/<pk>',views.accomodation,name='acco'),
    path('testcenter',views.testcenter,name='test_center'),
    path('coursematerials',views.coursematerials,name='course_materials'),
    path('batch/',views.batch,name='batch'),
    path('batch-registration/',views.batchreg,name='batchreg'),
    path('exam-registration/',views.examreg,name='examreg'),
    path('successfully-registered',views.success,name='success'),
    path('bank-loan/<int:pk>',views.bankloan,name='bankloan'),
    path('test-data',views.testdata,name='testdata'),
    path('response',views.submit_response,name='response'),
    path('blog2',views.blog2,name='blog2'),
    path('Coursematerials/<int:pk>/',views.CM2,name='CM2'),
    path('signin/',views.signup_view,name='signup'),
    path('addcoments',views.add_comment,name='addcomment'),
    path('addreply/<int:pk>/',views.add_reply,name='addreply'),
   
]
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)