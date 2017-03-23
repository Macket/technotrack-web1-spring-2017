import os

from django.conf import settings

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Drop and re-create the database"

    def handle(self, *args, **options):
        import MySQLdb

        self.stdout.write("Connecting...")
        db = MySQLdb.connect(host=settings.DATABASES['default']['HOST'] or "localhost",
                             user=settings.DATABASES['default']['USER'],
                             passwd=settings.DATABASES['default']['PASSWORD'], port=int(3306))

        cursor = db.cursor()
        self.stdout.write("Dropping database %s" % settings.DATABASES['default']['NAME'])
        cursor.execute("drop database %s; create database %s;" % (
            settings.DATABASES['default']['NAME'], settings.DATABASES['default']['NAME']))
        self.stdout.write("Dropped")
        self.delete_migrations_files()
        self.stdout.write("Done!")

    def delete_migrations_files(self):
        self.stdout.write("Deleting migrations' files:")
        for root, _, files in os.walk("."):
            if "migrations" in root:
                for filename in files:
                    if "__init__" not in filename:
                        full_filename = os.sep.join((root, filename))
                        self.stdout.write("\t%s" % full_filename)
                        os.remove(full_filename)