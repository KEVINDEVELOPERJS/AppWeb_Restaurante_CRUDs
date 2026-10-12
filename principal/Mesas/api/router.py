from rest_framework.routers import DefaultRouter
from ..views import MesaViewSet, ZonaViewSet

# Creamos el router para la app Mesas
router_mesa = DefaultRouter()

# Registramos los ViewSets
router_mesa.register(
    prefix='mesas',
    viewset=MesaViewSet,
    basename='mesas'
)

router_mesa.register(
    prefix='zonas',
    viewset=ZonaViewSet,
    basename='zonas'
)

# Exponemos las URLs generadas automáticamente
urlpatterns = router_mesa.urls
