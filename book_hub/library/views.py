from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

from rest_framework import filters

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author', 'isbn']

    def get_queryset(self):
        queryset = super().get_queryset()
        available = self.request.query_params.get('available')
        if available == 'true':
            queryset = queryset.filter(copies_available__gt=0)
        return queryset


from rest_framework import status, generics, permissions
from rest_framework.response import Response
from .models import Transaction, Book
from .serializers import TransactionSerializer
from django.utils import timezone

class CheckoutBookView(generics.CreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        book_id = request.data.get('book')
        user = request.user

        if not book_id:
            return Response({"error": "Book ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        if book.copies_available < 1:
            return Response({"error": "No copies available"}, status=status.HTTP_400_BAD_REQUEST)

        already_checked = Transaction.objects.filter(book=book, user=user, return_date__isnull=True).exists()
        if already_checked:
            return Response({"error": "You already have this book checked out"}, status=400)

        transaction = Transaction.objects.create(book=book, user=user)
        book.copies_available -= 1
        book.save()

        return Response(TransactionSerializer(transaction).data, status=201)

class ReturnBookView(generics.UpdateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        book_id = request.data.get('book')
        user = request.user

        try:
            transaction = Transaction.objects.get(user=user, book_id=book_id, return_date__isnull=True)
        except Transaction.DoesNotExist:
            return Response({"error": "No active checkout for this book"}, status=404)

        transaction.return_date = timezone.now().date()
        transaction.save()

        transaction.book.copies_available += 1
        transaction.book.save()

        return Response(TransactionSerializer(transaction).data)


class UserTransactionHistory(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by('-checkout_date')
from rest_framework.permissions import IsAuthenticated


from .permissions import IsAdminUser

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author', 'isbn']  # 👈 Only admins can perform CRUD

    def get_permissions(self):
        # Allow anyone (authenticated or not) to view books (GET)
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsAdminUser()]  # Create, update, delete = admin only


class OverdueBooksView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Transaction.objects.filter(return_date__isnull=True, due_date__lt=timezone.now().date())





from django.core.mail import send_mail

def send_overdue_reminder(user_email, book_title):
    send_mail(
        subject='Overdue Book Reminder',
        message=f'Your book "{book_title}" is overdue. Please return it ASAP.',
        from_email='library@example.com',
        recipient_list=[user_email],
    )

def get_queryset(self):
    queryset = Book.objects.all()
    available = self.request.query_params.get('available')
    if available == 'true':
        queryset = queryset.filter(copies_available__gt=0)
    return queryset
