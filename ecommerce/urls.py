from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('coreui.urls')),  # Include core cho UI
    # path('products/', include('products.urls')),
]

# Serve static trong development (Clean Code: Chỉ dev mode)
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)