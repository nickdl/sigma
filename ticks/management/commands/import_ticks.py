from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils import timezone
from itertools import islice
from datetime import datetime
import os
import csv
from ticks.models import Tick


class Command(BaseCommand):
    help = 'Imports ticks from csv file'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+')
        parser.add_argument(
            '--delete',
            action='store_true',
            dest='delete',
            help='Delete existing ticks'
        )

    def handle(self, *args, **options):
        if options['delete']:
            self.stdout.write(self.style.SUCCESS('Deleting existing ticks...'))
            Tick.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Deleted existing ticks'))

        file = os.path.join(settings.BASE_DIR, options['file'][0])
        if os.path.isfile(file):
            with open(file, 'r') as f:
                reader = csv.DictReader(f)
                self.stdout.write(self.style.SUCCESS('Importing ticks...'))
                batch_size = 1000
                while True:
                    batch = list(islice(reader, batch_size))
                    if not batch:
                        break
                    ticks = []
                    for row in batch:
                        for symbol in settings.SYMBOLS:
                            date = timezone.make_aware(
                                datetime.fromtimestamp(int(row['date'])),
                                timezone.get_current_timezone()
                            )
                            ticks.append(Tick(
                                date=date,
                                symbol=symbol,
                                open=row[symbol + '_open'],
                                high=row[symbol + '_high'],
                                low=row[symbol + '_low'],
                                close=row[symbol + '_close'],
                                volume=row[symbol + '_volume'],
                            ))
                    Tick.objects.bulk_create(ticks)
            self.stdout.write(self.style.SUCCESS('Successfully imported ticks'))
        else:
            raise CommandError('file %s does not exist' % file)
