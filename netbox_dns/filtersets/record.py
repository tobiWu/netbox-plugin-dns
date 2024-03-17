import netaddr

import django_filters
from django.db.models import Q

from netbox.filtersets import NetBoxModelFilterSet
from tenancy.filtersets import TenancyFilterSet
from utilities.filters import MultiValueCharFilter

from ipam.models import IPAddress

from netbox_dns.models import View, Zone, Record, RecordTypeChoices


class RecordFilterSet(TenancyFilterSet, NetBoxModelFilterSet):
    type = django_filters.MultipleChoiceFilter(
        choices=RecordTypeChoices,
        null_value=None,
    )
    zone_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Zone.objects.all(),
        label="Parent Zone ID",
    )
    zone = django_filters.ModelMultipleChoiceFilter(
        queryset=Zone.objects.all(),
        field_name="zone__name",
        to_field_name="name",
        label="Parent Zone",
    )
    view_id = django_filters.ModelMultipleChoiceFilter(
        queryset=View.objects.all(),
        field_name="zone__view",
        label="ID of the View the Parent Zone belongs to",
    )
    view = django_filters.ModelMultipleChoiceFilter(
        queryset=View.objects.all(),
        field_name="zone__view__name",
        to_field_name="name",
        label="View the Parent Zone belongs to",
    )
    address_record_id = django_filters.ModelMultipleChoiceFilter(
        field_name="address_record",
        queryset=Record.objects.all(),
        to_field_name="id",
        label="Address Record",
    )
    ptr_record_id = django_filters.ModelMultipleChoiceFilter(
        field_name="ptr_record",
        queryset=Record.objects.all(),
        to_field_name="id",
        label="Pointer Record",
    )
    rfc2317_cname_record_id = django_filters.ModelMultipleChoiceFilter(
        field_name="rfc2317_cname_record",
        queryset=Record.objects.all(),
        to_field_name="id",
        label="Pointer Record",
    )
    ipam_ip_address_id = django_filters.ModelMultipleChoiceFilter(
        field_name="ipam_ip_address",
        queryset=IPAddress.objects.all(),
        to_field_name="id",
        label="IPAM IP Address",
    )
    ip_address = MultiValueCharFilter(
        method="filter_ip_address",
        label="IP Address",
    )

    managed = django_filters.BooleanFilter()

    class Meta:
        model = Record
        fields = (
            "id",
            "type",
            "name",
            "description",
            "ttl",
            "value",
            "status",
            "disable_ptr",
            "zone",
            "managed",
            "tenant",
            "ip_address",
        )

    def filter_ip_address(self, queryset, name, value):
        if not value:
            return queryset
        try:
            ip_addresses = [
                str(netaddr.IPAddress(item)) for item in value if item.strip()
            ]
            if not ip_addresses:
                return queryset

            return queryset.filter(ip_address__in=ip_addresses)
        except (netaddr.AddrFormatError, ValueError):
            return queryset.none()

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(value__icontains=value)
            | Q(zone__name__icontains=value)
        )
        return queryset.filter(qs_filter)
