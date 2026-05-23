from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("colaboradores", "equipamento_emprestimo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="emprestimo",
            name="data_entrega",
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name="emprestimo",
            name="data_prevista_devolucao",
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name="emprestimo",
            name="data_devolucao",
            field=models.DateField(blank=True, null=True),
        ),
    ]