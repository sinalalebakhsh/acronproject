from django.urls import path, include
from rest_framework.routers import DefaultRouter,SimpleRouter
from . import views
app_name = "store"

router = DefaultRouter()
router.register("products", views.ProductViewSet, basename="product")
router.register("categories", views.CategoryViewSet, basename="category")

urlpatterns = router.urls
# urlpatterns = [
#     path("", include(router.urls)),
# ]


""" # urls___ = router.urls
# urls___ = router.urls
# print(urls___)
"""

""" # urlpatterns = [
# urlpatterns = [
#     # POST
#     path("products/post", views.ProductsPOST.as_view(), name="products_just_POST"),
    
#     # GET
#     path("products/", views.ProductList.as_view(), name="products"),

#     # GET + PUT + DELETE
#     path("products/<int:pk>/", views.ProductDetail.as_view(), name="products_int_pk"),
    
#     # GET
#     path("categories/", views.CategoryList.as_view(), name="categories"),


#     # GET + PUT + DELETE
#     path("categories/<int:pk>/", views.CategorieDetail.as_view(), name="category-detailaaa"),
# ]
"""
