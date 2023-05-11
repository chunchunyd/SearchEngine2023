from .models import *
from django_filters.rest_framework import FilterSet, filters


class CourtFilterSet(FilterSet):
    """
    Court过滤器
    """
    name = filters.CharFilter(field_name='name', lookup_expr='iexact')
    code = filters.CharFilter(field_name='code', lookup_expr='iexact')
    level = filters.CharFilter(field_name='level', lookup_expr='iexact')
    province = filters.CharFilter(field_name='province', lookup_expr='iexact')
    city = filters.CharFilter(field_name='city', lookup_expr='iexact')

    class Meta:
        model = Court
        fields = ['name', 'code', 'level', 'province', 'city']


class ProcuratorateFilterSet(FilterSet):
    """
    Procuratorate过滤器
    """
    name = filters.CharFilter(field_name='name', lookup_expr='iexact')
    district_code = filters.CharFilter(field_name='district_code', lookup_expr='iexact')
    province = filters.CharFilter(field_name='province', lookup_expr='iexact')
    city = filters.CharFilter(field_name='city', lookup_expr='iexact')
    county = filters.CharFilter(field_name='county', lookup_expr='iexact')
    level = filters.CharFilter(field_name='level', lookup_expr='iexact')

    class Meta:
        model = Procuratorate
        fields = ['name', 'district_code', 'province', 'city', 'county', 'level']


class LawDocumentFilterSet(FilterSet):
    """
    LawDocument过滤器
    """
    address = filters.CharFilter(field_name='address', lookup_expr='iexact')

    class Meta:
        model = LawDocument
        fields = ['address']


class JudgmentFilterSet(FilterSet):
    """
    Judgment过滤器
    """
    address = filters.CharFilter(field_name='address', lookup_expr='iexact')
    doc_type = filters.CharFilter(field_name='doc_type', lookup_expr='iexact')
    case_number = filters.CharFilter(field_name='case_number', lookup_expr='iexact')
    case_type = filters.CharFilter(field_name='case_type', lookup_expr='iexact')
    judgment_date = filters.DateFilter(field_name='judgment_date', lookup_expr='year')
    court_id = filters.CharFilter(field_name='court__id', lookup_expr='iexact')
    court_name = filters.CharFilter(field_name='court__name', lookup_expr='iexact')
    plaintiff = filters.CharFilter(field_name='plaintiff__id', lookup_expr='iexact')
    defendant = filters.CharFilter(field_name='defendant__id', lookup_expr='iexact')
    agent = filters.CharFilter(field_name='agent__id', lookup_expr='iexact')
    law_reference = filters.CharFilter(field_name='law_reference__id', lookup_expr='icontains')
    judge = filters.CharFilter(field_name='judge__id', lookup_expr='iexact')

    class Meta:
        model = Judgment
        fields = ['doc_type', 'case_number', 'case_type', 'judgment_date', 'court_id', 'court_name',
                  'plaintiff', 'defendant', 'agent', 'law_reference', 'judge', 'address']


class ProsecutionFilterSet(FilterSet):
    """
    Prosecution过滤器
    """
    address = filters.CharFilter(field_name='address', lookup_expr='iexact')
    doc_type = filters.CharFilter(field_name='doc_type', lookup_expr='iexact')
    case_number = filters.CharFilter(field_name='case_number', lookup_expr='iexact')
    case_type = filters.CharFilter(field_name='case_type', lookup_expr='iexact')
    p_date = filters.DateFilter(field_name='p_date', lookup_expr='year')
    court_id = filters.CharFilter(field_name='court__id', lookup_expr='iexact')
    procuratorate_id = filters.CharFilter(field_name='procuratorate__id', lookup_expr='iexact')
    procuratorate_name = filters.CharFilter(field_name='procuratorate__name', lookup_expr='iexact')
    defendant = filters.CharFilter(field_name='defendant__id', lookup_expr='iexact')

    class Meta:
        model = Prosecution
        fields = ['doc_type', 'case_number', 'case_type', 'p_date', 'court_id', 'procuratorate_id',
                  'procuratorate_name', 'defendant', 'address']
