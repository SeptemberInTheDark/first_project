import csv
from datetime import date
from decimal import Decimal
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify

from app.models import Phone


class Command(BaseCommand):
    help = "Import phones from a semicolon-delimited CSV file."

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            dest="path",
            default=None,
            help="Path to phones.csv (default: BASE_DIR/phones.csv)",
        )

    def handle(self, *args, **options):
        from django.conf import settings

        csv_path = options.get("path")
        if csv_path:
            path = Path(csv_path)
        else:
            path = Path(settings.BASE_DIR) / "phones.csv"

        if not path.exists():
            raise CommandError(f"CSV file not found: {path}")

        with path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f, delimiter=";")
            required = {"id", "name", "image", "price", "release_date", "lte_exists"}
            if not required.issubset(set(reader.fieldnames or [])):
                raise CommandError(
                    f"CSV must contain headers: {sorted(required)}. "
                    f"Got: {reader.fieldnames}"
                )

            created = 0
            updated = 0

            for row in reader:
                phone_id = int(row["id"])
                name = (row["name"] or "").strip()
                image = (row["image"] or "").strip()
                price = Decimal(str(row["price"]).strip())
                release_date = date.fromisoformat(str(row["release_date"]).strip())
                lte_exists = str(row["lte_exists"]).strip().lower() in {"true", "1", "yes", "y"}

                base_slug = slugify(name)
                slug = base_slug or str(phone_id)
                if Phone.objects.exclude(id=phone_id).filter(slug=slug).exists():
                    slug = f"{slug}-{phone_id}"

                obj, was_created = Phone.objects.update_or_create(
                    id=phone_id,
                    defaults={
                        "name": name,
                        "image": image,
                        "price": price,
                        "release_date": release_date,
                        "lte_exists": lte_exists,
                        "slug": slug,
                    },
                )
                if was_created:
                    created += 1
                else:
                    updated += 1

        self.stdout.write(self.style.SUCCESS(f"Import complete. Created: {created}, updated: {updated}"))
