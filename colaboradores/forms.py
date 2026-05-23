from datetime import datetime, time

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Colaborador
from .models import Equipamento, Emprestimo


class ColaboradorForm(forms.ModelForm):
    class Meta:
        model = Colaborador
        fields = ["nome", "matricula", "setor", "cargo", "ativo"]


class ColaboradorAuthenticationForm(AuthenticationForm):
    """Login do sistema usando credenciais do Django (username/senha).

    No contexto do projeto, o campo `username` representa a matrícula.
    """

    username = forms.CharField(
        label="Matrícula",
        widget=forms.TextInput(
            attrs={
                "autocomplete": "username",
                "placeholder": "Digite sua matrícula",
            }
        ),
    )

    password = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "placeholder": "Digite sua senha",
            }
        ),
    )

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        for field_name in ("username", "password"):
            field = self.fields.get(field_name)
            if field and getattr(field, "widget", None):
                existing = field.widget.attrs.get("class", "")
                field.widget.attrs["class"] = (existing + " form-control").strip()


class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = ["nome", "codigo", "quantidade", "descricao", "ativo"]


class _EmprestimoBaseForm(forms.ModelForm):
    data_entrega = forms.DateField(widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}))
    data_prevista_devolucao = forms.DateField(widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}))
    data_devolucao = forms.DateField(required=False, widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}))

    class Meta:
        model = Emprestimo
        fields = [
            "colaborador",
            "equipamento",
            "quantidade",
            "data_entrega",
            "data_prevista_devolucao",
            "status",
            "data_devolucao",
            "observacao_devolucao",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        date_formats = ["%Y-%m-%d"]
        for name in ("data_entrega", "data_prevista_devolucao", "data_devolucao"):
            field = self.fields.get(name)
            if field:
                field.input_formats = date_formats

        # Mantém a data visível mesmo que o banco armazene DateTime (com timezone)
        # (HTML5 date exige valor em YYYY-MM-DD; se renderizar em dd/mm/aaaa o browser zera o input)
        if self.instance and self.instance.pk:
            tz = timezone.get_current_timezone()
            if self.instance.data_entrega:
                self.initial["data_entrega"] = timezone.localtime(self.instance.data_entrega, tz).date()
            if self.instance.data_prevista_devolucao:
                self.initial["data_prevista_devolucao"] = timezone.localtime(self.instance.data_prevista_devolucao, tz).date()
            if self.instance.data_devolucao:
                self.initial["data_devolucao"] = timezone.localtime(self.instance.data_devolucao, tz).date()

    @staticmethod
    def _date_to_dt_preserving_time(date_value, original_dt=None):
        if not date_value:
            return None
        tz = timezone.get_current_timezone()
        if original_dt:
            original_local = timezone.localtime(original_dt, tz)
            original_time = original_local.timetz().replace(tzinfo=None)
        else:
            original_time = time(0, 0)
        combined = datetime.combine(date_value, original_time)
        return timezone.make_aware(combined, tz)

    def clean_data_prevista_devolucao(self):
        data_prevista = self.cleaned_data.get("data_prevista_devolucao")
        if data_prevista and data_prevista <= timezone.localdate():
            raise ValidationError("A data prevista para devolução deve ser posterior à data atual.")
        return data_prevista

    def clean(self):
        cleaned = super().clean()
        entrega = cleaned.get("data_entrega")
        prevista = cleaned.get("data_prevista_devolucao")
        devolucao = cleaned.get("data_devolucao")
        status = cleaned.get("status")

        if entrega and prevista and prevista <= entrega:
            raise ValidationError("A data prevista para devolução deve ser posterior à data de entrega.")

        status_exige_devolucao = {
            Emprestimo.STATUS_DEVOLVIDO,
            Emprestimo.STATUS_DANIFICADO,
            Emprestimo.STATUS_PERDIDO,
        }
        if status in status_exige_devolucao and not devolucao:
            self.add_error("data_devolucao", "Informe a data da devolução para esse status.")

        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Converte as datas (DateField do form) em DateTime (model), sem mexer na data existente
        if instance.pk:
            original = Emprestimo.objects.get(pk=instance.pk)
        else:
            original = None

        instance.data_entrega = self._date_to_dt_preserving_time(
            self.cleaned_data.get("data_entrega"),
            getattr(original, "data_entrega", None) if original else None,
        )
        instance.data_prevista_devolucao = self._date_to_dt_preserving_time(
            self.cleaned_data.get("data_prevista_devolucao"),
            getattr(original, "data_prevista_devolucao", None) if original else None,
        )
        instance.data_devolucao = self._date_to_dt_preserving_time(
            self.cleaned_data.get("data_devolucao"),
            getattr(original, "data_devolucao", None) if original else None,
        )

        if instance.pk:
            preserved = ["colaborador", "equipamento", "data_entrega", "data_prevista_devolucao"]
            for f in preserved:
                setattr(instance, f, getattr(original, f))
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class EmprestimoCreateForm(_EmprestimoBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].choices = [
            (Emprestimo.STATUS_EMPRESTADO, "Emprestado"),
            (Emprestimo.STATUS_FORNECIDO, "Fornecido"),
        ]

    def clean(self):
        cleaned = super().clean()
        status = cleaned.get("status")
        if status in {Emprestimo.STATUS_DEVOLVIDO, Emprestimo.STATUS_DANIFICADO, Emprestimo.STATUS_PERDIDO}:
            raise ValidationError("No cadastro, selecione apenas 'Emprestado' ou 'Fornecido'.")
        return cleaned


class EmprestimoUpdateForm(_EmprestimoBaseForm):
    pass
