from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('US', 'User'), ('MD', 'Moderator'), ('AD', 'Admin')], default='US', max_length=2),
        ),
    ]
