from django.urls import path, include
from rest_framework import routers
from .views import AuthAPI, AccountAPI, JobAPI, AdminAPI
from .views.company_api import CompanyAPI
from .views.education_api import EducationAPI
from .views.form_of_work_api import FormOfWorkAPI
from .views.industry_api import IndustryAPI
from .views.job_level_api import JobLevelAPI
from .views.location_api import LocationAPI

router = routers.DefaultRouter()
router.register('auth', AuthAPI, basename='auth')
router.register('account', AccountAPI, basename='account')
router.register('job', JobAPI, basename='job')
router.register('admin', AdminAPI, basename='admin')
router.register("company", CompanyAPI, basename='company')
router.register("industry",IndustryAPI, basename='industry')
router.register("job_level", JobLevelAPI, basename='job_level')
router.register('form_of_work', FormOfWorkAPI, basename='form_of_work')
router.register("education", EducationAPI, basename='education')
router.register('location', LocationAPI, basename='location')

urlpatterns = [
    path('', include(router.urls)),
]