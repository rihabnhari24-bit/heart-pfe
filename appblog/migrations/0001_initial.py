from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PatientPrediction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("patient_identifier", models.CharField(max_length=50)),
                ("patient_name", models.CharField(max_length=120)),
                ("age", models.IntegerField()),
                ("sex", models.IntegerField()),
                ("cp", models.IntegerField()),
                ("trestbps", models.IntegerField()),
                ("chol", models.IntegerField()),
                ("fbs", models.IntegerField()),
                ("restecg", models.IntegerField()),
                ("thalach", models.IntegerField()),
                ("exang", models.IntegerField()),
                ("oldpeak", models.FloatField()),
                ("slope", models.IntegerField()),
                ("ca", models.IntegerField()),
                ("thal", models.IntegerField()),
                ("prediction", models.CharField(max_length=30)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
