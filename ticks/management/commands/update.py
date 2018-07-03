from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils import timezone
from datetime import timedelta, datetime
from ticks.models import Tick
import requests
import time
import json


class Command(BaseCommand):
    help = 'Update ticks'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            nargs='+',
        )

    def request_ticks(self, from_timestamp, to_timestamp):
        params = {
            'command': 'returnChartData',
            'currencyPair': None,
            'start': None,
            'end': None,
            'period': settings.Q_STEP,
        }

        now = timezone.now()
        if from_timestamp != to_timestamp:
            interval = int(now.timestamp() - (now - timedelta(hours=24)).timestamp())
            timestamps = list(range(from_timestamp, to_timestamp, interval))
            timestamps.append(to_timestamp)
        else:
            timestamps = [from_timestamp, to_timestamp]

        ticks = []
        for index in range(len(timestamps) - 1):
            params['start'] = timestamps[index]
            params['end'] = timestamps[index + 1]
            for symbol in settings.SYMBOLS:
                params['currencyPair'] = 'USDT_' + symbol
                done = False
                while not done:
                    try:
                        r = requests.get(settings.API_URL, params=params, timeout=1)
                        done = True
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(e))
                        time.sleep(7)
                parsed = json.loads(r.text)
                self.stdout.write(
                    self.style.SUCCESS('got %s %s %s status %s len %s' % (
                        symbol,
                        timestamps[index],
                        timestamps[index + 1],
                        r.status_code,
                        len(parsed)
                    ))
                )
                for tick in parsed:
                    tick['symbol'] = symbol
                    ticks.append(tick)
                time.sleep(7)
        return ticks

    def handle(self, *args, **options):
        if options['days']:
            days = int(options['days'][0])
            last_ticks = Tick.objects \
                .filter(date__gte=timezone.now() - timedelta(days=days)) \
                .order_by('date') \
                .values_list('date', flat=True)
        else:
            last_ticks = Tick.objects \
                .filter(date__gte=timezone.now() - timedelta(seconds=2 * settings.Q_STEP)) \
                .order_by('date') \
                .values_list('date', flat=True)

        if not last_ticks:
            raise CommandError('Last update was more than 300sec ago')
        else:
            last_tick = list(last_ticks)[-1]
            last_timestamp = int(last_tick.timestamp())
            if (last_timestamp - settings.Q_START) % settings.Q_STEP:
                raise CommandError('Error in quantization')

        now = int(timezone.now().timestamp())
        to_timestamp = now - (now - settings.Q_START) % settings.Q_STEP
        self.stdout.write(
            self.style.SUCCESS('requesting ticks for %s %s' % (last_timestamp, to_timestamp))
        )
        ticks = self.request_ticks(last_timestamp, to_timestamp)
        ticks = list(filter(lambda x: int(x['date']) != last_timestamp, ticks))
        self.stdout.write(
            self.style.SUCCESS('got %s ticks' % len(ticks))
        )
        for tick in ticks:
            date = timezone.make_aware(
                datetime.fromtimestamp(int(tick['date'])),
                timezone.get_current_timezone()
            )
            tick_obj = Tick(
                date=date,
                symbol=tick['symbol'],
                open=tick['open'],
                high=tick['high'],
                low=tick['low'],
                close=tick['close'],
                volume=tick['volume'],
            )
            tick_obj.save()
        self.stdout.write(
            self.style.SUCCESS('Success updating ticks')
        )
