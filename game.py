import sys
import random

import pygame

from settings import *
from support import load_image, load_player_icons

pygame.init()
pygame.display.set_caption('CBS marathon game Hearts♥')

background_image = pygame.image.load("images/background.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))


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
            self.image = pygame.transform.scale(self.original_image, (int(CARD_WIDTH * 1.1), int(CARD_HEIGHT * 1.1)))
        else:
            self.image = self.original_image
        rect = self.image.get_rect(topleft=(x, y))
        screen.blit(self.image, rect)


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.image = None

    def play_card(self, trick_suit, leading_suit):
        pass


class Game:
    def __init__(self):
        self.players = [Player(f"Player {i + 1}") for i in range(NUM_PLAYERS)]
        self.deck = self.create_deck()
        self.current_player = 0
        self.leading_suit = None
        self.round_winner = None
        self.round_score = 0
        self.total_scores = [0] * NUM_PLAYERS
        self.round_number = 1
        self.played_cards = []
        self.trick = []

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.draw_players()

    def draw_players(self):
        player_icons = load_player_icons()

        player_icons = [pygame.transform.scale(image, (100, 100)) for image in player_icons]

        for i, image in enumerate(player_icons):
            if i == 0:
                x, y = 0, 0
            elif i == 1:
                x, y = 0, SCREEN_HEIGHT - 100
            elif i == 2:
                x, y = SCREEN_WIDTH - 100, 0
            elif i == 3:
                x, y = SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100

            self.screen.blit(image, (x, y))

    @staticmethod
    def create_deck():
        ranks = [str(i) for i in range(2, 11)] + ["J", "Q", "K", "A"]
        suits = ["♣", "♦", "♠", "♥"]
        deck = [Card(rank, suit) for rank in ranks for suit in suits]
        random.shuffle(deck)
        return deck

    def deal_cards(self):
        for i in range(NUM_PLAYERS):
            self.players[i].hand = self.deck[i * 13: (i + 1) * 13]

        for player in self.players:
            if any(card.rank == '2' and card.suit == '♣' for card in player.hand):
                self.current_player = self.players.index(player)
                break

    def handle_mouse_motion(self, pos):
        for player in self.players:
            for card in player.hand:
                if card.rect.collidepoint(pos):
                    card.hovered = True
                else:
                    card.hovered = False

    def handle_mouse_click(self, pos):
        current_player = self.players[self.current_player]

        for card in current_player.hand:
            if card.rect.collidepoint(pos):
                if current_player != self.leading_player():
                    if card.suit != self.leading_suit and any(
                            c.suit == self.leading_suit for c in current_player.hand):
                        continue

                card_index = current_player.hand.index(card)
                selected_card = current_player.hand.pop(card_index)

                center_x = SCREEN_WIDTH // 2 - CARD_WIDTH // 2
                center_y = SCREEN_HEIGHT // 2 - CARD_HEIGHT // 2
                selected_card.rect.topleft = (center_x, center_y)

                if not self.leading_suit:
                    self.leading_suit = selected_card.suit

                self.trick.append(selected_card)

                if len(self.trick) == NUM_PLAYERS:
                    self.resolve_trick()

                    if all(len(player.hand) == 0 for player in self.players):
                        self.end_round()

                    self.current_player = self.round_winner
                    self.leading_suit = None
                    self.trick = []
                    self.update_screen(self.screen)

                self.current_player = (self.current_player + 1) % NUM_PLAYERS

                current_player.selected_card = selected_card

                self.update_screen(self.screen)

    def leading_player(self):
        return self.players[(self.current_player - len(self.trick)) % NUM_PLAYERS]

    def resolve_trick(self):
        trick_winner = self.determine_trick_winner()
        self.round_winner = trick_winner
        self.total_scores[trick_winner] += self.round_score
        self.played_cards.extend(self.trick)
        self.trick = []
        self.round_score = 0
        self.leading_suit = None

        if all(len(player.hand) == 0 for player in self.players):
            self.end_round()

    def determine_trick_winner(self):
        leading_rank = self.trick[0].rank
        winning_card = max(self.trick, key=lambda card: (card.suit != '♥', card.suit != '♠', card.rank != 'Q♠', card.rank))
        return self.players.index(self.leading_player())

    def end_round(self):
        if any(score >= 100 for score in self.total_scores):
            self.end_game()
        else:
            print(f"End of Round {self.round_number}")
            print("Round Scores:", self.total_scores)
            self.round_number += 1

            self.deck = self.create_deck()
            random.shuffle(self.deck)
            self.deal_cards()
            self.played_cards.clear()

    def end_game(self):
        print("Game Over!")
        print("Total Scores:", self.total_scores)
        pygame.quit()
        sys.exit()

    def update_screen(self, screen):
        screen.blit(background_image, (0, 0))

        x_center = SCREEN_WIDTH // 2
        y_center = SCREEN_HEIGHT // 2
        spacing = 10

        for i, card in enumerate(self.played_cards):
            x = x_center - (len(self.played_cards) * CARD_WIDTH + (len(self.played_cards) - 1) * spacing) // 2 + i * (
                    CARD_WIDTH + spacing)
            y = y_center - CARD_HEIGHT // 2
            rotated_card = pygame.transform.rotate(card.image, 0)
            rect = rotated_card.get_rect(topleft=(x, y))
            card.rect = rect
            card.update()
            card.draw(screen, x, y)

        for player_idx, player in enumerate(self.players):
            num_cards = len(player.hand)
            total_width = num_cards * CARD_WIDTH + (num_cards - 1) * CARD_SPACING
            for card_idx, card in enumerate(player.hand):
                if player_idx == 0:  # 1st Player (top ^)
                    x = card_idx * (CARD_WIDTH + CARD_SPACING) + (SCREEN_WIDTH - total_width) / 2
                    y = CARD_SPACING + SCREEN_MARGIN_Y
                    angularity = 0
                elif player_idx == 1:  # 2nd Player (left hand)
                    x = CARD_SPACING + SCREEN_MARGIN_X
                    y = card_idx // 2 * (CARD_HEIGHT + CARD_SPACING) + (
                            SCREEN_HEIGHT // 2 - total_width / 4 + CARD_SPACING)
                    angularity = 90

                    if card_idx % 2 == 1:
                        x += CARD_WIDTH
                elif player_idx == 2:  # 3d Player (bottom _ )
                    x = card_idx * (CARD_WIDTH + CARD_SPACING) + (SCREEN_WIDTH - total_width) / 2
                    y = SCREEN_HEIGHT - CARD_HEIGHT - CARD_SPACING - SCREEN_MARGIN_Y
                    angularity = 0
                elif player_idx == 3:  # 4th Player (right hand)
                    x = SCREEN_WIDTH - CARD_WIDTH - CARD_SPACING - SCREEN_MARGIN_X
                    y = card_idx // 2 * (CARD_HEIGHT + CARD_SPACING) + (
                            SCREEN_HEIGHT // 4 + CARD_SPACING)
                    angularity = -90

                    if card_idx % 2 == 1:
                        x -= CARD_WIDTH

                rotated_card = pygame.transform.rotate(card.image, angularity)
                rect = rotated_card.get_rect(topleft=(x, y))
                card.rect = rect
                card.update()
                card.draw(screen, x, y)

        for player_idx, player in enumerate(self.players):
            if hasattr(player, 'selected_card') and player.selected_card is not None:
                selected_card = player.selected_card
                x = (SCREEN_WIDTH - CARD_WIDTH) // 2
                y = (SCREEN_HEIGHT - CARD_HEIGHT) // 2
                rotated_card = pygame.transform.rotate(selected_card.image, 0)
                rect = rotated_card.get_rect(topleft=(x, y))
                selected_card.rect = rect
                selected_card.update()
                selected_card.draw(screen, x, y)

    def main_loop(self):
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_motion(event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event.pos)

            self.update_screen(screen)
            pygame.display.flip()
            clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.deal_cards()
    game.main_loop()
