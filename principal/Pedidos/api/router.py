from rest_framework.routers import DefaultRouter
from ..views import PedidoViewSet

# Creamos el router para la app Pedidos
router_pedido = DefaultRouter()

# Registramos el ViewSet
router_pedido.register(
    prefix='pedidos',
    viewset=PedidoViewSet,
    basename='pedidos'
)

# Exponemos las URLs generadas automáticamente
urlpatterns = router_pedido.urls
