from django.contrib import admin
from django.urls import path, include
from expenses import views as expense_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Homepage
    path('', expense_views.home, name='home'),

    # Auth
    path('login/', expense_views.login_view, name='login'),
    path('register/', expense_views.register, name='register'),
    path('logout/', expense_views.logout_view, name='logout'),

    # Expenses app
    path('expenses/', include('expenses.urls')),
]
