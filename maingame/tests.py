"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.utils.translation import gettext
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from models import (TemplateArmy, Weapon, ArmorPlate, Chassis, Motor,
                    Gadget, Generator, TemplateRobot, AvailableMaps, ArmyClass)

from maps_utils import import_map

import constants
class CreateModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='user1')
        self.army_class = ArmyClass.objects.all()[0]

    def test_create_template_army_01(self):
        army = TemplateArmy(name=u"Test Army", owner=self.user, army_class=self.army_class)
        self.army = army.save()
        self.assertIsInstance(army, TemplateArmy)

    def test_create_template_army_02(self):
        with self.assertRaises(IntegrityError):
            TemplateArmy.objects.create(name=u"Army without owner and class")

    def test_create_template_army_03(self):
        with self.assertRaises(IntegrityError):
            TemplateArmy.objects.create(name=u"Army without owner", army_class=self.army_class)

    def test_create_template_army_04(self):
        with self.assertRaises(IntegrityError):
            TemplateArmy.objects.create(name=u"Army without army_class", owner=self.user)

    def test_create_Weapon(self):
        self.weapon = Weapon(name="Weapon1", price=1, weight=1, structure_points=2,
                        supported_weight=0, power_consumption=3,
                        damage=2, shot_per_turn=1, range=2)

    def test_create_ArmorPlate(self):
        self.armor = ArmorPlate(name="ArmorPlate1", price=1, weight=1, structure_points=2,
                        supported_weight=0, power_consumption=3,
                        armor_value=2)

    def test_create_Generatpr(self):
        self.generator = Generator(name="ArmorPlate1", price=1, weight=1, structure_points=2,
                        supported_weight=0, power_consumption=3,
                        power=2)

    def test_create_Chassis(self):
        self.chassis = Chassis(name="Chassis1", price=1, weight=1, structure_points=2,
                        supported_weight=0, power_consumption=3,
                        weapon_number=2)


    def test_create_Motor(self):
        self.motor = Motor(name="Motor1", price=1, weight=1, structure_points=2,
                        supported_weight=0, power_consumption=3,
                        speed=4)

    def test_create_Gadget(self):
        self.gadget = Gadget(name="Gadget1", price=1, weight=1, structure_points=2,
                        supported_weight=0, power_consumption=3,
                        name_condition_function="function_condition_test")


def build_a_robot(army):
    robot = TemplateRobot()
    robot.army = army
    robot.chassis = Chassis.objects.all()[0]
    robot.motor = Motor.objects.all()[0]
    robot.generator = Generator.objects.all()[0]
    robot.armor = ArmorPlate.objects.all()[0]
    robot.weapon1 = Weapon.objects.all()[0]
    robot.weapon2 = Weapon.objects.all()[2]
    robot.weapon3 = Weapon.objects.all()[1]
    robot.gadget1 = Gadget.objects.all()[0]
    robot.gadget2 = Gadget.objects.all()[0]
    robot.army.save()
    robot.recalculate_all_piece_and_save()
    return robot

def build_a_template_army(user):
    army_class = ArmyClass.objects.all()[0]
    army = TemplateArmy(name=u"Test Army", owner=user, army_class=army_class)
    army.save()
    return army

class BuildRobotTest(TestCase):
    fixtures = ['initial_data.yaml']

    def setUp(self):
        self.user = User.objects.create(username='user1')
        self.army = build_a_template_army(self.user)


    def test_create_Robot(self):
        self.robot = build_a_robot(self.army)
        self.assertEqual(self.robot.price, 25)

    def test_check_not_enougth_power(self):
        self.robot = robot = TemplateRobot()
        robot.army = self.army
        robot.chassis = Chassis.objects.all()[0]
        robot.recalculate_all_piece_and_save()
        motor = Motor.objects.all()[0]
        gene = Generator.objects.all()[0]
        r1, r2 = robot.check_for_add_piece(motor)
        self.assertEqual(r1, False)
        self.assertEqual(gettext(r2), gettext(constants.NOT_ENOUGTH_POWER))

        r11, r12 = robot.check_for_add_piece(gene)
        self.assertEqual(r11, True)
        self.assertEqual(r12, True)

        robot.generator = gene
        robot.recalculate_all_piece_and_save()

        r1, r2 = robot.check_for_add_piece(motor)
        self.assertEqual(r1, True)
        self.assertEqual(r2, True)


    def test_check_too_much_weight(self):
        self.robot = robot = TemplateRobot()
        robot.army = self.army
        robot.chassis = Chassis.objects.all()[0]
        robot.recalculate_all_piece_and_save()
        motor = Motor.objects.all()[1]
        gene = Generator.objects.all()[2]

        r11, r12 = robot.check_for_add_piece(gene)
        self.assertEqual(r11, True)
        self.assertEqual(r12, True)

        robot.generator = gene
        robot.recalculate_all_piece_and_save()

        r1, r2 = robot.check_for_add_piece(motor)
        self.assertEqual(r1, False)
        self.assertEqual(gettext(r2), gettext(constants.TOO_MUCH_WEIGHT))

        robot.chassis = Chassis.objects.all()[2]
        robot.recalculate_all_piece_and_save()


        r11, r12 = robot.check_for_add_piece(motor)
        self.assertEqual(r11, True)
        self.assertEqual(r12, True)


class AvailableMapsTest(TestCase):
    maps_tests = 'test_maps.json'

    def setUp(self):
        from os.path import dirname, join, abspath, exists
        PROJECT_ROOT = dirname(abspath(__file__))
        self.pathname = join(PROJECT_ROOT, 'fixtures', 'maps', self.maps_tests)

    def test_build_map(self):
        map  = import_map(self.pathname, 'test', True)
        self.assertEqual(map.name, 'test')
        self.assertEqual(map.width, 10)


class TemplateArmyTest(TestCase):
    fixtures = ['initial_data.yaml']

    def setUp(self):
        self.user = User.objects.create(username='user1')
        self.army = build_a_template_army(self.user)

    def test_is_army_valid(self):
        robot1 = build_a_robot(self.army)
        self.assertEqual(False, self.army.is_valid_army())
        robot2 = build_a_robot(self.army)
        self.assertEqual(False, self.army.is_valid_army())
        robot3 = build_a_robot(self.army)
        self.assertEqual(True, self.army.is_valid_army())
        robot4 = build_a_robot(self.army)
        self.assertEqual(False, self.army.is_valid_army())
