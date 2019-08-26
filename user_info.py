import pygame as pg


class UserInfo:
    def __init__(self, waves, lives, coins):
        self.waves = waves
        self.lives = lives
        self.coins = coins
        self.wave = 0

    def next_wave(self):
        if self.wave + 1 <= self.waves:
            self.wave += 1
            return True
        return False
