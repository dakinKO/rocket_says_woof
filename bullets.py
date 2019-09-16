import pygame as pg
from pygame import Vector2 as vec
LIGHT_GRAY = pg.Color('gray32')


class Bullets(pg.sprite.Sprite):
    def __init__(self, pos, damage):
        super().__init__()
        self.rect = pg.Rect(0, 0, 5, 5)
        self.rect.center = pos
        self.speed = 20
        self.damage = damage
        self.pos = vec()
        self.pos.xy = pos
        self.vel = vec()
        self.vel.xy = 0, 0
        self.target_sprite = None

    def draw(self, surface):
        self.rect.center = (self.pos.x, self.pos.y)
        pg.draw.rect(surface, LIGHT_GRAY, self.rect)

    def update(self):
        self.update_vel()
        self.pos += self.vel
        self.check_collisions()

    def update_vel(self):
        # Update the velocity and position
        target = vec()
        target.xy = self.target_sprite.rect.center
        desired = (target - self.pos)
        desired.normalize_ip()
        desired *= self.speed
        self.vel = desired

    def check_collisions(self):
        if self.rect.colliderect(self.target_sprite.rect):
            self.target_sprite.health -= self.damage
            self.kill()
