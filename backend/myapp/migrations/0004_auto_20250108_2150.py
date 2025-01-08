from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20250108_2148'),
    ]

    operations = [
        # Example: Adding a new field to the Petition model
        migrations.AddField(
            model_name='petition',
            name='example_field',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),

        # Example: Creating a custom script for data migration
        migrations.RunPython(
            code=lambda apps, schema_editor: print("Custom logic can go here"),
            reverse_code=lambda apps, schema_editor: print("Reverse logic here"),
        ),
    ]