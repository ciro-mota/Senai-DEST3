from django.db import models


class Colaborador(models.Model):
    nome = models.CharField(max_length=120)
    matricula = models.CharField(max_length=30, unique=True)
    setor = models.CharField(max_length=80)
    cargo = models.CharField(max_length=80)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self) -> str:
        return f"{self.nome} - {self.matricula}"


class Equipamento(models.Model):
    nome = models.CharField(max_length=140)
    codigo = models.CharField(max_length=60, blank=True)
    quantidade = models.PositiveIntegerField(default=1)
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self) -> str:
        return f"{self.nome} ({self.codigo})" if self.codigo else self.nome


class Emprestimo(models.Model):
    STATUS_EMPRESTADO = "emprestado"
    STATUS_FORNECIDO = "fornecido"
    STATUS_DEVOLVIDO = "devolvido"
    STATUS_DANIFICADO = "danificado"
    STATUS_PERDIDO = "perdido"

    STATUS_CHOICES = [
        (STATUS_EMPRESTADO, "Emprestado"),
        (STATUS_FORNECIDO, "Fornecido"),
        (STATUS_DEVOLVIDO, "Devolvido"),
        (STATUS_DANIFICADO, "Danificado"),
        (STATUS_PERDIDO, "Perdido"),
    ]

    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE, related_name="emprestimos")
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE, related_name="emprestimos")
    quantidade = models.PositiveIntegerField(default=1)
    data_entrega = models.DateField()
    data_prevista_devolucao = models.DateField()
    data_devolucao = models.DateField(null=True, blank=True)
    observacao_devolucao = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_EMPRESTADO)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]

    def __str__(self) -> str:
        return f"{self.colaborador.nome} — {self.equipamento.nome} ({self.status})"
