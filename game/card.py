# -*- coding: utf-8 -*-
from game.constants import GameConstants

class CreatureCard(object):
    """
    Basic creature card
    """
    def __init__(self, damage=1, health=1):
        self.is_alive = True
        self.health = health
        self.damage = damage
        self.rounds_alive = 0

    def attack(self, target):
        """
        Наносит урон цели, и принимает урон от цели.
        target -  cardObject for attack
        """
        if self.is_alive:
            target.take_damage(self.damage)
            self.take_damage(target.damage)

    def take_damage(self, damage):
        """
        Уменьшает свое здоровье равное количеству урона
        """
        self.health -= damage
        if self.health <= 0:
            self.is_alive = False

    def end_of_turn(self):
        """
        each time round is ended, this function called
        """
        self.rounds_alive += 1

    def die(self):
        """
        call this method to kill this creature
        """
        self.is_alive = False
        self.deathrattle()

    def deathrattle(self):
        """
        called after creature is died. ( is_alive = False )
        """
        pass
