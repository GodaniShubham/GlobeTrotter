from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("destinations", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="city",
            name="external_image_url",
            field=models.URLField(blank=True, max_length=1000),
        ),
    ]
