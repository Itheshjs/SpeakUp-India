from rest_framework import serializers
from .models import Complaint, Evidence

class EvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evidence
        fields = ['id', 'file_url', 'media_type', 'uploaded_at']

class ComplaintSerializer(serializers.ModelSerializer):
    evidence = EvidenceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Complaint
        fields = [
            'id', 'user', 'is_anonymous', 'title', 'description', 
            'category', 'status', 'urgency', 'latitude', 'longitude', 
            'created_at', 'updated_at', 'evidence'
        ]
        read_only_fields = ['status', 'user', 'created_at', 'updated_at', 'category']

    def create(self, validated_data):
        # We will add simple AI categorization mocking here
        # For now, just set a default category or let it be extracted later
        # We can extract text from description for a mock category
        desc = validated_data.get('description', '').lower()
        if 'road' in desc or 'pothole' in desc:
            validated_data['category'] = 'Road Damage'
        elif 'water' in desc or 'leak' in desc:
            validated_data['category'] = 'Water Leakage'
        elif 'garbage' in desc or 'dump' in desc:
            validated_data['category'] = 'Illegal Dumping'
        else:
            validated_data['category'] = 'General/Other'
            
        return super().create(validated_data)
