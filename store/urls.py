from django.urls import path



from . import views

app_name = "store"

urlpatterns = [
    path('products/', views.product_list, name="products"),
    path('products/<int:id>/', views.product_detail, name="products_int_id"),

]



