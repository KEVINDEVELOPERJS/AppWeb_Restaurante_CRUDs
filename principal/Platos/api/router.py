from rest_framework.routers import DefaultRouter
from ..views import PlatoViewSet, CategoriaViewSet

# Creamos el router
router_plato = DefaultRouter()

# Registramos los ViewSets
router_plato.register(
    prefix='platos',
    viewset=PlatoViewSet,
    basename='platos'
)

router_plato.register(
    prefix='categorias',
    viewset=CategoriaViewSet,
    basename='categorias'
)

# Exponemos las URLs generadas automáticamente
urlpatterns = router_plato.urls