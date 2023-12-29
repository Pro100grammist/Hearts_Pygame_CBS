import pygame

from settings import CARD_WIDTH, CARD_HEIGHT
from support import load_image


class Card(pygame.sprite.Sprite):
    def __init__(self, rank, suit):
        super().__init__()
        self.rank = rank
        self.suit = suit
        self.image = load_image(self)
        self.rect = self.image.get_rect()
        self.original_image = self.image
        self.hovered = False

    def draw(self, screen, x, y):
        if self.hovered:
            self.image = pygame.transform.scale(
                self.original_image, (int(CARD_WIDTH * 1.1), int(CARD_HEIGHT * 1.1))
            )
        else:
            self.image = self.original_image
        rect = self.image.get_rect(topleft=(x, y))
        screen.blit(self.image, rect)


class Player:
    def __init__(self, name, image):
        self.name = name
        self.hand = []
        self.image = pygame.transform.scale(image, (100, 100))

    def draw(self, screen, x, y):
        player_icon = pygame.transform.scale(self.image, (100, 100))
        screen.blit(player_icon, (x, y))

    def play_card(self, trick_suit, leading_suit):
        pass
