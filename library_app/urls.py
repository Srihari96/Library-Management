from django.conf.urls import url, include
from django.urls import path
from . import views

app_name="library_app"
urlpatterns = [
    # Home Navigations
    path('book-create/', views.BookCreateView.as_view(),name='book_create'),
    path('library-create/', views.LibraryCreateView.as_view(),name='library_create'),
    path('library-book-create/', views.LibraryBookCreateView.as_view(),name='library_create'),
    path('library-book-checkout/', views.LibraryBookCheckoutView.as_view(),name='library_checkout_view'),
    path('library-book-checkin/', views.LibraryBookCheckinView.as_view(),name='library_checkin_view'),
    path('library/checkout-list/', views.LibraryCheckoutListView.as_view(),name='library_checkout_list_view'),
    path('customer/checkout-list/', views.CustomerCheckoutListView.as_view(),name='library_checkout_list_view'),
]
