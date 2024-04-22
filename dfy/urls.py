from .views import *

from django.urls import path

urlpatterns = [
    path("plan/", PlanCreate.as_view(), name="plan_self_creation"),
    path("plan/points/", PlanCreatePoints.as_view(), name="plan_self_creation_points"),
    path("history/", History.as_view(), name="plan_history"),
    path("restaurants/", restaurants.as_view(), name="nearby_restaurants"),
    path("hotels/", restaurants.as_view(), name="nearby_hotels"),
    path("events/", Events_endpoint.as_view(), name="event_listing"),
    # path("news/", News.as_view(), name="news_listing"),
]
