"""
Seeds the database with sample products so the storefront isn't empty
on a fresh clone.

Usage:
    python manage.py seed_products
"""
import shutil
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from products_app.models import Product

SAMPLE_PRODUCTS = [
    # --- Electronics: featured (shows in "Deals and offers" + Home featured row) ---
    {"name": "Smart Watch Series 5", "price": 49.99, "old_price": 65.00, "category": "electronics",
     "stock": 40, "is_featured": True, "rating": 4.3,
     "description": "Fitness tracking smart watch with heart-rate monitor and 7-day battery life.",
     "image": "Home_Page_Images/Deals_and_offer_images/smart_watch.png"},
    {"name": "Laptop Pro 15-inch", "price": 899.00, "old_price": 1099.00, "category": "electronics",
     "stock": 15, "is_featured": True, "rating": 4.6,
     "description": "15-inch laptop with fast processor, perfect for work and study.",
     "image": "Home_Page_Images/Deals_and_offer_images/laptop.png"},
    {"name": "DSLR Camera 10x Zoom", "price": 349.00, "old_price": 420.00, "category": "electronics",
     "stock": 20, "is_featured": True, "rating": 4.4,
     "description": "Entry-level DSLR camera with 10x optical zoom, great for beginners.",
     "image": "Home_Page_Images/Deals_and_offer_images/camera.png"},
    {"name": "Wireless Headphones", "price": 59.99, "old_price": 79.99, "category": "electronics",
     "stock": 60, "is_featured": True, "rating": 4.2,
     "description": "Over-ear wireless headphones with noise cancellation.",
     "image": "Home_Page_Images/Deals_and_offer_images/headphone.png"},
    {"name": "Smartphone X", "price": 499.00, "old_price": 599.00, "category": "electronics",
     "stock": 25, "is_featured": True, "rating": 4.5,
     "description": "6.5-inch display smartphone with triple camera setup.",
     "image": "Home_Page_Images/Deals_and_offer_images/smart_phone.png"},

    # --- More electronics ---
    {"name": "Smart Watch Pro", "price": 79.00, "category": "electronics", "stock": 30, "rating": 4.1,
     "description": "Premium smart watch with GPS and always-on display.",
     "image": "Home_Page_Images/consumer_elec/watch.png"},
    {"name": "Action Camera 4K", "price": 89.00, "category": "electronics", "stock": 18, "rating": 4.0,
     "description": "Waterproof 4K action camera for adventure shoots.",
     "image": "Home_Page_Images/consumer_elec/camera.png"},
    {"name": "Gaming Headset", "price": 35.00, "category": "electronics", "stock": 45, "rating": 4.3,
     "description": "Surround-sound gaming headset with mic.",
     "image": "Home_Page_Images/consumer_elec/blue_headphone.png"},
    {"name": "Studio Headphones", "price": 45.00, "category": "electronics", "stock": 38, "rating": 4.2,
     "description": "Studio-quality over-ear headphones for music production.",
     "image": "Home_Page_Images/consumer_elec/headphone.png"},
    {"name": "Laptop & PC Combo", "price": 340.00, "category": "electronics", "stock": 10, "rating": 4.0,
     "description": "Budget-friendly laptop, great for everyday productivity.",
     "image": "Home_Page_Images/consumer_elec/laptop.png"},
    {"name": "Smartphone Mini", "price": 199.00, "category": "electronics", "stock": 22, "rating": 3.9,
     "description": "Compact smartphone with all-day battery life.",
     "image": "Home_Page_Images/consumer_elec/phone.png"},
    {"name": "Smartphone Red Edition", "price": 240.00, "category": "electronics", "stock": 14, "rating": 4.1,
     "description": "Limited red edition smartphone with 128GB storage.",
     "image": "Home_Page_Images/consumer_elec/redphone.png"},

    # --- Home & Outdoor ---
    {"name": "Soft Lounge Chair", "price": 19.00, "category": "home_outdoor", "stock": 12, "rating": 4.0,
     "description": "Comfortable soft chair for living rooms.",
     "image": "Home_Page_Images/home_and_outdoor/sofa.png"},
    {"name": "Modern Table Lamp", "price": 19.00, "category": "home_outdoor", "stock": 26, "rating": 4.2,
     "description": "Minimalist table lamp, warm ambient lighting.",
     "image": "Home_Page_Images/home_and_outdoor/lamp.png"},
    {"name": "Kitchen Dish Set", "price": 19.00, "category": "home_outdoor", "stock": 33, "rating": 4.1,
     "description": "Durable everyday kitchen dish set.",
     "image": "Home_Page_Images/home_and_outdoor/bed.png"},
    {"name": "Kitchen Mixer", "price": 39.00, "category": "home_outdoor", "stock": 16, "rating": 4.3,
     "description": "High-speed kitchen mixer for baking.",
     "image": "Home_Page_Images/home_and_outdoor/juicer.png"},
    {"name": "Coffee Maker Deluxe", "price": 35.00, "category": "home_outdoor", "stock": 19, "rating": 4.2,
     "description": "Drip coffee maker with auto shut-off.",
     "image": "Home_Page_Images/home_and_outdoor/cofee_maker.png"},
    {"name": "Outdoor Travel Bag", "price": 29.00, "category": "home_outdoor", "stock": 24, "rating": 4.0,
     "description": "Spacious travel bag for outdoor trips.",
     "image": "Home_Page_Images/home_and_outdoor/bags.png"},

    # --- Clothing ---
    {"name": "Men's Polo T-Shirt", "price": 10.30, "category": "clothing", "stock": 80, "rating": 4.0,
     "description": "T-shirt with multiple colors available, for men.",
     "image": "Home_Page_Images/Recommended_items/shirt.png"},
    {"name": "Denim Jacket", "price": 24.30, "category": "clothing", "stock": 40, "rating": 4.1,
     "description": "Classic denim jacket for everyday wear.",
     "image": "Home_Page_Images/Recommended_items/jacket.png"},
    {"name": "Winter Coat - Brown", "price": 32.50, "category": "clothing", "stock": 20, "rating": 4.4,
     "description": "Brown winter coat, medium size, warm fleece lining.",
     "image": "Home_Page_Images/Recommended_items/coat.png"},
    {"name": "Casual Shorts", "price": 9.99, "category": "clothing", "stock": 55, "rating": 3.9,
     "description": "Lightweight casual shorts for summer.",
     "image": "Home_Page_Images/Recommended_items/half_pent.png"},

    # --- Accessories ---
    {"name": "Travel Duffel Bag", "price": 34.00, "category": "accessories", "stock": 30, "rating": 4.0,
     "description": "Durable jeans-style duffel bag for travel.",
     "image": "Home_Page_Images/Recommended_items/bag.png"},
    {"name": "School Backpack", "price": 27.00, "category": "accessories", "stock": 45, "rating": 4.2,
     "description": "Spacious school backpack with laptop sleeve.",
     "image": "Home_Page_Images/Recommended_items/school_bag.png"},
    {"name": "Leather Wallet", "price": 14.30, "category": "accessories", "stock": 60, "rating": 4.1,
     "description": "Genuine leather wallet with card slots.",
     "image": "Home_Page_Images/Recommended_items/matka.png"},
    {"name": "Wireless Earbuds White", "price": 8.99, "category": "accessories", "stock": 70, "rating": 3.8,
     "description": "Compact wireless earbuds with charging case.",
     "image": "Home_Page_Images/Recommended_items/white_headphone.png"},
]


class Command(BaseCommand):
    help = "Seed the database with sample products (copies demo images into MEDIA_ROOT)."

    def handle(self, *args, **options):
        media_products_dir = Path(settings.MEDIA_ROOT) / "products"
        media_products_dir.mkdir(parents=True, exist_ok=True)

        created_count = 0
        updated_count = 0

        for item in SAMPLE_PRODUCTS:
            source_path = Path(settings.BASE_DIR) / "static" / "Images" / item["image"]

            dest_filename = Path(item["image"]).name
            dest_path = media_products_dir / dest_filename

            if source_path.exists() and not dest_path.exists():
                shutil.copy(source_path, dest_path)

            relative_image_path = f"products/{dest_filename}" if dest_path.exists() else None

            product, created = Product.objects.update_or_create(
                name=item["name"],
                defaults={
                    "price": item["price"],
                    "old_price": item.get("old_price"),
                    "description": item["description"],
                    "category": item["category"],
                    "stock": item["stock"],
                    "is_featured": item.get("is_featured", False),
                    "rating": item.get("rating", 4.0),
                    "image": relative_image_path,
                },
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Done. Created {created_count} products, updated {updated_count} existing ones."
        ))
