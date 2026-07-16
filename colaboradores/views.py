from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import ColaboradorForm
from .forms import EquipamentoForm, EmprestimoCreateForm, EmprestimoUpdateForm
from .models import Equipamento, Emprestimo
from .models import Colaborador


class ColaboradorListView(ListView):
    model = Colaborador
    template_name = "partials/colaborador_list.html"
    context_object_name = "colaboradores"

    def get_queryset(self):
        queryset = super().get_queryset()
        pesquisa = self.request.GET.get("q", "").strip()
        if pesquisa:
            queryset = queryset.filter(nome__icontains=pesquisa)
        self.pesquisa = pesquisa
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pesquisa"] = getattr(self, "pesquisa", "")
        return context


class ColaboradorCreateView(CreateView):
    model = Colaborador
    form_class = ColaboradorForm
    template_name = "partials/colaborador_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Colaborador cadastrado com sucesso.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Não foi possível cadastrar o colaborador. Verifique os campos informados.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("colaboradores:cadastrar")


class ColaboradorUpdateView(UpdateView):
    model = Colaborador
    form_class = ColaboradorForm
    template_name = "partials/colaborador_form.html"
    success_url = reverse_lazy("colaboradores:lista")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Colaborador atualizado com sucesso.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Não foi possível atualizar o colaborador. Verifique os campos informados.")
        return super().form_invalid(form)


class ColaboradorDeleteView(DeleteView):
    model = Colaborador
    template_name = "partials/colaborador_confirm_delete.html"
    success_url = reverse_lazy("colaboradores:lista")

    def delete(self, request, *args, **kwargs):
        colaborador = self.get_object()
        messages.success(request, f"Colaborador '{colaborador.nome}' excluído com sucesso.")
        return super().delete(request, *args, **kwargs)


class EquipamentoListView(ListView):
    model = Equipamento
    template_name = "partials/equipamento_list.html"
    context_object_name = "equipamentos"

    def get_queryset(self):
        queryset = super().get_queryset()
        pesquisa = self.request.GET.get("q", "").strip()
        if pesquisa:
            queryset = queryset.filter(nome__icontains=pesquisa)
        return queryset


class EquipamentoCreateView(CreateView):
    model = Equipamento
    form_class = EquipamentoForm
    template_name = "partials/equipamento_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Equipamento cadastrado com sucesso.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Não foi possível cadastrar o equipamento. Verifique os campos informados.")
        return super().form_invalid(form)

    def get_success_url(self):
        # Stay on the create page after creation
        return reverse_lazy("colaboradores:equipamento_cadastrar")


class EquipamentoUpdateView(UpdateView):
    model = Equipamento
    form_class = EquipamentoForm
    template_name = "partials/equipamento_form.html"
    success_url = reverse_lazy("colaboradores:equipamento_lista")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Equipamento atualizado com sucesso.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Não foi possível atualizar o equipamento. Verifique os campos informados.")
        return super().form_invalid(form)


class EquipamentoDeleteView(DeleteView):
    model = Equipamento
    template_name = "partials/equipamento_confirm_delete.html"
    success_url = reverse_lazy("colaboradores:equipamento_lista")

    def delete(self, request, *args, **kwargs):
        equipamento = self.get_object()
        messages.success(request, f"Equipamento '{equipamento.nome}' excluído com sucesso.")
        return super().delete(request, *args, **kwargs)


class EmprestimoListView(ListView):
    model = Emprestimo
    template_name = "partials/emprestimo_list.html"
    context_object_name = "emprestimos"

    def get_queryset(self):
        queryset = super().get_queryset().select_related("colaborador", "equipamento")
        # simple filters for colaborador name, equipamento name and status (AND)
        nome = self.request.GET.get("colaborador", "").strip()
        epi = self.request.GET.get("equipamento", "").strip()
        status = self.request.GET.get("status", "").strip()
        if nome:
            queryset = queryset.filter(colaborador__nome__icontains=nome)
        if epi:
            queryset = queryset.filter(equipamento__nome__icontains=epi)
        if status:
            queryset = queryset.filter(status=status)
        return queryset


class EmprestimoCreateView(CreateView):
    model = Emprestimo
    form_class = EmprestimoCreateForm
    template_name = "partials/emprestimo_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Empréstimo registrado com sucesso.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Não foi possível registrar o empréstimo. Verifique os campos informados.")
        return super().form_invalid(form)

    def get_success_url(self):
        # Stay on the create page after creation
        return reverse_lazy("colaboradores:emprestimo_cadastrar")


class EmprestimoUpdateView(UpdateView):
    model = Emprestimo
    form_class = EmprestimoUpdateForm
    template_name = "partials/emprestimo_form.html"
    success_url = reverse_lazy("colaboradores:emprestimo_lista")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Prevent editing of certain fields when updating status
        immutable = ["colaborador", "equipamento", "data_entrega", "data_prevista_devolucao"]
        for f in immutable:
            if f in form.fields:
                form.fields[f].disabled = True
        return form

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Empréstimo atualizado com sucesso.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Não foi possível atualizar o empréstimo. Verifique os campos informados.")
        return super().form_invalid(form)
