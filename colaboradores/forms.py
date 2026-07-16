from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Colaborador
from .models import Equipamento, Emprestimo


class ColaboradorForm(forms.ModelForm):
    class Meta:
        model = Colaborador
        fields = ["nome", "matricula", "setor", "cargo", "ativo"]


class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = ["nome", "codigo", "quantidade", "descricao", "ativo"]


class EmprestimoForm(forms.ModelForm):
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
        widgets = {
            "data_entrega": forms.DateInput(attrs={"type": "date"}),
            "data_prevista_devolucao": forms.DateInput(attrs={"type": "date"}),
            "data_devolucao": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_data_prevista_devolucao(self):
        data_prevista = self.cleaned_data.get("data_prevista_devolucao")
        if data_prevista and data_prevista <= timezone.localdate():
            raise ValidationError("A data prevista para devolução deve ser posterior à data atual.")
        return data_prevista

    def clean(self):
        cleaned = super().clean()
        # ensure data_prevista_devolucao is after data_entrega if both provided
        entrega = cleaned.get("data_entrega")
        prevista = cleaned.get("data_prevista_devolucao")
        if entrega and prevista and prevista <= entrega:
            raise ValidationError("A data prevista para devolução deve ser posterior à data de entrega.")
        return cleaned

    def save(self, commit=True):
        # Preserve immutable fields when updating status only
        instance = super().save(commit=False)
        if self.instance and self.instance.pk:
            # If some fields were disabled in the form rendering, ensure we don't overwrite them
            preserved = ["colaborador", "equipamento", "data_entrega", "data_prevista_devolucao"]
            for f in preserved:
                if getattr(self.instance, f) is not None:
                    setattr(instance, f, getattr(self.instance, f))
        if commit:
            instance.save()
            self.save_m2m()
        return instance
