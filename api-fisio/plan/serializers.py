from rest_framework import serializers
from .models import Plan, Exercise, ExerciseVideo


class ExerciseVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseVideo
        fields = ['id', 'name', 'video_file']


class ExerciseSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(source='created_by.username')

    videos = ExerciseVideoSerializer(
        many=True,
        source='exercisevideo_set',
        required=False
    )

    class Meta:
        model = Exercise
        fields = ['id', 'name', 'description', 'created_by', 'videos']


class PlanSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(source='created_by.username')
    exercise_set = ExerciseSerializer(many=True, required=False)

    class Meta:
        model = Plan
        fields = ['id', 'created_by', 'title', 'description', 'exercise_set']


class AddExerciseToPlanSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField()
    exercise_id = serializers.IntegerField()
