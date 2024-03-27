from drf_yasg.utils import swagger_auto_schema

import requests

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Mailbox, Person
from .serializers import (
    FriendsSerializer,
    MailboxSerializer,
    PersonCreateSerializer,
    PersonSerializer,
    PersonUpdateSerializer,
)


class PersonDetailBySurname(APIView):
    def get(self, request, surname):
        try:
            person = Person.objects.get(surname=surname)
        except Person.DoesNotExist:
            return Response(
                {"message": "Person not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PersonSerializer(person)
        return Response(serializer.data)


class PersonDetailByID(APIView):
    def get(self, request, id):
        try:
            person = Person.objects.get(id=id)
        except Person.DoesNotExist:
            return Response(
                {"message": "Person not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PersonSerializer(person)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=PersonUpdateSerializer,
        responses={200: PersonSerializer(many=False)},
    )
    def put(self, request, id):
        try:
            person = Person.objects.get(id=id)
        except Person.DoesNotExist:
            return Response(
                {"message": "Person not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PersonUpdateSerializer(person, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonList(APIView):

    def get(self, request):
        persons = Person.objects.all()
        serializer = PersonSerializer(persons, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=PersonCreateSerializer,
        responses={201: PersonSerializer()},
    )
    def post(self, request):
        serializer = PersonCreateSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data["name"]
            gender, nationality, age = get_person_info(name)
            serializer.save(gender=gender, nationality=nationality, age=age)
            person = serializer.instance
            response_serializer = PersonSerializer(person)
            return Response(
                response_serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddMailbox(APIView):
    def post(self, request, person_id, email):
        try:
            Person.objects.get(id=person_id)
        except Person.DoesNotExist:
            return Response(
                {"message": "Person not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = MailboxSerializer(
            data={"person": person_id, "email": email}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteMailbox(APIView):
    def delete(self, request, person_id, email_id):
        try:
            person = Person.objects.get(id=person_id)
            mailbox = Mailbox.objects.get(person=person, id=email_id)
        except (Person.DoesNotExist, Mailbox.DoesNotExist):
            return Response(
                {"message": "Person or mailbox not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        mailbox.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddFriend(APIView):
    def post(self, request, person_id, friend_id):
        try:
            person = Person.objects.get(id=person_id)
            friend = Person.objects.get(id=friend_id)
        except Person.DoesNotExist:
            return Response(
                {"message": "Person not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        person.friends.add(friend)
        return Response(status=status.HTTP_200_OK)


class RemoveFriend(APIView):
    def delete(self, request, person_id, friend_id):
        try:
            person = Person.objects.get(id=person_id)
            friend = Person.objects.get(id=friend_id)
        except Person.DoesNotExist:
            return Response(
                {"message": "Person not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        person.friends.remove(friend)
        return Response(status=status.HTTP_200_OK)


class GetFriends(APIView):
    def get(self, request, person_id):
        try:
            person = Person.objects.get(id=person_id)
            serializer = FriendsSerializer(person)
            return Response(serializer.data)

        except Person.DoesNotExist:
            return Response(
                {"message": "Person not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


def get_person_info(name):
    gender = ""
    nationality = ""
    age = None
    gender_response = requests.get(f"https://api.genderize.io/?name={name}")
    if gender_response.status_code == 200:
        gender_data = gender_response.json()
        gender = gender_data.get("gender")
    nationality_response = requests.get(
        f"https://api.nationalize.io/?name={name}"
    )
    if nationality_response.status_code == 200:
        nationality_data = nationality_response.json()
        countries = nationality_data.get("country")
        if countries:
            nationality = countries[0].get("country_id")
    age_response = requests.get(f"https://api.agify.io/?name={name}")
    if age_response.status_code == 200:
        age_data = age_response.json()
        age = age_data.get("age")

    return gender, nationality, age
