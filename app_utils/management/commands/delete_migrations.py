import os
import pathlib
from django.core.management.base import BaseCommand, CommandError
import glob

current_path = pathlib.Path(__file__).parent.parent.parent.parent.resolve()


# ---- Run Command
class Command(BaseCommand):
    help = 'delete all app migrations'

    def handle(self, *args, **options):
        try:
            all_file = glob.glob(f"{current_path}/*/migrations/*.py", recursive=True)

            for file in all_file:
                if not file.endswith("__init__.py"):
                    os.remove(file)
            # --- response
            self.stdout.write(self.style.SUCCESS('Successfully Delete All Migrations'))
        except:
            raise CommandError("something went wrong")
