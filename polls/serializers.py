from rest_framework import serializers
from .models import Question, Choice

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'choice_text']  # No 'votes' field here because votes are counted separately

class ChoiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['choice_text']

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True, source='choices')  # use related_name='choices'

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'pub_date', 'choices']

class QuestionCreateSerializer(serializers.ModelSerializer):
    choices = ChoiceCreateSerializer(many=True)

    class Meta:
        model = Question
        fields = ['question_text', 'pub_date', 'choices']

    def create(self, validated_data):
        choices_data = validated_data.pop('choices')
        question = Question.objects.create(**validated_data)
        for choice_data in choices_data:
            Choice.objects.create(question=question, **choice_data)
        return question

# NEW serializers for results view:

class ChoiceResultSerializer(serializers.ModelSerializer):
    vote_count = serializers.IntegerField()
    percentage = serializers.FloatField()

    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'vote_count', 'percentage']

class QuestionResultSerializer(serializers.ModelSerializer):
    choices = serializers.SerializerMethodField()
    total_votes = serializers.IntegerField()

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'choices', 'total_votes']

    def get_choices(self, obj):
        # Access the annotated choices passed in context from the view
        choices = self.context.get('choices')
        return ChoiceResultSerializer(choices, many=True).data

