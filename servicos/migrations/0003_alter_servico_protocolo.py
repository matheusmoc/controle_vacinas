# Generated by Django 4.1.7 on 2023-04-07 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0002_rename_titulo_regiaoservico_cidade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servico',
            name='protocolo',
            field=models.CharField(blank=True, max_length=52, null=True),
        ),
    ]