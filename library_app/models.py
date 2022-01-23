from django.db import models
from django.contrib.auth.models import User, Group
import uuid

# Create your models here.
ACCOUNT_TYPE_CHOICES = (('LIBRARY','Library'),('CONSUMER', 'Consumer'),('PROVIDER','Provider'))
DATAMODE_CHOICES = (('A','Active'),('I', 'Inactive'),('D','Deleted'))
BOOK_GENRE_CHOICES = (('ROMANCE','Romance'),('THRILLER', 'Thriller'),('HORROR','HORROR'))
LIBRARY_ACTIVITY_CHOICES = (('LEND','Lend'),('SOLD', 'Sold'))
LIBRARY_MEMBERSHIP_CHOICES = (('MONTHLY','Monthly'),('YEARLY', 'Yearly'))
BOOK_DELIVERY_TRACKING_CHOICES = (('ORDERED','Ordered'),('OUTFORDELIVERY', 'Out for Delivery'),('DELIVERED','Delivered'),('RETURNINITIATED','Return Iniated'),('RETURNED','Returned'))

class Account(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)
    uid = models.CharField(max_length=20, unique=True,editable=False, db_index=True)
    account_type = models.CharField(max_length=15, default='LIBRARY', choices=ACCOUNT_TYPE_CHOICES)
    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    created_by = models.ForeignKey(User, related_name="%(class)s_createdby", on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, related_name='%(class)s_updated_by', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=1, default='A', choices=DATAMODE_CHOICES)

    def __str__(self):
        return "{0}({1})".format(self.name, self.uid)

    def save(self, *args, **kwargs):
        super(Account, self).save(*args, **kwargs)
        if self.uid == "":
            self.uid  = "A%08d" % (int(self.id))
            super(Account, self).save()

    class Meta:
        db_table = 'account'
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'


class AccountUser(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)
    uid = models.CharField(max_length=20, unique=True, editable=False, db_index=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_default_account = models.BooleanField(default=True)
    is_current_account = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, related_name='%(class)s_created_by', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, related_name='%(class)s_updated_by', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=1, default='A', choices=DATAMODE_CHOICES)

    def __str__(self):
        return "{0}({1})".format(self.user.first_name, self.uid)

    def save(self):
        super(AccountUser, self).save()
        if self.uid == "":
            self.uid  = "AU%08d" % (int(self.id))
            super(AccountUser, self).save()

    class Meta:
        db_table = 'account_user'
        verbose_name = 'AccountUser'
        verbose_name_plural = 'AccountUser'


class UserKYCProfile(models.Model): #INDIVIDUAL_PROFILE
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.URLField(blank=True)
    language = models.CharField(max_length=10,default='en-us')
    mobile_number =  models.CharField(max_length=20,blank=True,null=True)
    alternate_mobile_number = models.CharField(max_length=20,blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,related_name = "%(class)s_createdby", on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User,related_name = "%(class)s_updatedby", on_delete=models.CASCADE)
    datamode = models.CharField(max_length=1, default='A', choices=DATAMODE_CHOICES)

    def __str__(self):
        return "{0}".format(self.user.username)

    class Meta:
        db_table = 'user_kyc_profile'

class LibraryProfile(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    library_name = models.CharField(max_length=100,unique=True)
    logo = models.URLField(blank=True)
    library_license_number = models.CharField(max_length=100,blank=True,null=True)
    email_address = models.EmailField()
    phone_number  = models.CharField(max_length=20,blank=True,null=True)
    website = models.URLField(blank=True)
    address_line1 = models.CharField(max_length=200)
    address_line2 = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    postalcode = models.CharField(max_length=15, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=10)
    updated_by = models.CharField(max_length=10)
    datamode = models.CharField(max_length=1, default='A', choices=DATAMODE_CHOICES)

    def __str__(self):
        return "{0}".format(self.library_name)

    class Meta:
        db_table = 'library_profile'
        verbose_name = 'LibraryProfile'
        verbose_name_plural = 'LibraryProfile'

class Books(models.Model):
    title = models.CharField(max_length=100,unique=True)
    cover_photo = models.URLField(blank=True)
    isbn_number = models.CharField(max_length=100,unique=True)
    genre = models.CharField(max_length=50, choices=BOOK_GENRE_CHOICES)
    author = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=10)
    updated_by = models.CharField(max_length=10)
    datamode = models.CharField(max_length=1, default='A', choices=DATAMODE_CHOICES)

    def __str__(self):
        return "{0}".format(self.title)

    class Meta:
        db_table = 'books'
        verbose_name = 'Books'
        verbose_name_plural = 'Books'


class LibraryBooks(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    library = models.ForeignKey(LibraryProfile, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=10)
    updated_by = models.CharField(max_length=10)
    datamode = models.CharField(max_length=1, default='A', choices=DATAMODE_CHOICES)

    def __str__(self):
        return "{0}".format(self.book.title)

    class Meta:
        db_table = 'library_books'
        verbose_name = 'LibraryBooks'
        verbose_name_plural = 'LibraryBooks'


class LibraryActivities(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    library_book = models.ForeignKey(LibraryBooks, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=15, default='LEND', choices=LIBRARY_ACTIVITY_CHOICES)
    checked_in_on = models.DateTimeField(null=True,blank=True)
    checked_out_on = models.DateTimeField(null=True,blank=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=10)
    updated_by = models.CharField(max_length=10)
    datamode = models.CharField(max_length=1, default='A', choices=DATAMODE_CHOICES)

    def __str__(self):
        return "{0}({1})".format(self.customer.first_name,self.library_book.book.title)

    class Meta:
        db_table = 'library_activities'
        verbose_name = 'LibraryActivities'
        verbose_name_plural = 'LibraryActivities'

class LibraryMembership(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    library = models.ForeignKey(LibraryProfile, on_delete=models.CASCADE)
    membership_type = models.CharField(max_length=15, default='MONTHLY', choices=LIBRARY_MEMBERSHIP_CHOICES)
    expiry_on = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=10)
    updated_by = models.CharField(max_length=10)
    datamode = models.CharField(max_length=1, default='A', choices=DATAMODE_CHOICES)

    class Meta:
        db_table = 'library_membership'
        verbose_name = 'LibraryMembership'
        verbose_name_plural = 'LibraryMembership'


class BookDeliveryTracking(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)
    library_activity = models.ForeignKey(LibraryActivities, on_delete=models.CASCADE)
    delivery_tracking_url = models.URLField(blank=True)
    delivery_status = models.CharField(max_length=30, default='ORDERED', choices=BOOK_DELIVERY_TRACKING_CHOICES)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=10)
    updated_by = models.CharField(max_length=10)
    datamode = models.CharField(max_length=1, default='A', choices=DATAMODE_CHOICES)

    class Meta:
        db_table = 'book_delivery_tracking'
        verbose_name = 'BookDeliveryTracking'
        verbose_name_plural = 'BookDeliveryTracking'


class LibraryRating(models.Model):
    library = models.ForeignKey(LibraryProfile, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=10)
    updated_by = models.CharField(max_length=10)
    datamode = models.CharField(max_length=1, default='A', choices=DATAMODE_CHOICES)


    class Meta:
        db_table = 'library_rating'
        verbose_name = 'LibraryRating'
        verbose_name_plural = 'LibraryRating'


class BookRating(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=10)
    updated_by = models.CharField(max_length=10)
    datamode = models.CharField(max_length=1, default='A', choices=DATAMODE_CHOICES)

    class Meta:
        db_table = 'book_rating'
        verbose_name = 'BookRating'
        verbose_name_plural = 'BookRating'






