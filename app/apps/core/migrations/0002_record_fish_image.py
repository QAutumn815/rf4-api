# Generated manually — add fish_image field to record tables

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="absoluterecord",
            name="fish_image",
            field=models.URLField(
                blank=True, default="", max_length=512, verbose_name="Fish image URL"
            ),
        ),
        migrations.AddField(
            model_name="weeklyrecord",
            name="fish_image",
            field=models.URLField(
                blank=True, default="", max_length=512, verbose_name="Fish image URL"
            ),
        ),
    ]
