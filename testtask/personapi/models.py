from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, blank=True)
    age = models.IntegerField(null=True)
    nationality = models.CharField(max_length=255, blank=True)
    friends = models.ManyToManyField("self", symmetrical=True)


class Mailbox(models.Model):
    person = models.ForeignKey(
        Person, related_name="mailboxes", on_delete=models.CASCADE
    )
    email = models.EmailField()

    def __str__(self):
        return self.email
