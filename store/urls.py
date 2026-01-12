from django.urls import path



from . import views

app_name = "store"

urlpatterns = [
    path("products/", views.product_list, name="products"),
    path("products/<int:pk>/", views.product_detail, name="products_int_pk"),
    
    path("categories/<int:pk>/", views.category_detail, name="category-detailaaa"),


    # POST
    path("product/post", views.product_just_POST, name="product_just_POST"),





    
    path("json/", views.json, name="json"),

]




