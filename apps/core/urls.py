from django.urls import path, register_converter
from . import views

# defining custom path for the save_root view
class CustomIDConverter:
    regex = r'_[A-Za-z0-9]'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value

register_converter(CustomIDConverter, 'custom_id')

urlpatterns = [
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('gallery/', views.gallery, name='gallery'),
    path('edit-profileInfo/', views.edit_profileInfo, name='edit_profileInfo'),
    path('edit-profileSocial/', views.edit_profileSocial, name='edit_profileSocial'),
    path('delete-image/<int:image_id>/', views.delete_image, name='delete_image'),
    path('timeline/', views.timeline, name='timeline'),
    path('add-timeline/', views.add_timeline, name='add_timeline'),
    path('delete-timeline/<int:timeline_id>/', views.delete_timeline, name='delete_timeline'),
    path('edit-timeline/<int:timeline_id>/', views.edit_timeline, name='edit_timeline'),
    path('get-timeline/<int:timeline_id>/', views.get_timeline, name='get_timeline'),
    path('roots-list/', views.roots_list, name='roots_list'),
    path('roots-grid/', views.roots_grid, name='roots_grid'),
    path('save-roots/<custom_id:id>/', views.save_root, name='save_root'),
    path('quiz/', views.quiz, name='quiz'),
    path('add-question/', views.add_question, name='add_question'),
    path('delete_question/<int:question_id>/', views.delete_question, name='delete_question'),
    path('recommendation/', views.recommendation, name='recommendation'),
]
