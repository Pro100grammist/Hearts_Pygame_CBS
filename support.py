import os
import pygame

from settings import IMAGE_DIRECTORY, PLAYER_ICONS_DIR, SOUND_DIRECTORY, CARD_HEIGHT, CARD_WIDTH
from data import CARDS, PLAYER_ICONS


def load_image(self):
    image_path = os.path.join(IMAGE_DIRECTORY, CARDS.get((self.rank, self.suit), "card_empty.png"))
    image = pygame.image.load(image_path)
    return pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))


def load_player_icons():
    player_images = []
    for icon in PLAYER_ICONS.values():
        image_path = os.path.join(PLAYER_ICONS_DIR, icon)
        image = pygame.image.load(image_path)
        player_images.append(image)
    return player_images


def load_track(track):
    track_path = os.path.join(SOUND_DIRECTORY, track)
    pygame.mixer.music.load(track_path)
