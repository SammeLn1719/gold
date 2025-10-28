from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'category'

urlpatterns = [

    path('', views.ProductListView.as_view(), name='product_list'),
    path('category/<slug:slug>/', views.CategoryProductListView.as_view(), name='category_products'),
    path('products/', RedirectView.as_view(pattern_name='category:product_list', permanent=True, query_string=True)),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
]
