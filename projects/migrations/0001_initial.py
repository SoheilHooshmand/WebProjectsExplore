# Generated by Django 4.1 on 2023-03-17 20:38

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, default='default.jpg', null=True, upload_to='')),
                ('descriptions', models.TextField(blank=True, null=True)),
                ('demo_link', models.CharField(blank=True, max_length=2000, null=True)),
                ('source_link', models.CharField(blank=True, max_length=200, null=True)),
                ('vote_total', models.IntegerField(blank=True, default=0, null=True)),
                ('vote_ratio', models.IntegerField(blank=True, default=0, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('body', models.TextField(blank=True, null=True)),
                ('value', models.CharField(choices=[('up', 'Up Vote'), ('down', 'Down Vote')], max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='tags',
            field=models.ManyToManyField(blank=True, to='projects.tag'),
        ),
    ]