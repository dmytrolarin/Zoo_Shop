from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction

from shop_app.models import Brand, FilterGroup, FilterItem, Packing, Product, TypeOfProduct


TYPE_SPECS = {
    "dog_food": {
        "name": "Dog food",
        "image_asset": "shop_app/img/home/dog.png",
        "filters": [
            ("Protein source", ["Beef", "Chicken", "Lamb"]),
            ("Age", ["Puppy", "Adult", "Senior"]),
        ],
    },
    "cat_food": {
        "name": "Cat food",
        "image_asset": "shop_app/img/home/cat.png",
        "filters": [
            ("Protein source", ["Chicken", "Tuna", "Salmon"]),
            ("Age", ["Kitten", "Adult", "Mature 7+"]),
        ],
    },
    "wet_food": {
        "name": "Wet food",
        "image_asset": "shop_app/img/products/product.png",
        "filters": [
            ("Texture", ["Pate", "Shreds in Sauce", "Loaf in Sauce", "Thin Slices in Gravy"]),
            ("Pet type", ["Adult cats", "Kittens"]),
        ],
    },
    "care_and_hygiene": {
        "name": "Care and hygiene",
        "image_asset": "shop_app/img/assortment/brands-logos/logo.png",
        "filters": [
            ("Product type", ["Shampoo", "Dental care", "Ear care", "Paw care"]),
            ("Pet type", ["Dogs", "Cats", "Universal"]),
        ],
    },
}

BRAND_SPECS = {
    "Pedigree": {
        "segment": "eco",
        "logo_url": "https://static.cdnlogo.com/logos/p/37/pedigree.svg",
    },
    "IAMS": {
        "segment": "premium",
        "logo_url": "https://static.cdnlogo.com/logos/i/33/iams.svg",
    },
    "Royal Canin": {
        "segment": "super-premium",
        "logo_url": "https://static.cdnlogo.com/logos/r/35/royal-canin.svg",
    },
    "Whiskas": {
        "segment": "eco",
        "logo_url": "https://static.cdnlogo.com/logos/w/40/whiskas.svg",
    },
    "Hill's Science Diet": {
        "segment": "premium",
        "logo_url": "https://static.cdnlogo.com/logos/h/82/hills.svg",
    },
    "Friskies": {
        "segment": "eco",
        "logo_url": "https://static.cdnlogo.com/logos/f/84/friskies.svg",
    },
    "TRIXIE": {
        "segment": "eco",
        "logo_url": "https://www.trixie.de/_next/static/media/TRIXIE_LOGO_RGB_Rot_NEW2024.5a8a215d.png",
    },
    "TropiClean": {
        "segment": "premium",
        "logo_url": "https://tropiclean.com/cdn/shop/files/TClogo-CoreGreen_eda95612-d68c-4fb0-ba66-0ad7b0a16e9b.png?v=1768940581&width=500",
    },
    "Virbac": {
        "segment": "super-premium",
        "logo_url": "https://static.cdnlogo.com/logos/v/72/virbac.svg",
    },
}

CATALOG = {
    "dog_food": {
        "eco": {
            "brand": "Pedigree",
            "products": [
                {
                    "vendor_code": "REAL-DOG-PED-001",
                    "name": "PEDIGREE Adult Complete Nutrition Grilled Steak & Vegetable Flavor Dry Dog Food",
                    "description": "Real dry dog food by Pedigree for adult dogs with a steak and vegetable recipe.",
                    "age": "Adult",
                    "protein": "Beef",
                    "packings": [(2, 18, None), (10, 54, 59)],
                    "filters": ["Beef", "Adult"],
                },
                {
                    "vendor_code": "REAL-DOG-PED-002",
                    "name": "PEDIGREE Puppy Growth & Protection Chicken & Vegetable Flavor Dry Dog Food",
                    "description": "Real Pedigree puppy formula with chicken and vegetables for growing dogs.",
                    "age": "Puppy",
                    "protein": "Chicken",
                    "packings": [(2, 17, None), (12, 58, None)],
                    "filters": ["Chicken", "Puppy"],
                },
                {
                    "vendor_code": "REAL-DOG-PED-003",
                    "name": "PEDIGREE High Protein Beef & Lamb Flavor Adult Dry Dog Food",
                    "description": "Real high-protein Pedigree dry dog food for adult dogs with beef and lamb flavors.",
                    "age": "Senior",
                    "protein": "Lamb",
                    "packings": [(3, 23, None), (14, 65, 72)],
                    "filters": ["Lamb", "Senior"],
                },
            ],
        },
        "premium": {
            "brand": "IAMS",
            "products": [
                {
                    "vendor_code": "REAL-DOG-IAM-001",
                    "name": "IAMS Proactive Health Healthy Puppy Dry Dog Food with Real Chicken",
                    "description": "Real IAMS puppy kibble with chicken for healthy growth and daily feeding.",
                    "age": "Puppy",
                    "protein": "Chicken",
                    "packings": [(3, 24, None), (13, 67, None)],
                    "filters": ["Chicken", "Puppy"],
                },
                {
                    "vendor_code": "REAL-DOG-IAM-002",
                    "name": "IAMS Proactive Health Adult Minichunks Lamb & Rice Recipe Dry Dog Food",
                    "description": "Real IAMS adult dry dog food with lamb and rice in smaller kibble pieces.",
                    "age": "Adult",
                    "protein": "Lamb",
                    "packings": [(3, 25, None), (15, 73, 79)],
                    "filters": ["Lamb", "Adult"],
                },
                {
                    "vendor_code": "REAL-DOG-IAM-003",
                    "name": "IAMS Proactive Health Adult Minichunks Beef & Rice Recipe Dry Dog Food",
                    "description": "Real IAMS adult dog food with beef and rice for daily feeding.",
                    "age": "Senior",
                    "protein": "Beef",
                    "packings": [(3, 26, None), (15, 75, None)],
                    "filters": ["Beef", "Senior"],
                },
            ],
        },
        "super-premium": {
            "brand": "Royal Canin",
            "products": [
                {
                    "vendor_code": "REAL-DOG-RC-001",
                    "name": "Royal Canin Mini Puppy Dry Dog Food",
                    "description": "Real Royal Canin dry dog food for small-breed puppies.",
                    "age": "Puppy",
                    "protein": "Chicken",
                    "packings": [(1, 22, None), (8, 88, 94)],
                    "filters": ["Chicken", "Puppy"],
                },
                {
                    "vendor_code": "REAL-DOG-RC-002",
                    "name": "Royal Canin Maxi Adult Dry Dog Food",
                    "description": "Real Royal Canin adult dog food formulated for large-breed dogs.",
                    "age": "Adult",
                    "protein": "Chicken",
                    "packings": [(3, 32, None), (15, 108, None)],
                    "filters": ["Chicken", "Adult"],
                },
                {
                    "vendor_code": "REAL-DOG-RC-003",
                    "name": "Royal Canin Medium Aging 10+ Dry Dog Food",
                    "description": "Real Royal Canin dry dog food for mature medium-breed dogs aged 10 and over.",
                    "age": "Senior",
                    "protein": "Chicken",
                    "packings": [(3, 34, None), (15, 114, 122)],
                    "filters": ["Chicken", "Senior"],
                },
            ],
        },
    },
    "cat_food": {
        "eco": {
            "brand": "Whiskas",
            "products": [
                {
                    "vendor_code": "REAL-CAT-WHI-001",
                    "name": "WHISKAS Kitten Dry Food with Real Chicken",
                    "description": "Real Whiskas dry cat food for kittens with real chicken.",
                    "age": "Kitten",
                    "protein": "Chicken",
                    "packings": [(1, 9, None), (7, 34, None)],
                    "filters": ["Chicken", "Kitten"],
                },
                {
                    "vendor_code": "REAL-CAT-WHI-002",
                    "name": "WHISKAS Adult 1+ Chicken Flavour Dry Cat Food",
                    "description": "Real Whiskas adult dry cat food with chicken flavour.",
                    "age": "Adult",
                    "protein": "Chicken",
                    "packings": [(2, 14, None), (7, 36, 41)],
                    "filters": ["Chicken", "Adult"],
                },
                {
                    "vendor_code": "REAL-CAT-WHI-003",
                    "name": "WHISKAS Adult 7+ Chicken Flavour Dry Cat Food",
                    "description": "Real Whiskas mature cat dry food formulated for cats aged 7 years and older.",
                    "age": "Mature 7+",
                    "protein": "Chicken",
                    "packings": [(2, 15, None), (7, 39, None)],
                    "filters": ["Chicken", "Mature 7+"],
                },
            ],
        },
        "premium": {
            "brand": "Hill's Science Diet",
            "products": [
                {
                    "vendor_code": "REAL-CAT-HIL-001",
                    "name": "Hill's Science Diet Adult Indoor Chicken Recipe Cat Food",
                    "description": "Real Hill's Science Diet indoor dry food for adult cats.",
                    "age": "Adult",
                    "protein": "Chicken",
                    "packings": [(2, 21, None), (7, 52, None)],
                    "filters": ["Chicken", "Adult"],
                },
                {
                    "vendor_code": "REAL-CAT-HIL-002",
                    "name": "Hill's Science Diet Kitten Chicken Recipe Cat Food",
                    "description": "Real Hill's Science Diet kitten dry cat food with chicken recipe.",
                    "age": "Kitten",
                    "protein": "Chicken",
                    "packings": [(2, 22, None), (7, 57, 63)],
                    "filters": ["Chicken", "Kitten"],
                },
                {
                    "vendor_code": "REAL-CAT-HIL-003",
                    "name": "Hill's Science Diet Adult 7+ Indoor Chicken Recipe Cat Food",
                    "description": "Real Hill's Science Diet mature indoor dry cat food for cats age 7+.",
                    "age": "Mature 7+",
                    "protein": "Chicken",
                    "packings": [(2, 23, None), (7, 59, None)],
                    "filters": ["Chicken", "Mature 7+"],
                },
            ],
        },
        "super-premium": {
            "brand": "Royal Canin",
            "products": [
                {
                    "vendor_code": "REAL-CAT-RC-001",
                    "name": "Royal Canin Kitten Dry Cat Food",
                    "description": "Real Royal Canin dry cat food for kittens in the growth stage.",
                    "age": "Kitten",
                    "protein": "Chicken",
                    "packings": [(1, 24, None), (4, 68, None)],
                    "filters": ["Chicken", "Kitten"],
                },
                {
                    "vendor_code": "REAL-CAT-RC-002",
                    "name": "Royal Canin Indoor Adult Dry Cat Food",
                    "description": "Real Royal Canin dry cat food for indoor adult cats.",
                    "age": "Adult",
                    "protein": "Chicken",
                    "packings": [(2, 33, None), (7, 86, 92)],
                    "filters": ["Chicken", "Adult"],
                },
                {
                    "vendor_code": "REAL-CAT-RC-003",
                    "name": "Royal Canin Indoor 7+ Dry Cat Food",
                    "description": "Real Royal Canin dry cat food for mature indoor cats age 7+.",
                    "age": "Mature 7+",
                    "protein": "Chicken",
                    "packings": [(2, 35, None), (7, 91, None)],
                    "filters": ["Chicken", "Mature 7+"],
                },
            ],
        },
    },
    "wet_food": {
        "eco": {
            "brand": "Friskies",
            "products": [
                {
                    "vendor_code": "REAL-WET-FRI-001",
                    "name": "Friskies Paté Chicken & Tuna Dinner Wet Cat Food",
                    "description": "Real Friskies wet cat food in a smooth pate texture with chicken and tuna.",
                    "age": "Adult",
                    "protein": "Chicken",
                    "packings": [(1, 2, None), (12, 19, None)],
                    "filters": ["Pate", "Adult cats"],
                },
                {
                    "vendor_code": "REAL-WET-FRI-002",
                    "name": "Friskies Shreds With Ocean Whitefish & Tuna In Sauce Wet Cat Food",
                    "description": "Real Friskies wet cat food with shredded pieces in sauce.",
                    "age": "Adult",
                    "protein": "Tuna",
                    "packings": [(1, 2, None), (12, 21, 24)],
                    "filters": ["Shreds in Sauce", "Adult cats"],
                },
                {
                    "vendor_code": "REAL-WET-FRI-003",
                    "name": "Friskies Extra Gravy Chunky With Turkey In Savory Gravy Wet Cat Food",
                    "description": "Real Friskies chunky wet cat food with turkey in gravy.",
                    "age": "Adult",
                    "protein": "Chicken",
                    "packings": [(1, 2, None), (12, 20, None)],
                    "filters": ["Shreds in Sauce", "Adult cats"],
                },
            ],
        },
        "premium": {
            "brand": "Hill's Science Diet",
            "products": [
                {
                    "vendor_code": "REAL-WET-HIL-001",
                    "name": "Hill's Science Diet Adult Savory Chicken Entree Canned Cat Food",
                    "description": "Real Hill's Science Diet wet cat food with savory chicken entree.",
                    "age": "Adult",
                    "protein": "Chicken",
                    "packings": [(1, 4, None), (12, 36, None)],
                    "filters": ["Pate", "Adult cats"],
                },
                {
                    "vendor_code": "REAL-WET-HIL-002",
                    "name": "Hill's Science Diet Kitten Tender Chicken Dinner Canned Cat Food",
                    "description": "Real Hill's Science Diet wet kitten food with chicken dinner.",
                    "age": "Kitten",
                    "protein": "Chicken",
                    "packings": [(1, 4, None), (12, 39, 44)],
                    "filters": ["Loaf in Sauce", "Kittens"],
                },
                {
                    "vendor_code": "REAL-WET-HIL-003",
                    "name": "Hill's Science Diet Adult Tender Tuna Dinner Canned Cat Food",
                    "description": "Real Hill's Science Diet wet cat food with tuna dinner.",
                    "age": "Adult",
                    "protein": "Tuna",
                    "packings": [(1, 4, None), (12, 38, None)],
                    "filters": ["Loaf in Sauce", "Adult cats"],
                },
            ],
        },
        "super-premium": {
            "brand": "Royal Canin",
            "products": [
                {
                    "vendor_code": "REAL-WET-RC-001",
                    "name": "Royal Canin Adult Instinctive Loaf in Sauce Wet Cat Food",
                    "description": "Real Royal Canin wet cat food in loaf-in-sauce texture for adult cats.",
                    "age": "Adult",
                    "protein": "Chicken",
                    "packings": [(1, 5, None), (12, 49, None)],
                    "filters": ["Loaf in Sauce", "Adult cats"],
                },
                {
                    "vendor_code": "REAL-WET-RC-002",
                    "name": "Royal Canin Kitten Thin Slices in Gravy Canned Cat Food",
                    "description": "Real Royal Canin wet kitten food with thin slices in gravy.",
                    "age": "Kitten",
                    "protein": "Chicken",
                    "packings": [(1, 5, None), (12, 52, 57)],
                    "filters": ["Thin Slices in Gravy", "Kittens"],
                },
                {
                    "vendor_code": "REAL-WET-RC-003",
                    "name": "Royal Canin Instinctive 7+ Thin Slices in Gravy Canned Cat Food",
                    "description": "Real Royal Canin wet cat food for mature cats with thin slices in gravy.",
                    "age": "Adult",
                    "protein": "Chicken",
                    "packings": [(1, 5, None), (12, 53, None)],
                    "filters": ["Thin Slices in Gravy", "Adult cats"],
                },
            ],
        },
    },
    "care_and_hygiene": {
        "eco": {
            "brand": "TRIXIE",
            "products": [
                {
                    "vendor_code": "REAL-CARE-TRI-001",
                    "name": "TRIXIE Orange Shampoo",
                    "description": "Real TRIXIE shampoo for deep cleaning and coat shine.",
                    "age": "",
                    "protein": "",
                    "packings": [(1, 7, None), (2, 12, None)],
                    "filters": ["Shampoo", "Dogs"],
                },
                {
                    "vendor_code": "REAL-CARE-TRI-002",
                    "name": "TRIXIE Ear Care",
                    "description": "Real TRIXIE ear care solution for cleansing and deodorising ears.",
                    "age": "",
                    "protein": "",
                    "packings": [(1, 6, None), (2, 11, 13)],
                    "filters": ["Ear care", "Universal"],
                },
                {
                    "vendor_code": "REAL-CARE-TRI-003",
                    "name": "TRIXIE Paw Care Cream",
                    "description": "Real TRIXIE paw care cream with beeswax for dogs and cats.",
                    "age": "",
                    "protein": "",
                    "packings": [(1, 6, None), (2, 10, None)],
                    "filters": ["Paw care", "Universal"],
                },
            ],
        },
        "premium": {
            "brand": "TropiClean",
            "products": [
                {
                    "vendor_code": "REAL-CARE-TRO-001",
                    "name": "TropiClean OxyMed Hypoallergenic Shampoo for Dogs & Cats",
                    "description": "Real TropiClean hypoallergenic shampoo for dogs and cats.",
                    "age": "",
                    "protein": "",
                    "packings": [(1, 12, None), (2, 19, None)],
                    "filters": ["Shampoo", "Universal"],
                },
                {
                    "vendor_code": "REAL-CARE-TRO-002",
                    "name": "TropiClean Fresh Breath Oral Care Gel for Dogs",
                    "description": "Real TropiClean no-brushing oral care gel for dogs.",
                    "age": "",
                    "protein": "",
                    "packings": [(1, 13, None), (2, 21, 24)],
                    "filters": ["Dental care", "Dogs"],
                },
                {
                    "vendor_code": "REAL-CARE-TRO-003",
                    "name": "TropiClean Fresh Breath Oral Care Gel for Cats",
                    "description": "Real TropiClean no-brushing oral care gel for cats.",
                    "age": "",
                    "protein": "",
                    "packings": [(1, 13, None), (2, 21, None)],
                    "filters": ["Dental care", "Cats"],
                },
            ],
        },
        "super-premium": {
            "brand": "Virbac",
            "products": [
                {
                    "vendor_code": "REAL-CARE-VIR-001",
                    "name": "Virbac EPI-SOOTHE Shampoo",
                    "description": "Real Virbac shampoo designed to soothe and cleanse dry, sensitive skin.",
                    "age": "",
                    "protein": "",
                    "packings": [(1, 18, None), (2, 32, None)],
                    "filters": ["Shampoo", "Universal"],
                },
                {
                    "vendor_code": "REAL-CARE-VIR-002",
                    "name": "Virbac C.E.T. Enzymatic Toothpaste",
                    "description": "Real Virbac enzymatic toothpaste for dogs and cats.",
                    "age": "",
                    "protein": "",
                    "packings": [(1, 15, None), (2, 28, 31)],
                    "filters": ["Dental care", "Universal"],
                },
                {
                    "vendor_code": "REAL-CARE-VIR-003",
                    "name": "Virbac EPIOTIC Advanced Ear Cleanser",
                    "description": "Real Virbac ear cleanser for routine cleansing in dogs and cats.",
                    "age": "",
                    "protein": "",
                    "packings": [(1, 17, None), (2, 30, None)],
                    "filters": ["Ear care", "Universal"],
                },
            ],
        },
    },
}

OLD_BRAND_NAMES = {
    "Eco Bark",
    "Premium Bark",
    "Royal Bark",
    "Eco Whisker",
    "Premium Whisker",
    "Royal Whisker",
    "Eco Tender",
    "Premium Tender",
    "Royal Tender",
    "Eco Care",
    "Premium Care",
    "Royal Care",
}
OLD_VENDOR_PREFIXES = ("ZF-", "DOG-", "CAT-", "WET-", "CARE-", "REAL-")


class Command(BaseCommand):
    help = "Seed the catalog with real pet brands and products across all shop segments."

    def handle(self, *args, **options):
        self.static_dir = Path(settings.BASE_DIR) / "shop_app" / "static"
        with transaction.atomic():
            self._remove_old_seed()
            self._seed_types()
            self._seed_filters()
            self._seed_brands()
            self._seed_products()
        self.stdout.write(self.style.SUCCESS("Real catalog seeded successfully."))

    def _remove_old_seed(self):
        for prefix in OLD_VENDOR_PREFIXES:
            Product.objects.filter(vendor_code__startswith=prefix).delete()
        Brand.objects.filter(name__in=OLD_BRAND_NAMES).delete()
        FilterGroup.objects.all().delete()

    def _seed_types(self):
        self.types_by_slug = {}
        for type_slug, spec in TYPE_SPECS.items():
            product_type, _ = TypeOfProduct.objects.update_or_create(
                url_name=type_slug,
                defaults={"name": spec["name"]},
            )
            self._assign_static_image(
                product_type.image,
                spec["image_asset"],
                f"{type_slug}{Path(spec['image_asset']).suffix}",
            )
            self.types_by_slug[type_slug] = product_type

    def _seed_filters(self):
        self.filter_items = {}
        for type_slug, spec in TYPE_SPECS.items():
            for title, item_names in spec["filters"]:
                group_slug = f"{type_slug}-{self._slugify(title)}"
                filter_group = FilterGroup.objects.create(title=title, slug=group_slug)
                filter_group.type_of_products.set([self.types_by_slug[type_slug]])
                for item_name in item_names:
                    item_slug = f"{group_slug}-{self._slugify(item_name)}"
                    filter_item = FilterItem.objects.create(
                        name=item_name,
                        filter_group=filter_group,
                        slug=item_slug,
                    )
                    self.filter_items[(type_slug, item_name)] = filter_item

    def _seed_brands(self):
        self.brands_by_name = {}
        brand_types: dict[str, set[str]] = {}
        for type_slug, segment_map in CATALOG.items():
            for segment_data in segment_map.values():
                brand_types.setdefault(segment_data["brand"], set()).add(type_slug)

        for brand_name, spec in BRAND_SPECS.items():
            brand, _ = Brand.objects.update_or_create(
                name=brand_name,
                defaults={"segment": spec["segment"]},
            )
            type_objects = [self.types_by_slug[type_slug] for type_slug in sorted(brand_types.get(brand_name, []))]
            brand.type_of_products.set(type_objects)
            self._assign_remote_image(
                brand.image,
                spec["logo_url"],
                f"{self._slugify(brand_name)}",
                fallback_asset="shop_app/img/assortment/brands-logos/logo.png",
            )
            self.brands_by_name[brand_name] = brand

    def _seed_products(self):
        seed_vendor_codes = []
        for type_slug, segment_map in CATALOG.items():
            type_obj = self.types_by_slug[type_slug]
            for segment_key, data in segment_map.items():
                brand = self.brands_by_name[data["brand"]]
                for product_index, product_spec in enumerate(data["products"], start=1):
                    vendor_code = product_spec["vendor_code"]
                    seed_vendor_codes.append(vendor_code)
                    product, _ = Product.objects.update_or_create(
                        vendor_code=vendor_code,
                        defaults={
                            "name": product_spec["name"],
                            "type_of_product": type_obj,
                            "brand": brand,
                            "description": product_spec["description"],
                            "in_stock": True,
                            "age_of_animal": product_spec["age"],
                            "source_of_protein": product_spec["protein"],
                            "is_hit": product_index == 1,
                        },
                    )
                    self._assign_static_image(
                        product.image,
                        "shop_app/img/products/product.png",
                        f"{vendor_code.lower()}.png",
                    )
                    product.filter_items.set(
                        [self.filter_items[(type_slug, item_name)] for item_name in product_spec["filters"]]
                    )
                    self._sync_packings(product, product_spec["packings"])

        Product.objects.filter(vendor_code__startswith="REAL-").exclude(vendor_code__in=seed_vendor_codes).delete()

    def _sync_packings(self, product: Product, packings: list[tuple[int, int, int | None]]):
        existing_weights = set(Packing.objects.filter(product=product).values_list("weight", flat=True))
        desired_weights = set()
        for weight, current_price, old_price in packings:
            desired_weights.add(weight)
            Packing.objects.update_or_create(
                product=product,
                weight=weight,
                defaults={"current_price": current_price, "old_price": old_price},
            )
        Packing.objects.filter(product=product, weight__in=existing_weights - desired_weights).delete()

    def _assign_static_image(self, field_file, relative_asset_path: str, target_name: str):
        source_path = self.static_dir / relative_asset_path
        with source_path.open("rb") as source_file:
            field_file.save(target_name, ContentFile(source_file.read()), save=True)

    def _assign_remote_image(self, field_file, url: str, target_base_name: str, fallback_asset: str):
        try:
            content, suffix = self._download_file(url)
            field_file.save(f"{target_base_name}{suffix}", ContentFile(content), save=True)
        except Exception:
            self._assign_static_image(
                field_file,
                fallback_asset,
                f"{target_base_name}{Path(fallback_asset).suffix}",
            )

    def _download_file(self, url: str) -> tuple[bytes, str]:
        request = Request(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"
                )
            },
        )
        with urlopen(request, timeout=30) as response:
            content = response.read()
            content_type = response.headers.get("Content-Type", "").lower()
        return content, self._get_extension(url, content_type)

    def _get_extension(self, url: str, content_type: str) -> str:
        path = urlparse(url).path.lower()
        for suffix in (".svg", ".png", ".jpg", ".jpeg", ".webp"):
            if path.endswith(suffix):
                return suffix
        if "svg" in content_type:
            return ".svg"
        if "png" in content_type:
            return ".png"
        if "webp" in content_type:
            return ".webp"
        if "jpeg" in content_type or "jpg" in content_type:
            return ".jpg"
        return ".png"

    def _slugify(self, value: str) -> str:
        return (
            value.lower()
            .replace("&", "and")
            .replace("®", "")
            .replace("™", "")
            .replace("+", "plus")
            .replace("'", "")
            .replace(".", "")
            .replace("(", "")
            .replace(")", "")
            .replace("/", "-")
            .replace(" ", "-")
        )
