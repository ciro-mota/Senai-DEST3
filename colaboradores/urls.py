from django.urls import path

from .views import ColaboradorCreateView, ColaboradorDeleteView, ColaboradorListView, ColaboradorUpdateView


app_name = "colaboradores"

urlpatterns = [
    path("", ColaboradorListView.as_view(), name="lista"),
    path("colaboradores/novo/", ColaboradorCreateView.as_view(), name="cadastrar"),
    path("colaboradores/<int:pk>/editar/", ColaboradorUpdateView.as_view(), name="editar"),
    path("colaboradores/<int:pk>/excluir/", ColaboradorDeleteView.as_view(), name="excluir"),
]

# Equipamentos
from .views import (
    EquipamentoListView,
    EquipamentoCreateView,
    EquipamentoUpdateView,
    EquipamentoDeleteView,
)

urlpatterns += [
    path("equipamentos/", EquipamentoListView.as_view(), name="equipamento_lista"),
    path("equipamentos/novo/", EquipamentoCreateView.as_view(), name="equipamento_cadastrar"),
    path("equipamentos/<int:pk>/editar/", EquipamentoUpdateView.as_view(), name="equipamento_editar"),
    path("equipamentos/<int:pk>/excluir/", EquipamentoDeleteView.as_view(), name="equipamento_excluir"),
]

# Empréstimos (EPI)
from .views import EmprestimoListView, EmprestimoCreateView, EmprestimoUpdateView

urlpatterns += [
    path("emprestimos/", EmprestimoListView.as_view(), name="emprestimo_lista"),
    path("emprestimos/novo/", EmprestimoCreateView.as_view(), name="emprestimo_cadastrar"),
    path("emprestimos/<int:pk>/editar/", EmprestimoUpdateView.as_view(), name="emprestimo_editar"),
]
