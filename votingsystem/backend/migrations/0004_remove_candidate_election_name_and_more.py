# Generated by Django 4.2.6 on 2023-11-26 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0003_candidate_email"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="candidate",
            name="election_name",
        ),
        migrations.RemoveField(
            model_name="voter",
            name="election_name",
        ),
        migrations.AddField(
            model_name="candidate",
            name="election_name",
            field=models.ManyToManyField(to="backend.election"),
        ),
        migrations.AddField(
            model_name="voter",
            name="election_name",
            field=models.ManyToManyField(to="backend.election"),
        ),
    ]