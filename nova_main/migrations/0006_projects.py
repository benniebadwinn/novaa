# Generated by Django 5.0.6 on 2024-05-29 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nova_main', '0005_alter_product_options_rename_title_product_title_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('img', models.ImageField(upload_to='media/product_images/%Y/%m/%d')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': '3. Projects',
                'ordering': ['title'],
            },
        ),
    ]
