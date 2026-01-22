from django.contrib import admin
from django.urls import path, include
from . import views
from website import views as website_views

urlpatterns = [
    # Django admin
    path("admin/", admin.site.urls),
    # Public pages
    path("", website_views.home, name="home"),
    path("about/", website_views.about, name="about"),
    path("help/", website_views.help, name="help"),
    # Auth / profile
    path("profile/", website_views.profile, name="profile"),
    path("redirect/", website_views.role_redirect, name="role_redirect"),
    # Staff / Admin interface
    path("staff/", website_views.staff, name="staff"),
    # User interface
    path("user/", website_views.user, name="user"),
    # Bank interface
    # Google OAuth
    path("oauth/", include("social_django.urls", namespace="social")),
    path("admin/", views.admin, name="admin"),
    path("bank/", views.bank, name="bank"),
    path('book/', views.book, name='book'),
    path('list/', views.list, name='list'),
    path('data/', views.data, name='data'),
]
