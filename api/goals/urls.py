from django.urls import path
from .views import categories_views, goals_views


urlpatterns = [
    path('goal_category/create', categories_views.CategoryCreateAPIView.as_view(), name='create_category'),
    path('goal_category/list', categories_views.CategoryListAPIView.as_view(), name='user\'s_list_category'),
    path('goal_category/<int:pk>', categories_views.CategoryRUDAPIView.as_view(), name='user\'s_category'),

    path('goal/create', goals_views.GoalCreateAPIView.as_view(), name='create_goal'),
    path('goal/list', goals_views.GoalListAPIView.as_view(), name='list_goals'),
    path('goal/<int:pk>', goals_views.GoalRUDAPIView.as_view(), name='rud_goal')
]
