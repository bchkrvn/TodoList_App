from django.urls import path
from .views import categories_views, goals_views, comments_views, board_views

urlpatterns = [
    # boards urls
    path('board/create', board_views.BoardCreateAPIView.as_view(), name='create_board'),
    path('board/list', board_views.BoardListAPIView.as_view(), name='board_list'),
    path('board/<int:pk>', board_views.BoardRetrieveUpdateDestroyAPIView.as_view(), name='board_rud'),

    # categories urls
    path('goal_category/create', categories_views.CategoryCreateAPIView.as_view(), name='create_category'),
    path('goal_category/list', categories_views.CategoryListAPIView.as_view(), name='user\'s_list_category'),
    path('goal_category/<int:pk>', categories_views.CategoryRUDAPIView.as_view(), name='user\'s_category_rud'),

    # goals urls
    path('goal/create', goals_views.GoalCreateAPIView.as_view(), name='create_goal'),
    path('goal/list', goals_views.GoalListAPIView.as_view(), name='list_goals'),
    path('goal/<int:pk>', goals_views.GoalRUDAPIView.as_view(), name='rud_goal'),

    # comments urls
    path('goal_comment/create', comments_views.CommentCreateAPIView.as_view(), name='create_comment'),
    path('goal_comment/list', comments_views.CommentListAPIView.as_view(), name='comments_list'),
    path('goal_comment/<int:pk>', comments_views.CommentRUDAPIView.as_view(), name='rud_comment'),
]
