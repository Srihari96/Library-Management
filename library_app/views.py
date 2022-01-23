from rest_framework.generics import GenericAPIView
from rest_framework import status, permissions, filters, pagination, viewsets, generics
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework_filters import backends
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from .serializers import *
from .models import *

class BookCreateView(GenericAPIView):
    serializer_class = BookSerializer

    def post(self, request):
        data = dict()
        try:
            serializer = BookSerializer(data=request.data)
            if serializer.is_valid():
                book = serializer.save()
                data = {'book_id': book.id}
                
                return JsonResponse({"message":"Success","errors": dict(),"data":data,"status":status.HTTP_201_CREATED})
            return JsonResponse({"message":"Error","errors": serializer.errors, "status":status.HTTP_400_BAD_REQUEST})
        except Exception as e:
            return JsonResponse({'message':e, 'status':status.HTTP_500_INTERNAL_SERVER_ERROR})


class LibraryCreateView(GenericAPIView):
    serializer_class = LibrarySerializer

    def post(self, request):
        data = dict()
        try:
            serializer = LibrarySerializer(data=request.data)
            if serializer.is_valid():
                library = serializer.save()
                data = {'library_id': library.id}
                
                return JsonResponse({"message":"Success","errors": dict(),"data":data,"status":status.HTTP_201_CREATED})
            return JsonResponse({"message":"Error","errors": serializer.errors, "status":status.HTTP_400_BAD_REQUEST})
        except Exception as e:
            return JsonResponse({'message':e, 'status':status.HTTP_500_INTERNAL_SERVER_ERROR})

class LibraryBookCreateView(GenericAPIView):
    serializer_class = LibraryBookSerializer

    def post(self, request):
        data = dict()
        try:
            serializer = LibraryBookSerializer(data=request.data)
            if serializer.is_valid():
                book = serializer.save()
                data = {'library_book': serializer.data}
                
                return JsonResponse({"message":"Success","errors": dict(),"data":data,"status":status.HTTP_201_CREATED})
            return JsonResponse({"message":"Error","errors": serializer.errors, "status":status.HTTP_400_BAD_REQUEST})
        except Exception as e:
            return JsonResponse({'message':e, 'status':status.HTTP_500_INTERNAL_SERVER_ERROR})


class LibraryBookCheckinView(GenericAPIView):
    serializer_class = LibraryBookCheckinSerializer

    def post(self, request):
        data = dict()
        try:
            serializer = LibraryBookCheckinSerializer(data=request.data)
            if serializer.is_valid():
                library_book_activity = serializer.save()
                data = {'library_book_activity': library_book_activity.checked_out_on}
                
                return JsonResponse({"message":"Success","errors": dict(),"data":data,"status":status.HTTP_201_CREATED})
            return JsonResponse({"message":"Error","errors": serializer.errors, "status":status.HTTP_400_BAD_REQUEST})
        except Exception as e:
            return JsonResponse({'message':e, 'status':status.HTTP_500_INTERNAL_SERVER_ERROR})

class LibraryBookCheckoutView(GenericAPIView):
    serializer_class = LibraryBookCheckoutSerializer

    def post(self, request):
        data = dict()
        try:
            serializer = LibraryBookCheckoutSerializer(data=request.data)
            if serializer.is_valid():
                library_book_activity = serializer.save()
                data = {'library_book_activity': serializer.data}
                
                return JsonResponse({"message":"Success","errors": dict(),"data":data,"status":status.HTTP_201_CREATED})
            return JsonResponse({"message":"Error","errors": serializer.errors, "status":status.HTTP_400_BAD_REQUEST})
        except Exception as e:
            return JsonResponse({'message':e, 'status':status.HTTP_500_INTERNAL_SERVER_ERROR})

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 1000	


class LibraryCheckoutListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LibraryActivitySerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = dict()
        account_user = AccountUser.objects.filter(user=self.request.user).first()
        account = account_user.account
        library = LibraryProfile.objects.filter(account=account,datamode='A')
        if library:
            library = library.first()
            queryset = LibraryActivities.objects.filter(library_book__library=library,is_active=True,datamode="A").order_by("-updated_on")
        return queryset


class CustomerCheckoutListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LibraryActivitySerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = LibraryActivities.objects.filter(customer=self.request.user,is_active=True,datamode="A").order_by("-updated_on")
        return queryset