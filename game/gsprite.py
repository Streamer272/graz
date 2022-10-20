import pygame

from shared.sprite import Sprite

MOVEMENT_SPEED = 2.0


def load_image(path: str, width: int, height: int):
    image = pygame.image.load(f"./game/images/{path}")
    image = pygame.transform.scale(image, (width, height))
    return image


class GSprite(Sprite):
    surface: pygame.Surface
    destroy: bool

    def init_gsprite(self, surface: pygame.Surface, x: int, y: int):
        self.surface = surface
        self.destroy = False
        self.init_sprite(x, y, surface.get_width(), surface.get_height())
        return self

    def show(self):
        pygame.display.get_surface().blit(self.surface, (self.x, self.y))
