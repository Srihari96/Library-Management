from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password
import datetime

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Books
        fields = ['title', 'isbn_number', 'genre', 'author','description']

    def save(self, *args, **kwargs):
        book = Books()
        book.title = self.validated_data.get('title')
        book.isbn_number = self.validated_data.get('isbn_number')
        book.genre = self.validated_data.get('genre')
        book.author = self.validated_data.get('author')
        book.description = self.validated_data.get('description')
        book.save()
        return book

class LibrarySerializer(serializers.ModelSerializer):
    library_name = serializers.CharField(max_length=100,required=True)

    class Meta:
        model = User
        fields = ['library_name', 'email', 'password']

    def validate(self, data):
        email = data.get('email','')
        if email:
            user = User.objects.filter(email=data.get('email'))
            if user:
                raise serializers.ValidationError({"email":"Email Already exists.Please give different email."})
        library_name = data.get('library_name','')
        if library_name:
            library = LibraryProfile.objects.filter(library_name=data.get('library_name'))
            if library:
                raise serializers.ValidationError({"library_name":"Library name already exists"})
        return data
    
    def validate_password(self, value):
        return make_password(value)

    def save(self, *args, **kwargs):
        user = User()
        user.username = self.validated_data.get('email')
        user.email = self.validated_data.get('email')
        user.password = self.validated_data.get('password')
        user.save()
        user_kyc_profile = UserKYCProfile()
        user_kyc_profile.user = user
        user_kyc_profile.created_by = user
        user_kyc_profile.updated_by = user
        user_kyc_profile.save()
        account = Account()
        account.account_type = 'LIBRARY'
        account.created_by = user
        account.updated_by = user
        account.save()
        account_user = AccountUser()
        account_user.account = account
        account_user.user = user
        account_user.is_default_account = True
        account_user.is_current_account = True
        account_user.created_by = user
        account_user.updated_by = user
        account_user.save()
        library_profile = LibraryProfile()
        library_profile.library_name = self.validated_data.get('library_name')
        library_profile.account = account
        library_profile.save()
        return library_profile

class LibraryBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = LibraryBooks
        fields = ['book', 'library', 'quantity']

    def save(self, *args, **kwargs):
        library_book = LibraryBooks()
        library_book.book = self.validated_data.get('book')
        library_book.library = self.validated_data.get('library')
        library_book.quantity = self.validated_data.get('quantity')
        library_book.save()
        return library_book


class LibraryBookCheckinSerializer(serializers.Serializer):
    library_activity_id = serializers.IntegerField(required=True)

    def validate(self, data):
        library_activity_id = data.get('library_activity_id','')
        if library_activity_id:
            library_activity = LibraryActivities.objects.filter(id=library_activity_id)
            if not library_activity:
                raise serializers.ValidationError({"library_activity_id":"Please provide a valid activity"})
            elif library_activity.first().checked_out_on:
                raise serializers.ValidationError({"library_activity_id":"This activity has already been closed"})
        return data

    def save(self, *args, **kwargs):
        library_activity_id = self.validated_data.get('library_activity_id','')
        library_activity = LibraryActivities.objects.filter(id=library_activity_id).first()
        library_activity.checked_in_on = datetime.datetime.now()
        library_activity.is_active = False
        library_activity.save()
        library_activity.library_book.quantity += 1
        library_activity.library_book.save()
        return library_activity

class LibraryBookCheckoutSerializer(serializers.ModelSerializer):

    class Meta:
        model = LibraryActivities
        fields = ['customer', 'library_book', 'activity_type']

    def save(self, *args, **kwargs):
        library_activity = LibraryActivities()
        library_activity.customer = self.validated_data.get('customer')
        library_activity.library_book = self.validated_data.get('library_book')
        library_activity.activity_type = self.validated_data.get('activity_type','LEND')
        library_activity.checked_out_on = datetime.datetime.now()
        library_activity.save()
        library_activity.library_book.quantity -= 1
        library_activity.library_book.save()
        return library_activity


class LibraryActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = LibraryActivities
        fields ='__all__'

