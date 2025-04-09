from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, CheckoutBookView, ReturnBookView, UserTransactionHistory, OverdueBooksView
from .views import BookViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='books')

urlpatterns = [
    path('', include(router.urls)),
    path('checkout/', CheckoutBookView.as_view(), name='checkout'),
    path('return/', ReturnBookView.as_view(), name='return'),
    path('my-history/', UserTransactionHistory.as_view(), name='user-history'),
    path('overdue/', OverdueBooksView.as_view(), name='overdue-books'),


]
