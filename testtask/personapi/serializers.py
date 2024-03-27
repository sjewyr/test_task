from rest_framework import serializers

from .models import Mailbox, Person


class MailboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailbox
        fields = ["id", "person", "email"]


class PersonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["name", "surname", "patronymic"]


class PersonSerializer(serializers.ModelSerializer):
    mailboxes = MailboxSerializer(many=True, read_only=True)

    class Meta:
        model = Person
        fields = [
            "id",
            "name",
            "surname",
            "patronymic",
            "gender",
            "nationality",
            "age",
            "mailboxes",
        ]


class FriendsSerializer(serializers.ModelSerializer):
    friends = PersonSerializer(many=True, read_only=True)

    class Meta:
        model = Person
        fields = ["id", "friends"]


class PersonUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = [
            "id",
            "name",
            "surname",
            "patronymic",
            "gender",
            "nationality",
            "age",
        ]
        extra_kwargs = {
            "name": {"required": False},
            "surname": {"required": False},
            "patronymic": {"required": False},
        }
