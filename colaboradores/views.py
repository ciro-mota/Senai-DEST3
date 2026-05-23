from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ColaboradorAuthenticationForm, ColaboradorForm
from .forms import EquipamentoForm, EmprestimoCreateForm, EmprestimoUpdateForm
from .models import Equipamento, Emprestimo
from .models import Colaborador


class ColaboradorLoginView(LoginView):
    template_name = "partials/login.html"
    authentication_form = ColaboradorAuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        next_url = self.request.POST.get("next") or self.request.GET.get("next")
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={self.request.get_host()}):
            return next_url
        return str(reverse_lazy("colaboradores:lista"))


@require_POST
def colaborador_logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect(f"{reverse_lazy('colaboradores:login')}?logged_out=1")


class ColaboradorListView(LoginRequiredMixin, ListView):
    model = Colaborador
    template_name = "partials/colaborador_list.html"
    context_object_name = "colaboradores"
    login_url = reverse_lazy("colaboradores:login")

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


class ColaboradorCreateView(LoginRequiredMixin, CreateView):
    model = Colaborador
    form_class = ColaboradorForm
    template_name = "partials/colaborador_form.html"
    login_url = reverse_lazy("colaboradores:login")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Colaborador cadastrado com sucesso.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Não foi possível cadastrar o colaborador. Verifique os campos informados.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("colaboradores:cadastrar")


class ColaboradorUpdateView(LoginRequiredMixin, UpdateView):
    model = Colaborador
    form_class = ColaboradorForm
    template_name = "partials/colaborador_form.html"
    success_url = reverse_lazy("colaboradores:lista")
    login_url = reverse_lazy("colaboradores:login")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Colaborador atualizado com sucesso.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Não foi possível atualizar o colaborador. Verifique os campos informados.")
        return super().form_invalid(form)


class ColaboradorDeleteView(LoginRequiredMixin, DeleteView):
    model = Colaborador
    template_name = "partials/colaborador_confirm_delete.html"
    success_url = reverse_lazy("colaboradores:lista")
    login_url = reverse_lazy("colaboradores:login")

    def delete(self, request, *args, **kwargs):
        colaborador = self.get_object()
        messages.success(request, f"Colaborador '{colaborador.nome}' excluído com sucesso.")
        return super().delete(request, *args, **kwargs)


class EquipamentoListView(LoginRequiredMixin, ListView):
    model = Equipamento
    template_name = "partials/equipamento_list.html"
    context_object_name = "equipamentos"
    login_url = reverse_lazy("colaboradores:login")

    def get_queryset(self):
        queryset = super().get_queryset()
        pesquisa = self.request.GET.get("q", "").strip()
        if pesquisa:
            queryset = queryset.filter(nome__icontains=pesquisa)
        return queryset


class EquipamentoCreateView(LoginRequiredMixin, CreateView):
    model = Equipamento
    form_class = EquipamentoForm
    template_name = "partials/equipamento_form.html"
    login_url = reverse_lazy("colaboradores:login")

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


class EquipamentoUpdateView(LoginRequiredMixin, UpdateView):
    model = Equipamento
    form_class = EquipamentoForm
    template_name = "partials/equipamento_form.html"
    success_url = reverse_lazy("colaboradores:equipamento_lista")
    login_url = reverse_lazy("colaboradores:login")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Equipamento atualizado com sucesso.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Não foi possível atualizar o equipamento. Verifique os campos informados.")
        return super().form_invalid(form)


class EquipamentoDeleteView(LoginRequiredMixin, DeleteView):
    model = Equipamento
    template_name = "partials/equipamento_confirm_delete.html"
    success_url = reverse_lazy("colaboradores:equipamento_lista")
    login_url = reverse_lazy("colaboradores:login")

    def delete(self, request, *args, **kwargs):
        equipamento = self.get_object()
        messages.success(request, f"Equipamento '{equipamento.nome}' excluído com sucesso.")
        return super().delete(request, *args, **kwargs)


class EmprestimoControleListView(LoginRequiredMixin, ListView):
    model = Emprestimo
    template_name = "partials/controle_epi_list.html"
    context_object_name = "emprestimos"
    login_url = reverse_lazy("colaboradores:login")

    def get_queryset(self):
        return super().get_queryset().select_related("colaborador", "equipamento")


class EmprestimoRelatorioListView(LoginRequiredMixin, ListView):
    model = Emprestimo
    template_name = "partials/emprestimo_relatorios.html"
    context_object_name = "emprestimos"
    login_url = reverse_lazy("colaboradores:login")

    def get_queryset(self):
        queryset = super().get_queryset().select_related("colaborador", "equipamento")
        # filtro AND: status, equipamento, colaborador
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


class EmprestimoCreateView(LoginRequiredMixin, CreateView):
    model = Emprestimo
    form_class = EmprestimoCreateForm
    template_name = "partials/emprestimo_form.html"
    login_url = reverse_lazy("colaboradores:login")

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


class EmprestimoUpdateView(LoginRequiredMixin, UpdateView):
    model = Emprestimo
    form_class = EmprestimoUpdateForm
    template_name = "partials/emprestimo_form.html"
    success_url = reverse_lazy("colaboradores:emprestimo_lista")
    login_url = reverse_lazy("colaboradores:login")

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
