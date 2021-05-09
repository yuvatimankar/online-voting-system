from django.urls import path

from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.home, name='home'),
    path('list/', views.polls_list, name='list'),
    path('add/', views.add_poll, name='add'),
    path('results/', views.all_results, name='results'),
    path('edit/<int:poll_id>/', views.edit_poll, name='edit_poll'),
    path('edit/<int:poll_id>/candidate/add/', views.add_candidate, name="add_candidate"),
    path('edit/candidate/<int:candidate_id>/', views.edit_candidate, name="edit_candidate"),
    path('delete/candidate/<int:candidate_id>/', views.delete_candidate, name='candidate_confirm_delete'),
    path('delete/poll/<int:poll_id>/', views.delete_poll, name='poll_confirm_delete'),
    path('details/<int:poll_id>/', views.poll_detail, name='detail'),
    path('details/<int:poll_id>/vote/', views.poll_vote, name='vote')
]

