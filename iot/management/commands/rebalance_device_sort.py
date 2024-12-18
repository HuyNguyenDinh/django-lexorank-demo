from django_lexorank.management.commands.base_rebalance import Command as BaseCommand
from iot.models import DeviceSort


class Command(BaseCommand):
    model = DeviceSort