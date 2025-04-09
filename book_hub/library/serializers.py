from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    is_overdue = serializers.SerializerMethodField()
  
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['user', 'checkout_date']


        def get_is_overdue(self, obj):
            return obj.is_overdue()
