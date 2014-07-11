# -*- coding: utf-8 -*-

import os

from django.core.management.base import BaseCommand

from ...models import AvailableMaps
from ...maps_utils import import_map

class Command(BaseCommand):

    def handle(self, maps_dir, *app_labels, **options):
        files_list = os.listdir(maps_dir)
        for file in files_list:
            print u'Import of %s map file' % file
            import_map(os.path.join(maps_dir, file),
                       file.split('.')[0], True)
