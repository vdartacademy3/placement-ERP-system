from rest_framework import serializers
from .models import Lab, Equipment, Maintenance

class EquipmentSerializer(serializers.ModelSerializer):
    lab_name = serializers.CharField(source='lab.name', read_only=True)
    class Meta:
        model = Equipment
        fields = '__all__'

class LabSerializer(serializers.ModelSerializer):
    equipment_count = serializers.SerializerMethodField()
    class Meta:
        model = Lab
        fields = '__all__'
    def get_equipment_count(self, obj):
        return obj.equipment.count()

class LabDetailSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer(many=True, read_only=True)
    class Meta:
        model = Lab
        fields = '__all__'

class MaintenanceSerializer(serializers.ModelSerializer):
    equipment_name = serializers.CharField(source='equipment.name', read_only=True)
    lab_name       = serializers.CharField(source='equipment.lab.name', read_only=True)
    class Meta:
        model = Maintenance
        fields = '__all__'
