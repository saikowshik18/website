from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='dashboard_home'),
    path('sell/', views.sell_product, name='sell_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('my_products', views.my_products, name='my_products'),
    path('wishlist/toggle/', views.toggle_wishlist, name='toggle_wishlist'),
    path('wishlist/', views.wishlist_view, name='wishlist_view'),
    path("wishlist/delete/", views.delete_from_wishlist, name="delete_from_wishlist"),
    path('logout/', views.logout_view, name='logout_view'),
    # path('update-product/<int:pk>/', views.update_product, name='update_product'),
    path('update-product/<int:id>/', views.update_product, name='update_product'),
    path('filter-products/', views.filter_products, name='filter_products'),

    path('delete-product-ajax/', views.delete_product_ajax, name='delete_product_ajax'),
    path('search-ajax/', views.search_products_ajax, name='search_products_ajax'),






]



