# Generated by Django 2.0.6 on 2018-07-29 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_category_cate_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipient', models.CharField(max_length=20)),
                ('site', models.CharField(max_length=50)),
                ('zip_code', models.CharField(max_length=20)),
                ('telephone', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'address',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sum_money', models.FloatField()),
                ('recipient', models.CharField(max_length=20)),
                ('site', models.CharField(max_length=50)),
                ('zip_code', models.CharField(max_length=20)),
                ('telephone', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'order',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('unit_price', models.FloatField()),
                ('subtotal', models.FloatField()),
                ('book_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Book')),
                ('order_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Order')),
            ],
            options={
                'db_table': 'orderitem',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 't_user',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.User'),
        ),
        migrations.AddField(
            model_name='address',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.User'),
        ),
    ]
