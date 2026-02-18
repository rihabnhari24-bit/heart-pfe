from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("appblog", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="patientprediction",
            name="user_name",
            field=models.CharField(default="", max_length=150),
            preserve_default=False,
        ),
    ]
