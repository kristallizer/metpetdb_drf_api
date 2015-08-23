from rest_framework import serializers

from api.lib.serializers import DynamicFieldsModelSerializer
from api.samples.v1.serializers import MineralSerializer
from api.users.v1.serializers import UserSerializer
from apps.chemical_analyses.models import (
    ChemicalAnalysis,
    ChemicalAnalysisElement,
    ChemicalAnalysisOxide,
    Element,
    Oxide,
)


CHEMICAL_ANALYSIS_FIELDS = ('reference_x', 'reference_y', 'stage_x',
                            'analysis_method', 'where_done', 'analyst',
                            'analysis_date', 'date_precision',
                            'description', 'total', 'spot_id', 'reference')


class ChemicalAnalysisElementSerializer(DynamicFieldsModelSerializer):
    id = serializers.ReadOnlyField(source='element.id')
    name = serializers.ReadOnlyField(source='element.name')
    alternate_name = serializers.ReadOnlyField(source='element.alternate_name')
    symbol = serializers.ReadOnlyField(source='element.symbol')
    atomic_number = serializers.ReadOnlyField(source='element.atomic_number')
    weight = serializers.ReadOnlyField(source='element.weight')
    order_id = serializers.ReadOnlyField(source='element.order_id')

    class Meta:
        model = ChemicalAnalysisElement
        fields = ('id', 'name', 'alternate_name', 'symbol', 'atomic_number',
                  'weight', 'order_id', 'amount', 'precision',
                  'precision_type', 'measurement_unit', 'min_amount',
                  'max_amount')


class ChemicalAnalysisOxideSerializer(DynamicFieldsModelSerializer):
    id = serializers.ReadOnlyField(source='oxide.id')
    element_id = serializers.ReadOnlyField(source='oxide.element_id')
    oxidation_state = serializers.ReadOnlyField(source='oxide.oxidation_state')
    species = serializers.ReadOnlyField(source='oxide.species')
    weight = serializers.ReadOnlyField(source='oxide.weight')
    cations_per_oxide = serializers.ReadOnlyField(
        source='oxide.cations_per_oxide')
    conversion_factor = serializers.ReadOnlyField(
        source='oxide.conversion_factor')
    order_id = serializers.ReadOnlyField(source='oxide.order_id')

    class Meta:
        model = ChemicalAnalysisOxide
        fields = ('id', 'element_id', 'oxidation_state', 'species', 'weight',
                  'cations_per_oxide', 'conversion_factor', 'order_id',
                  'amount', 'precision', 'precision_type', 'measurement_unit',
                  'min_amount', 'max_amount' )


class ChemicalAnalysisSerializer(DynamicFieldsModelSerializer):
    mineral = MineralSerializer(read_only=True)
    owner = UserSerializer(read_only=True)
    elements = ChemicalAnalysisElementSerializer(
        many=True,
        source='chemicalanalysiselement_set')
    oxides = ChemicalAnalysisOxideSerializer(
        many=True,
        source='chemicalanalysisoxide_set')

    class Meta:
        model = ChemicalAnalysis
        depth = 1

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr in CHEMICAL_ANALYSIS_FIELDS:
                setattr(instance, attr, value)
        instance.save()

        return instance


class ElementSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Element


class OxideSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Oxide
