from typing import Any

from django.db import transaction
from rest_framework import serializers
from ..models import Board, BoardParticipant
from core.models import User


class BoardParticipantSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    role = serializers.ChoiceField(required=True, choices=BoardParticipant.Role.choices)

    class Meta:
        model = BoardParticipant
        fields = ('id', 'user', 'role', 'created', 'updated')
        read_only_fields = ('id', 'created', 'updated')


class BoardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = ('id', 'title', 'created', 'updated', 'user', 'is_deleted')
        read_only_fields = ('id', 'created', 'updated', 'is_deleted')

    def create(self, validated_data: dict[str:Any]) -> Board:
        user = validated_data.pop('user')
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(board=board, user=user, role=BoardParticipant.Role.owner)

        return board


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"


class BoardSerializer(serializers.ModelSerializer):
    participants = BoardParticipantSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = ('id', 'title', 'created', 'updated', 'participants', 'is_deleted', 'user')
        read_only_fields = ('id', 'created', 'updated', 'is_deleted')

    def update(self, instance: Board, validated_data: dict[str:Any]) -> Board:
        """
        Change board title and board's participants and their roles
        """
        owner = validated_data.pop('user')
        participants_data = validated_data.pop('participants')
        old_participants = instance.participants.exclude(user=owner)
        new_participants = {new_participant['user'].id: new_participant for new_participant in participants_data}

        # Group participants by updated, deleted and new
        updated_old_participants = []
        deleted_old_participants_ids = []
        new_participants_objects = []

        for old_participant in old_participants:
            if old_participant.user_id not in new_participants:
                deleted_old_participants_ids.append(old_participant.user_id)
            else:
                if old_participant.role != new_participants[old_participant.user_id]['role']:
                    old_participant.role = new_participants[old_participant.user_id]['role']
                    updated_old_participants.append(old_participant)
                del new_participants[old_participant.user_id]

        for new_participant in new_participants.values():
            new_participants_objects.append(BoardParticipant(board=instance,
                                                             user=new_participant['user'],
                                                             role=new_participant['role']))

        # Save participants and board title
        with transaction.atomic():

            if deleted_old_participants_ids:
                BoardParticipant.objects.filter(user_id__in=deleted_old_participants_ids).delete()

            if updated_old_participants:
                BoardParticipant.objects.bulk_update(updated_old_participants, ['role'])

            if new_participants_objects:
                BoardParticipant.objects.bulk_create(new_participants_objects)

            instance.title = validated_data['title']
            instance.save()

        return instance
