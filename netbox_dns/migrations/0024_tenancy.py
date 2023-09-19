# Generated by Django 4.2.4 on 2023-09-17 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("tenancy", "0010_tenant_relax_uniqueness"),
        ("netbox_dns", "0023_alter_record_value"),
    ]

    operations = [
        migrations.AddField(
            model_name="nameserver",
            name="tenant",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="netbox_dns_nameservers",
                to="tenancy.tenant",
            ),
        ),
        migrations.AddField(
            model_name="record",
            name="tenant",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="netbox_dns_records",
                to="tenancy.tenant",
            ),
        ),
        migrations.AddField(
            model_name="view",
            name="tenant",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="netbox_dns_views",
                to="tenancy.tenant",
            ),
        ),
        migrations.AddField(
            model_name="zone",
            name="tenant",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="netbox_dns_zones",
                to="tenancy.tenant",
            ),
        ),
    ]