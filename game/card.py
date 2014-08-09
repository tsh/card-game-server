# -*- coding: utf-8 -*-
from game.constants import GameConstants


class CreatureCard(object):

    def __init__(self, damage=1, health=1):
        self.is_alive = True
        self.health = health
        self.damage = damage

    def attack(self, target):
        """Наносит урон цели, и принимает урон от цели.
        """
        if self.is_alive:
            target.take_damage(self.damage)
            self.take_damage(target.damage)

    def take_damage(self, damage):
        """Уменьшает свое здоровье равное количеству урона
        """
        self.health -= damage
        if self.health <= 0:
            self.is_alive = False
