from django.db import migrations

def populate_categories(apps, schema_editor):
    Category = apps.get_model('shop', 'Category')
    
    # Categories from MainApp
    categories = [
        {'name': 'Writing Instruments', 'slug': 'writing-instruments', 'description': 'Pens, pencils, markers, and other writing tools'},
        {'name': 'Notebooks & Journals', 'slug': 'notebooks-journals', 'description': 'Notebooks, journals, and other paper-based writing surfaces'},
        {'name': 'Paper Products', 'slug': 'paper-products', 'description': 'Loose paper, notepads, and other paper supplies'},
        {'name': 'Files & Folders', 'slug': 'files-folders', 'description': 'Organizational tools for storing documents and papers'},
        {'name': 'Art & Craft Supplies', 'slug': 'art-craft-supplies', 'description': 'Materials for creative projects and artistic endeavors'},
        {'name': 'Desk Organizers', 'slug': 'desk-organizers', 'description': 'Tools to keep your workspace tidy and efficient'},
        {'name': 'Sticky Notes & Memo Pads', 'slug': 'sticky-notes-memo-pads', 'description': 'Adhesive notes and pads for quick reminders'},
        {'name': 'Office Tools', 'slug': 'office-tools', 'description': 'Staplers, punchers, and other office essentials'},
        {'name': 'School Supplies', 'slug': 'school-supplies', 'description': 'Essential items for students and educators'},
        {'name': 'Calendars & Planners', 'slug': 'calendars-planners', 'description': 'Tools for time management and organization'},
        {'name': 'Markers & Highlighters', 'slug': 'markers-highlighters', 'description': 'Colored markers and highlighting tools'},
        {'name': 'Correction Supplies', 'slug': 'correction-supplies', 'description': 'Whiteout, correction tape, and other correction tools'},
        {'name': 'Tapes & Glues', 'slug': 'tapes-glues', 'description': 'Adhesives for various applications'},
        {'name': 'Erasers & Sharpeners', 'slug': 'erasers-sharpeners', 'description': 'Tools for correcting mistakes and maintaining writing instruments'},
        {'name': 'Clipboards & Boards', 'slug': 'clipboards-boards', 'description': 'Rigid surfaces for writing on the go'},
    ]
    
    for category_data in categories:
        Category.objects.create(**category_data)

def reverse_populate_categories(apps, schema_editor):
    Category = apps.get_model('shop', 'Category')
    Category.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_categories, reverse_populate_categories),
    ] 