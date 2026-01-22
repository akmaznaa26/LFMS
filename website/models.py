from django.db import models
from django.contrib.auth.models import User


# PROFILE – role staff / patron
class Profile(models.Model):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("staff", "Staff"),
        ("user", "User"),
        ("bank", "Bank"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username


# BOOK
class Book(models.Model):
    STATUS_CHOICES = (
        ("Available", "Available"),
        ("Borrowed", "Borrowed"),
    )

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    isbn = models.CharField(max_length=20)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Available"
    )
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.title


# BORROW
class Borrow(models.Model):
    username = models.CharField(max_length=100)
    book_id = models.CharField(max_length=50)
    title = models.CharField(max_length=200)

    borrow_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    late_days = models.IntegerField(default=0)
    fine = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.username} - {self.title}"


# Staff
class Staff(models.Model):
    staff_name = models.CharField(max_length=100)
    assigning_section = models.CharField(max_length=100)
    staff_email = models.EmailField()
    shift_time = models.CharField(max_length=50)

    def __str__(self):
        return self.staff_name


# Bank
class Payment(models.Model):
    username = models.CharField(max_length=100)
    card_number = models.CharField(max_length=20)
    borrow_id = models.CharField(max_length=50)
    fine_amount = models.CharField(max_length=20)
    payment_date = models.CharField(max_length=50)

    def __str__(self):
        return self.username
