from django.urls import path, include
from books.views import BookAPIViewSet, GenresAPIViewSet, GPTResponseApiView, AuthorsAPIViewSet, UserTextListView, \
    UserTextDetailView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"books", BookAPIViewSet)
router.register(r"genres", GenresAPIViewSet)
router.register(r"genres", AuthorsAPIViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('<str:link>/view_page/<int:page_number>/', BookAPIViewSet.as_view({'get': 'view_page'})),

    path('<str:link>/create_favorite/', BookAPIViewSet.as_view({'post': 'create_favorite'})),
    path('<str:link>/delete_favorite/', BookAPIViewSet.as_view({'post': 'delete_favorite'})),
    path('books/my_favorites/', BookAPIViewSet.as_view({'get': 'my_favorites'}), name='my-favorites'),

    path('user_gen_text/', GPTResponseApiView.as_view()),
    path('user_texts/', UserTextListView.as_view(), name='user-texts-list'),
    path('user_texts/<int:pk>/', UserTextDetailView.as_view(), name='user-text-detail'),
]