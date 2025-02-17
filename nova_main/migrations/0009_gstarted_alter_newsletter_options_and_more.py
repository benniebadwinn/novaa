# Generated by Django 5.0.6 on 2024-05-29 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nova_main', '0008_alter_subscriptions_options_newsletter'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gstarted',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=50)),
                ('email_address', models.EmailField(max_length=150)),
            ],
            options={
                'verbose_name': 'gstartedt',
                'verbose_name_plural': '3. gstarted',
            },
        ),
        migrations.AlterModelOptions(
            name='newsletter',
            options={'verbose_name': 'Newsletter', 'verbose_name_plural': '6. Newsletter'},
        ),
        migrations.AlterModelOptions(
            name='projects',
            options={'ordering': ['title'], 'verbose_name_plural': '4. Projects'},
        ),
        migrations.AlterModelOptions(
            name='subscriptions',
            options={'ordering': ['email'], 'verbose_name_plural': '5. Subscriptions'},
        ),
    ]
