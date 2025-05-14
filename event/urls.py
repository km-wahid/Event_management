from django.urls import path
from .views import home, create_event, event_list, update_event, delete_event, create_category, category_list
from debug_toolbar.toolbar import debug_toolbar_urls
urlpatterns = [
    path("", home),
    path("event_list/", event_list, name="event_list"),
    path("create_event/", create_event, name="create_event"),
    path("update_event/<int:id>/", update_event, name="update_event"),
    path("delete_event/<int:id>/", delete_event, name="delete_event"), 
    path("create_category/", create_category, name="create_category"),
    path("categories/", category_list, name="category_list"),  
]+ debug_toolbar_urls()

