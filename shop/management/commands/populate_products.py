from django.core.management.base import BaseCommand
from django.utils.text import slugify
from shop.models import Category, Product
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Populates the shop with sample products'

    def handle(self, *args, **kwargs):
        # Clear existing products
        Product.objects.all().delete()
        
        # Get all categories
        categories = Category.objects.all()
        
        if not categories.exists():
            self.stdout.write(self.style.ERROR('No categories found. Please run migrations first.'))
            return
        
        # Sample product data
        products_data = [
            # Writing Instruments
            {'name': 'Premium Fountain Pen', 'price': 29.99, 'description': 'Smooth writing experience with this premium fountain pen. Features a fine nib and ergonomic grip.', 'category': 'Writing Instruments'},
            {'name': 'Mechanical Pencil Set', 'price': 12.99, 'description': 'Set of 3 mechanical pencils with different lead sizes. Includes erasers and replacement leads.', 'category': 'Writing Instruments'},
            {'name': 'Gel Pen Pack', 'price': 8.99, 'description': 'Pack of 10 colorful gel pens for smooth writing and drawing.', 'category': 'Writing Instruments'},
            
            # Notebooks & Journals
            {'name': 'Leather Journal', 'price': 24.99, 'description': 'Handcrafted leather journal with 200 pages of high-quality paper.', 'category': 'Notebooks & Journals'},
            {'name': 'College Ruled Notebook', 'price': 5.99, 'description': '100-page college ruled notebook with durable cover.', 'category': 'Notebooks & Journals'},
            {'name': 'Bullet Journal', 'price': 18.99, 'description': 'Dotted grid bullet journal perfect for planning and creative journaling.', 'category': 'Notebooks & Journals'},
            
            # Paper Products
            {'name': 'Premium Copy Paper', 'price': 9.99, 'description': '500 sheets of 20lb premium copy paper, perfect for printing and copying.', 'category': 'Paper Products'},
            {'name': 'Colored Construction Paper', 'price': 7.99, 'description': 'Pack of 100 sheets in 10 different colors.', 'category': 'Paper Products'},
            {'name': 'Origami Paper Set', 'price': 12.99, 'description': 'Set of 50 sheets in various colors and patterns for origami projects.', 'category': 'Paper Products'},
            
            # Files & Folders
            {'name': 'Document Organizer', 'price': 15.99, 'description': 'Expandable file organizer with 12 pockets and elastic closure.', 'category': 'Files & Folders'},
            {'name': 'Hanging File Folders', 'price': 11.99, 'description': 'Set of 25 hanging file folders in assorted colors.', 'category': 'Files & Folders'},
            {'name': 'Portfolio Folder', 'price': 19.99, 'description': 'Professional portfolio folder with zipper closure and handle.', 'category': 'Files & Folders'},
            
            # Art & Craft Supplies
            {'name': 'Watercolor Paint Set', 'price': 22.99, 'description': 'Set of 24 watercolor paints with brush and mixing palette.', 'category': 'Art & Craft Supplies'},
            {'name': 'Sketching Pencils', 'price': 14.99, 'description': 'Set of 12 graphite pencils in various hardness levels.', 'category': 'Art & Craft Supplies'},
            {'name': 'Craft Scissors', 'price': 8.99, 'description': 'Set of 3 precision craft scissors with different blade patterns.', 'category': 'Art & Craft Supplies'},
            
            # Desk Organizers
            {'name': 'Desk Tray Set', 'price': 24.99, 'description': 'Set of 3 stackable desk trays for organizing papers and supplies.', 'category': 'Desk Organizers'},
            {'name': 'Pen Holder', 'price': 9.99, 'description': 'Stylish pen holder with multiple compartments.', 'category': 'Desk Organizers'},
            {'name': 'Desk Caddy', 'price': 29.99, 'description': 'Multi-compartment desk caddy for organizing all your supplies.', 'category': 'Desk Organizers'},
            
            # Sticky Notes & Memo Pads
            {'name': 'Colorful Sticky Notes', 'price': 6.99, 'description': 'Pack of 5 pads in different colors and sizes.', 'category': 'Sticky Notes & Memo Pads'},
            {'name': 'Memo Cube', 'price': 4.99, 'description': 'Cube of 400 sheets in assorted colors.', 'category': 'Sticky Notes & Memo Pads'},
            {'name': 'Page Markers', 'price': 5.99, 'description': 'Set of 50 page markers in various colors and designs.', 'category': 'Sticky Notes & Memo Pads'},
            
            # Office Tools
            {'name': 'Stapler Set', 'price': 12.99, 'description': 'Stapler with 1000 staples and staple remover.', 'category': 'Office Tools'},
            {'name': '3-Hole Punch', 'price': 9.99, 'description': 'Heavy-duty 3-hole punch with adjustable paper guide.', 'category': 'Office Tools'},
            {'name': 'Paper Shredder', 'price': 39.99, 'description': 'Cross-cut paper shredder with 5-sheet capacity.', 'category': 'Office Tools'},
            
            # School Supplies
            {'name': 'Backpack', 'price': 34.99, 'description': 'Durable backpack with multiple compartments and laptop sleeve.', 'category': 'School Supplies'},
            {'name': 'Scientific Calculator', 'price': 19.99, 'description': 'Advanced scientific calculator with 240 functions.', 'category': 'School Supplies'},
            {'name': 'Geometry Set', 'price': 8.99, 'description': 'Set of geometric tools including compass, ruler, and protractor.', 'category': 'School Supplies'},
            
            # Calendars & Planners
            {'name': 'Wall Calendar', 'price': 14.99, 'description': 'Large wall calendar with beautiful artwork and spacious writing areas.', 'category': 'Calendars & Planners'},
            {'name': 'Planner', 'price': 24.99, 'description': 'Weekly planner with goal-setting sections and habit trackers.', 'category': 'Calendars & Planners'},
            {'name': 'Desk Calendar', 'price': 9.99, 'description': 'Compact desk calendar with tear-off pages.', 'category': 'Calendars & Planners'},
            
            # Markers & Highlighters
            {'name': 'Dry Erase Markers', 'price': 7.99, 'description': 'Pack of 8 dry erase markers in various colors.', 'category': 'Markers & Highlighters'},
            {'name': 'Permanent Markers', 'price': 6.99, 'description': 'Set of 5 permanent markers for labeling and crafts.', 'category': 'Markers & Highlighters'},
            {'name': 'Highlighters', 'price': 5.99, 'description': 'Pack of 6 highlighters in different colors.', 'category': 'Markers & Highlighters'},
            
            # Correction Supplies
            {'name': 'Correction Tape', 'price': 4.99, 'description': 'Roll of correction tape for neat corrections.', 'category': 'Correction Supplies'},
            {'name': 'Whiteout', 'price': 3.99, 'description': 'Bottle of quick-drying whiteout with brush applicator.', 'category': 'Correction Supplies'},
            {'name': 'Correction Pen', 'price': 5.99, 'description': 'Precision correction pen for detailed corrections.', 'category': 'Correction Supplies'},
            
            # Tapes & Glues
            {'name': 'Scotch Tape Dispenser', 'price': 6.99, 'description': 'Dispenser with 3 rolls of clear tape.', 'category': 'Tapes & Glues'},
            {'name': 'Glue Sticks', 'price': 4.99, 'description': 'Pack of 5 washable glue sticks.', 'category': 'Tapes & Glues'},
            {'name': 'Double-Sided Tape', 'price': 7.99, 'description': 'Roll of double-sided tape for crafts and mounting.', 'category': 'Tapes & Glues'},
            
            # Erasers & Sharpeners
            {'name': 'Pencil Sharpener', 'price': 5.99, 'description': 'Dual-hole sharpener with shavings container.', 'category': 'Erasers & Sharpeners'},
            {'name': 'Eraser Pack', 'price': 3.99, 'description': 'Pack of 10 erasers in various shapes and sizes.', 'category': 'Erasers & Sharpeners'},
            {'name': 'Electric Sharpener', 'price': 12.99, 'description': 'Battery-operated electric pencil sharpener.', 'category': 'Erasers & Sharpeners'},
            
            # Clipboards & Boards
            {'name': 'Clipboard', 'price': 8.99, 'description': 'Standard clipboard with clip and storage compartment.', 'category': 'Clipboards & Boards'},
            {'name': 'Whiteboard', 'price': 19.99, 'description': 'Small whiteboard with markers and eraser.', 'category': 'Clipboards & Boards'},
            {'name': 'Magnetic Board', 'price': 15.99, 'description': 'Magnetic board with dry erase surface.', 'category': 'Clipboards & Boards'},
        ]
        
        # Create products
        for product_data in products_data:
            category_name = product_data.pop('category')
            category = Category.objects.get(name=category_name)
            
            # Create slug from name
            slug = slugify(product_data['name'])
            
            # Create product
            Product.objects.create(
                category=category,
                slug=slug,
                stock=random.randint(5, 50),
                **product_data
            )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(products_data)} products')) 