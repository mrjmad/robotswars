# -*- coding: utf-8 -*-

from django.contrib import admin

from models import (AvailableMaps, Weapon, ArmorPlate, Chassis,
                    Generator, Motor, Gadget, TemplateRobot, TemplateArmy)

admin.site.register(AvailableMaps)
admin.site.register(TemplateArmy)
admin.site.register(Gadget)
admin.site.register(Motor)
admin.site.register(Generator)
admin.site.register(Chassis)
admin.site.register(ArmorPlate)
admin.site.register(Weapon)
admin.site.register(TemplateRobot)
