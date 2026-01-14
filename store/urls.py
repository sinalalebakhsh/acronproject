from django.urls import path



from . import views

app_name = "store"

urlpatterns = [
    # POST
    path("products/post", views.ProductsPOST.as_view(), name="products_just_POST"),
    path("products/", views.ProductList.as_view(), name="products"),
    path("products/<int:pk>/", views.ProductDetail.as_view(), name="products_int_pk"),
    


    path("categories/", views.categories, name="categories"),
    path("categories/<int:pk>/", views.category_detail, name="category-detailaaa"),







    
    path("json/", views.json, name="json"),

]




