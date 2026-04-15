from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction

from shop_app.models import Brand, FilterGroup, FilterItem, Packing, Product, TypeOfProduct


TYPE_SPECS = [
    {
        "name": "Dog food",
        "url_name": "dog_food",
        "image_asset": "shop_app/img/home/dog.png",
        "brand_prefix": "Bark",
        "products": [
            ("Chicken Adult", "Adult", "Chicken"),
            ("Lamb Puppy", "Puppy", "Lamb"),
            ("Turkey Senior", "Senior", "Turkey"),
        ],
        "filters": [
            ("Protein source", ["Chicken", "Lamb", "Turkey"]),
            ("Age", ["Puppy", "Adult", "Senior"]),
        ],
        "packings": [
            [(2, 420, None), (10, 1490, 1650)],
            [(2, 455, None), (8, 1590, None), (12, 2190, 2390)],
            [(2, 470, None), (7, 1410, None)],
        ],
    },
    {
        "name": "Cat food",
        "url_name": "cat_food",
        "image_asset": "shop_app/img/home/cat.png",
        "brand_prefix": "Whisker",
        "products": [
            ("Chicken Kitten", "Kitten", "Chicken"),
            ("Salmon Adult", "Adult", "Salmon"),
            ("Duck Sterilised", "Sterilised", "Duck"),
        ],
        "filters": [
            ("Protein source", ["Chicken", "Salmon", "Duck"]),
            ("Age", ["Kitten", "Adult", "Sterilised"]),
        ],
        "packings": [
            [(1, 295, None), (3, 865, None)],
            [(1, 320, None), (4, 980, 1090), (10, 2280, None)],
            [(1, 335, None), (4, 1025, None)],
        ],
    },
    {
        "name": "Wet food",
        "url_name": "wet_food",
        "image_asset": "shop_app/img/products/product.png",
        "brand_prefix": "Tender",
        "products": [
            ("Chicken Pate", "Adult", "Chicken"),
            ("Salmon Mousse", "Adult", "Salmon"),
            ("Turkey Chunks", "Adult", "Turkey"),
        ],
        "filters": [
            ("Texture", ["Pate", "Mousse", "Chunks in gravy"]),
            ("Purpose", ["Daily menu", "Sensitive digestion", "Indoor pets"]),
        ],
        "packings": [
            [(1, 95, None), (3, 255, None)],
            [(1, 108, None), (6, 590, 660)],
            [(1, 104, None), (6, 565, None), (12, 1080, 1190)],
        ],
    },
    {
        "name": "Care and hygiene",
        "url_name": "care_and_hygiene",
        "image_asset": "shop_app/img/assortment/brands-logos/logo.png",
        "brand_prefix": "Care",
        "products": [
            ("Sensitive Shampoo", "", ""),
            ("Dental Gel", "", ""),
            ("Paw Balm", "", ""),
        ],
        "filters": [
            ("Product type", ["Shampoo", "Dental care", "Paw balm"]),
            ("Pet type", ["Dogs", "Cats", "Universal"]),
        ],
        "packings": [
            [(1, 180, None), (2, 320, None)],
            [(1, 210, None), (2, 390, 430), (3, 540, None)],
            [(1, 195, None), (2, 360, None)],
        ],
    },
]

SEGMENTS = [
    ("eco", "Eco"),
    ("premium", "Premium"),
    ("super-premium", "Royal"),
]

OLD_BRAND_NAMES = {"Paw Daily", "Whisker Bloom", "Vet Harmony", "Clean Tail"}
OLD_VENDOR_PREFIXES = ("DOG-", "CAT-", "WET-", "CARE-")


class Command(BaseCommand):
    help = "Seeds the demo catalog with non-AI local images and at least 3 products per category and segment."

    def handle(self, *args, **options):
        self.static_dir = Path(settings.BASE_DIR) / "shop_app" / "static"
        with transaction.atomic():
            self._remove_old_seed()
            self._seed_types()
            self._seed_filters()
            self._seed_brands()
            self._seed_products()
        self.stdout.write(self.style.SUCCESS("Demo catalog seeded successfully."))

    def _remove_old_seed(self):
        Product.objects.filter(vendor_code__startswith=OLD_VENDOR_PREFIXES[0]).delete()
        Product.objects.filter(vendor_code__startswith=OLD_VENDOR_PREFIXES[1]).delete()
        Product.objects.filter(vendor_code__startswith=OLD_VENDOR_PREFIXES[2]).delete()
        Product.objects.filter(vendor_code__startswith=OLD_VENDOR_PREFIXES[3]).delete()
        Brand.objects.filter(name__in=OLD_BRAND_NAMES).delete()

    def _seed_types(self):
        self.types_by_slug = {}
        for spec in TYPE_SPECS:
            product_type, _ = TypeOfProduct.objects.update_or_create(
                url_name=spec["url_name"],
                defaults={"name": spec["name"]},
            )
            self._assign_static_image(
                product_type.image,
                spec["image_asset"],
                f"{spec['url_name']}{Path(spec['image_asset']).suffix}",
            )
            self.types_by_slug[spec["url_name"]] = product_type

    def _seed_filters(self):
        self.filter_items = {}
        for spec in TYPE_SPECS:
            type_slug = spec["url_name"]
            for title, items in spec["filters"]:
                group_slug = f"{type_slug}-{self._slugify(title)}"
                filter_group, _ = FilterGroup.objects.update_or_create(
                    slug=group_slug,
                    defaults={"title": title},
                )
                filter_group.type_of_products.set([self.types_by_slug[type_slug]])
                for item_name in items:
                    item_slug = f"{group_slug}-{self._slugify(item_name)}"
                    filter_item, _ = FilterItem.objects.update_or_create(
                        slug=item_slug,
                        defaults={"name": item_name, "filter_group": filter_group},
                    )
                    self.filter_items[(type_slug, item_name)] = filter_item

    def _seed_brands(self):
        self.brands_by_key = {}
        for spec in TYPE_SPECS:
            type_slug = spec["url_name"]
            for segment_key, segment_label in SEGMENTS:
                brand_name = f"{segment_label} {spec['brand_prefix']}"
                brand, _ = Brand.objects.update_or_create(
                    name=brand_name,
                    defaults={"segment": segment_key},
                )
                self._assign_static_image(
                    brand.image,
                    "shop_app/img/assortment/brands-logos/logo.png",
                    f"{self._slugify(brand_name)}.png",
                )
                brand.type_of_products.set([self.types_by_slug[type_slug]])
                self.brands_by_key[(type_slug, segment_key)] = brand

    def _seed_products(self):
        seed_vendor_codes = []
        for spec in TYPE_SPECS:
            type_slug = spec["url_name"]
            type_obj = self.types_by_slug[type_slug]
            for segment_index, (segment_key, segment_label) in enumerate(SEGMENTS, start=1):
                brand = self.brands_by_key[(type_slug, segment_key)]
                for product_index, (product_name, age, protein) in enumerate(spec["products"], start=1):
                    vendor_code = f"ZF-{type_slug[:3].upper()}-{segment_index}{product_index:02d}"
                    seed_vendor_codes.append(vendor_code)
                    product, _ = Product.objects.update_or_create(
                        vendor_code=vendor_code,
                        defaults={
                            "name": f"{brand.name} {product_name}",
                            "type_of_product": type_obj,
                            "brand": brand,
                            "description": self._build_description(type_obj.name, product_name, segment_label),
                            "in_stock": True,
                            "age_of_animal": age,
                            "source_of_protein": protein,
                            "is_hit": product_index == 1,
                        },
                    )
                    self._assign_static_image(
                        product.image,
                        "shop_app/img/products/product.png",
                        f"{vendor_code.lower()}.png",
                    )
                    product.filter_items.set(self._get_filter_items(type_slug, product_index, age, protein))
                    self._sync_packings(product, spec["packings"][product_index - 1], segment_index)

        Product.objects.filter(vendor_code__startswith="ZF-").exclude(vendor_code__in=seed_vendor_codes).delete()

    def _get_filter_items(self, type_slug: str, product_index: int, age: str, protein: str):
        if type_slug == "dog_food":
            return [
                self.filter_items[(type_slug, protein)],
                self.filter_items[(type_slug, age)],
            ]
        if type_slug == "cat_food":
            return [
                self.filter_items[(type_slug, protein)],
                self.filter_items[(type_slug, age)],
            ]
        if type_slug == "wet_food":
            texture_names = ["Pate", "Mousse", "Chunks in gravy"]
            purpose_names = ["Daily menu", "Sensitive digestion", "Indoor pets"]
            return [
                self.filter_items[(type_slug, texture_names[product_index - 1])],
                self.filter_items[(type_slug, purpose_names[product_index - 1])],
            ]
        product_type_names = ["Shampoo", "Dental care", "Paw balm"]
        pet_type_names = ["Universal", "Dogs", "Cats"]
        return [
            self.filter_items[(type_slug, product_type_names[product_index - 1])],
            self.filter_items[(type_slug, pet_type_names[product_index - 1])],
        ]

    def _sync_packings(self, product: Product, base_packings: list[tuple[int, int, int | None]], segment_index: int):
        existing_weights = set(Packing.objects.filter(product=product).values_list("weight", flat=True))
        desired_weights = set()
        price_multiplier = 1 + (segment_index - 1) * 0.18
        for weight, current_price, old_price in base_packings:
            adjusted_current_price = int(round(current_price * price_multiplier))
            adjusted_old_price = int(round(old_price * price_multiplier)) if old_price else None
            desired_weights.add(weight)
            Packing.objects.update_or_create(
                product=product,
                weight=weight,
                defaults={
                    "current_price": adjusted_current_price,
                    "old_price": adjusted_old_price,
                },
            )
        Packing.objects.filter(product=product, weight__in=existing_weights - desired_weights).delete()

    def _build_description(self, type_name: str, product_name: str, segment_label: str) -> str:
        return (
            f"{segment_label} line of {type_name.lower()} products. "
            f"{product_name} is added as demo content for catalog pages, filters, and packings."
        )

    def _assign_static_image(self, field_file, relative_asset_path: str, target_name: str):
        source_path = self.static_dir / relative_asset_path
        with source_path.open("rb") as source_file:
            field_file.save(target_name, ContentFile(source_file.read()), save=True)

    def _slugify(self, value: str) -> str:
        return (
            value.lower()
            .replace(" and ", "-")
            .replace(" ", "-")
            .replace("/", "-")
            .replace(".", "")
        )
