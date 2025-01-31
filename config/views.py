from django.shortcuts import render
from .models import Book
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .serializers import BookSerializer
from rest_framework import serializers, status
from .permissions import *

# Create your views here.

class BookListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View - Retrieve, Update, Delete
class BookDetailView(APIView):
    permission_classes = [IsAuthorOrReadOnly]

    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        self.check_object_permissions(request, book)
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        self.check_object_permissions(request, book)
        book.delete()
        return Response({'message': 'Book deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
