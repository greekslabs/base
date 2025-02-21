from rest_framework import serializers

class BaseModelSerializer(serializers.ModelSerializer):
    COMMON_FIELDS = (
        'id', 'created_by', 'created_at', 'updated_at',
    )

    class Meta:
        abstract = True

    def create(self, validated_data):
        # Set the 'created_by' and 'updated_by' fields to the logged-in user if available
        user = self.context['request'].user
        if 'created_by' in self.Meta.model._meta.get_fields():
            validated_data['created_by'] = user
        if 'updated_by' in self.Meta.model._meta.get_fields():
            validated_data['updated_by'] = user

        # Set the 'user' field only if it exists in the model
        if 'user' in self.Meta.model._meta.get_fields():
            validated_data['user'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Custom logic for updating an object can go here
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # You can add custom representation logic if needed
        return representation
