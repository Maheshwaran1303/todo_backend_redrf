from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Users app routes
    path('api/users/', include('users.urls')),

    # Todos app routes
    path('api/todos/', include('todos.urls')),
]
