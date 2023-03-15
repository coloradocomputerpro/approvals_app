from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'programs', views.ProgramViewSet, basename='program')
router.register(r'approvers', views.ApproverViewSet, basename='approver')
router.register(r'requests', views.RequestViewSet, basename='request')
router.register(r'member_types', views.MemberTypeViewSet, basename='member_type')
router.register(r'members', views.MemberViewSet, basename='member')

urlpatterns = [
    path('api/', include(router.urls)),
    path('programs/', views.program_list, name='program_list'),
    path('programs/<int:program_id>/', views.program_detail, name='program_detail'),
    path('programs/<int:pk>/edit/', views.ProgramEdit.as_view(), name='program_edit'),
    path('programs/<int:program_id>/add_member/', views.add_member, name='add_member'),
    path('members/<int:member_id>/edit/', views.edit_member, name='edit_member'),
    path('members/<int:member_id>/remove/', views.remove_member, name='remove_member'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('request/create/', views.RequestCreate.as_view(), name='request_create'),
]
