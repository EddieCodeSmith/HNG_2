from django.urls import path
from .views import RegisterView, LoginView, UserDetailView, OrganisationListView, OrganisationDetailView, OrganisationCreateView, AddUserToOrganisationView

urlpatterns = [
    path('auth/register', RegisterView.as_view(), name='register'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('api/users/<uuid:user_id>', UserDetailView.as_view(), name='user_detail'),
    path('api/organisations', OrganisationListView.as_view(), name='organisation_list'),
    path('api/organisations/<uuid:org_id>', OrganisationDetailView.as_view(), name='organisation_detail'),
    path('api/organisations/create', OrganisationCreateView.as_view(), name='organisation_create'),
    path('api/organisations/<uuid:org_id>/users', AddUserToOrganisationView.as_view(), name='add_user_to_organisation'),
]