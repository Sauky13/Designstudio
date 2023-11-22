from django.urls import path
from .views import LoginViewUser, profile, index, LogoutViewUser, ApplicationCreateDone, ApplicationDeleteView, \
    application_detail, change_application_status, CategoryListView, CategoryCreate,  CategoryDelete
from .views import RegisterDoneView, UserRegisterView, create_application
from .views import view_user_applications
from designstudio import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

app_name = 'main'

urlpatterns = [
                  path('', index, name='index'),
                  path('accounts/login', LoginViewUser.as_view(), name='login'),
                  path('accounts/logout/', LogoutViewUser.as_view(), name='logout'),
                  path('accounts/profile/', profile, name='profile'),
                  path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
                  path('accounts/register/', UserRegisterView.as_view(), name='register'),
                  path('accounts/create_application/', create_application, name='create_application'),
                  path('accounts/create_application/done/', ApplicationCreateDone.as_view(),
                       name='application_create_done'),
                  path('user/applications/', view_user_applications, name='view_user_applications'),
                  path('application/<int:pk>/', application_detail, name='application_detail'),
                  path('application/delete/<int:pk>/', ApplicationDeleteView.as_view(), name='application_delete'),
                  path('application-deleted/', TemplateView.as_view(template_name='application_deleted.html'),
                       name='application_deleted'),
                  path('application/<int:pk>/change_status/', change_application_status,
                       name='change_application_status'),
                  path('category/', CategoryListView.as_view(), name='category'),
                  path('category/create/', CategoryCreate.as_view(), name='category-create'),

                  path('category/<int:pk>/delete/', CategoryDelete.as_view(), name='category-delete'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
