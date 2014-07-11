# -*- coding: utf-8 -*-


from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse

import constants

class ArmyClass(models.Model):
    name = models.CharField(_(u"Army Class Name"), max_length=250)
    max_amount = models.PositiveIntegerField(_(u"Max Amount for army"))
    max_robot_number = models.PositiveIntegerField(_(u"Max Robot's Number"))
    min_robot_number = models.PositiveIntegerField(_(u"Min Robot's Number"))


    class Meta:
        verbose_name = _(u'Army Class')
        verbose_name_plural = _(u'Armies Class')

    def __unicode__(self):
        return u"%s, Points Max : %s" % (self.name, self.max_amount )


class TemplateArmy(models.Model):
    name = models.CharField(_(u"Template Army Name"), max_length=250)
    army_class = models.ForeignKey(ArmyClass, verbose_name=_(u"Army Class"))
    amount = models.PositiveIntegerField(_(u"Amount"), default=0, editable=False)
    #owner = models.ForeignKey(User, verbose_name=_(u"Owner"), editable=False)
    owner = models.ForeignKey(User, verbose_name=_(u"Owner"))
    #finish = models.BooleanField(_(u"Is Finish ?"), default=False, editable=False)
    finish = models.BooleanField(_(u"Is Finish ?"), default=False)

    def is_valid_army(self):
        number = self.templaterobot_set.count()
        if number < self.min_robot_number or number > self.max_robot_number:
            return False
        self.calculate_amount()
        if self.amount > self.army_class.max_amount:
            return False
        return True

    def calculate_amount(self):
        self.amount = sum([robot.price for robot in self.templaterobot_set.all()])
        self.save()
        return self.amount

    def __unicode__(self):
        return u"%s, Class : %s, Amount : %s" % (self.name, self.army_class, self.amount )

    @property
    def number_robots(self):
        return self.templaterobot_set.count()

    def get_absolute_url(self):
        return reverse('army_detail', kwargs={'pk': self.pk})


    class Meta:
        verbose_name = _(u'Template Army')
        verbose_name_plural = _(u'Template Army')



class AbstractPieceOfRobot(models.Model):
    name = models.CharField(_(u"Name"), max_length=250)
    price = models.PositiveIntegerField(_(u"Price"), default=0)
    weight = models.PositiveIntegerField(_(u"Weight"), default=0)
    structure_points = models.PositiveIntegerField(_(u"Structure's Points"), default=0)
    supported_weight = models.PositiveIntegerField(_(u"Supported Weight"), default=0)
    power_consumption = models.PositiveIntegerField(_(u"Power Consumption"), default=0)


    def __unicode__(self):
        return self.name


    class Meta:
        verbose_name = _(u'Piece of Robot')
        verbose_name_plural = _(u'Piece of Robot')
        abstract = True


class Weapon(AbstractPieceOfRobot):
    damage = models.PositiveIntegerField(_(u"Damage"), default=0)
    shot_per_turn = models.PositiveIntegerField(_(u"Shot per turn"), default=0)
    range = models.PositiveIntegerField(_(u"Range"), default=0)

    class Meta:
        verbose_name = _(u'Weapons')
        verbose_name_plural = _(u'Weapons')

class ArmorPlate(AbstractPieceOfRobot):
    armor_value = models.PositiveIntegerField(_(u"Armor Value"), default=0)

    class Meta:
        verbose_name = _(u'Armor Plate')
        verbose_name_plural = _(u'Armor Plate')

class Chassis(AbstractPieceOfRobot):
    weapon_number = models.PositiveIntegerField(_(u"Number of Weapons"), default=0)

    class Meta:
        verbose_name = _(u'Chassis')
        verbose_name_plural = _(u'Chassis')

class Generator(AbstractPieceOfRobot):
    power = models.PositiveIntegerField(_(u"Power"), default=0)

    class Meta:
        verbose_name = _(u'Generator')
        verbose_name_plural = _(u'Generators')


class Motor(AbstractPieceOfRobot):
    speed = models.PositiveIntegerField(_(u"Speed"), default=0)

    class Meta:
        verbose_name = _(u'Motor')
        verbose_name_plural = _(u'Motors')

class Gadget(AbstractPieceOfRobot):
    name_condition_function = models.CharField(_(u"Name condition fonction"), max_length=250)

    class Meta:
        verbose_name = _(u'Gadget')
        verbose_name_plural = _(u'Gadgets')

LIST_NAME_ROBOT_ATTRIBUT = ['chassis', 'motor', 'generator', 'armor',
                            'weapon1', 'weapon2', 'weapon3',
                            'gadget1', 'gadget2']

class TemplateRobot(AbstractPieceOfRobot):
    army = models.ForeignKey(TemplateArmy, verbose_name=_(u"his Template Army"))

    chassis = models.ForeignKey(Chassis, verbose_name=_(u"Chassis"), null=True, blank=True)
    motor = models.ForeignKey(Motor, verbose_name=_(u"Motor"), null=True, blank=True)
    generator = models.ForeignKey(Generator, verbose_name=_(u"Generator"), null=True, blank=True)

    armor = models.ForeignKey(ArmorPlate, verbose_name=_(u"Armor plate"),
                              blank=True, null=True)

    weapon1 = models.ForeignKey(Weapon, verbose_name=_(u"First Weapon"), related_name=u"robot_weapons1_set",
                                blank=True, null=True)
    weapon2 = models.ForeignKey(Weapon, verbose_name=_(u"Second Weapon"), related_name=u"robot_weapons2_set",
                                blank=True, null=True)
    weapon3 = models.ForeignKey(Weapon, verbose_name=_(u"Third Weapon"), related_name=u"robot_weapons3_set",
                                blank=True, null=True)
    gadget1 = models.ForeignKey(Gadget, verbose_name=_(u"First Gadget"), related_name=_(u"robot_gadget1_set"),
                                blank=True, null=True)
    gadget2 = models.ForeignKey(Gadget, verbose_name=_(u"Second Gadget"), related_name=_(u"robot_gadget2_set"),
                                blank=True, null=True)

    power = models.PositiveIntegerField(_(u"Power"), default=0)
    speed = models.PositiveIntegerField(_(u"Speed"), default=0)
    armor_value = models.PositiveIntegerField(_(u"Armor"), default=0)

    def check_for_add_piece(self, piece):
        if self.weight + piece.weight > self.supported_weight:
            return (False, constants.TOO_MUCH_WEIGHT )
        if self.power_consumption + piece.power_consumption > self.power:
            return (False, constants.NOT_ENOUGTH_POWER )
        return (True, True)

    def recalculate_value_with_new_piece_no_save(self, piece):
        self.weight += piece.weight
        self.power_consumption += piece.power_consumption
        self.structure_points += piece.structure_points
        self.price += piece.price

        self.supported_weight += getattr(piece, "supported_weight", 0)
        self.power += getattr(piece, "power", 0)
        self.speed += getattr(piece, "speed", 0)
        self.armor_value += getattr(piece, "armor_value", 0)

    def recalculate_value_with_new_piece_and_save(self, piece):
        self.recalculate_value_with_new_piece_no_save(piece)
        self.save()

    def recalculate_all_piece_no_save(self):
        self.power = 0
        self.weight = 0
        self.supported_weight = 0
        self.armor_value = 0
        self.price = 0
        self.power_consumption = 0
        self.structure_points = 0
        self.speed = 0
        for piece in LIST_NAME_ROBOT_ATTRIBUT:
            try:
                real_piece = getattr(self, piece)
            except ObjectDoesNotExist:
                real_piece = None
            if real_piece:
                self.recalculate_value_with_new_piece_no_save(real_piece)

    def recalculate_all_piece_and_save(self):
        self.power = 0
        self.weight = 0
        self.supported_weight = 0
        self.armor_value = 0
        self.price = 0
        self.power_consumption = 0
        self.structure_points = 0
        self.speed = 0
        for piece in LIST_NAME_ROBOT_ATTRIBUT:
            try:
                real_piece = getattr(self, piece)
            except ObjectDoesNotExist:
                real_piece = None
            if real_piece:
                self.recalculate_value_with_new_piece_no_save(real_piece)
        self.save()



    class Meta:
        verbose_name = _(u'Robot')
        verbose_name_plural = _(u'Robots')


class AvailableMaps(models.Model):
    name = models.CharField(_(u"Name"), max_length=250)
    author = models.CharField(_(u"Author's Name"), max_length=250, blank=True, null=True)
    map_file = models.FileField(_(u"Map's file"), max_length=500, upload_to='upload/maps', null=True, blank=True)
    sprite_file = models.CharField(_(u"Name of Sprite file"), max_length=500)
    tile_size = models.PositiveIntegerField(_(u"Height"))
    height = models.PositiveIntegerField(_(u"Height"))
    width = models.PositiveIntegerField(_(u"Width"))
    data  = models.TextField(_(u"Data"))


    real_map = []


    def get_absolute_url(self):
        return reverse('available_map_detail', kwargs={'id': self.id})

    def __unicode__(self):
        return u"%s" % self.name

