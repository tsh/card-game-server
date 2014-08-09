import unittest

from game.card import CreatureCard

class TestCreatureCard(unittest.TestCase):

    def setUp(self):
        self.c_d10_h20 = CreatureCard(10,20)
        self.c_d5_h30 = CreatureCard(5, 30)

    def test_creature_damage_other(self):
        c1 = CreatureCard(10, 20)
        c2 = CreatureCard(10, 20)
        c1.attack(c2)
        self.assertEqual(c2.health,10)

    def test_creature_when_damage_other_damage_self(self):
        self.c_d10_h20.attack(self.c_d5_h30)
        self.assertEqual(self.c_d10_h20.health, 15)


    def test_creature_can_die_from_damage(self):
        c1 = CreatureCard(10, 10)
        c1.take_damage(20)
        self.assertFalse(c1.is_alive)



