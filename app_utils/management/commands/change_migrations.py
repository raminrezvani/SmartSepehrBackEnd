import glob
import pathlib

from django.core.management.base import BaseCommand, CommandError

current_path = pathlib.Path(__file__).parent.parent.parent.parent.resolve()


# ---- Run Command
class Command(BaseCommand):
    help = 'delete all app migrations'

    def handle(self, *args, **options):
        try:
            all_file = glob.glob(f"{current_path}/*/migrations/*.py", recursive=True)

            for file in all_file:
                if not file.endswith("__init__.py"):
                    file_path = file

                    with open(file_path, 'r') as migration_file:
                        file_data = migration_file.read()
                        migration_file.close()

                    old_data = "parler.models.TranslatedFieldsModelMixin"
                    old_data_2 = "parler.models.TranslatableModelMixin"
                    new_data = "parler.models.TranslatableModel"
                    file_data = file_data.replace(old_data, new_data)
                    file_data = file_data.replace(old_data_2, new_data)

                    with open(file_path, 'w') as migration_file:
                        migration_file.write(file_data)
                        migration_file.close()
            # --- response
            self.stdout.write(self.style.SUCCESS('Successfully Worked'))
        except:
            raise CommandError("something went wrong")
