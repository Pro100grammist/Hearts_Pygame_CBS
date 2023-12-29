import sys
import random

import pygame

from settings import *
from support import load_player_icons, load_track
from entities import Card, Player

pygame.init()
pygame.display.set_caption("CBS marathon game Hearts♥")

background_image = pygame.transform.scale(
    pygame.image.load("images/background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)
)


class Game:
    def __init__(self):
        self.players = [
            Player(f"Player {i + 1}", load_player_icons()[i])
            for i in range(NUM_PLAYERS)
        ]
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

        self.load_music()
        self.play_music()

    @staticmethod
    def create_deck():
        ranks = [str(i) for i in range(2, 11)] + ["J", "Q", "K", "A"]
        suits = ["♣", "♦", "♠", "♥"]
        deck = [Card(rank, suit) for rank in ranks for suit in suits]
        random.shuffle(deck)
        return deck

    def deal_cards(self):
        for i in range(NUM_PLAYERS):
            self.players[i].hand = self.deck[i * 13 : (i + 1) * 13]

        for player in self.players:
            if any(card.rank == "2" and card.suit == "♣" for card in player.hand):
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
                        c.suit == self.leading_suit for c in current_player.hand
                    ):
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
        winning_card = max(
            self.trick,
            key=lambda card: (
                card.suit != "♥",
                card.suit != "♠",
                card.rank != "Q♠",
                card.rank,
            ),
        )
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
            x = (x_center - (len(self.played_cards) * CARD_WIDTH + (len(self.played_cards) - 1)
                             * spacing) // 2 + i * (CARD_WIDTH + spacing))
            y = y_center - CARD_HEIGHT // 2
            card.rect = card.image.get_rect(topleft=(x, y))
            card.update()
            card.draw(screen, x, y)

        for idx, player in enumerate(self.players):
            num_cards = len(player.hand)
            total_width = num_cards * CARD_WIDTH + (num_cards - 1) * CARD_SPACING

            for card_idx, card in enumerate(player.hand):
                if idx == 0:  # 1st Player (top ^)
                    x = (card_idx * (CARD_WIDTH + CARD_SPACING) + (SCREEN_WIDTH - total_width) / 2)
                    y = CARD_SPACING + SCREEN_MARGIN_Y

                elif idx == 1:  # 2nd Player (left hand)
                    x = CARD_SPACING + SCREEN_MARGIN_X
                    y = card_idx // 2 * (CARD_HEIGHT + CARD_SPACING) + (SCREEN_HEIGHT // 2 - total_width / 4 + CARD_SPACING)

                    if card_idx % 2 == 1:
                        x += CARD_WIDTH

                elif idx == 2:  # 3d Player (bottom _ )
                    x = (card_idx * (CARD_WIDTH + CARD_SPACING) + (SCREEN_WIDTH - total_width) / 2)
                    y = SCREEN_HEIGHT - CARD_HEIGHT - CARD_SPACING - SCREEN_MARGIN_Y

                elif idx == 3:  # 4th Player (right hand)
                    x = SCREEN_WIDTH - CARD_WIDTH - CARD_SPACING - SCREEN_MARGIN_X
                    y = card_idx // 2 * (CARD_HEIGHT + CARD_SPACING) + (SCREEN_HEIGHT // 4 + CARD_SPACING)

                    if card_idx % 2 == 1:
                        x -= CARD_WIDTH

                card.rect = card.image.get_rect(topleft=(x, y))
                card.update()
                card.draw(screen, x, y)

            if idx == 0:  # 1st Player (top ^)
                x = x_center - player.image.get_width() // 2
                y = CARD_SPACING
            elif idx == 1:  # 2nd Player (left hand)
                x = CARD_SPACING
                y = y_center - player.image.get_height() // 2
            elif idx == 2:  # 3d Player (bottom _ )
                x = x_center - player.image.get_width() // 2
                y = SCREEN_HEIGHT - player.image.get_height() - CARD_SPACING
            elif idx == 3:  # 4th Player (right hand)
                x = SCREEN_WIDTH - player.image.get_width() - CARD_SPACING
                y = y_center - player.image.get_height() // 2

            player.rect = player.image.get_rect(topleft=(x, y))
            player.draw(screen, x, y)

        for player in self.players:
            if hasattr(player, "selected_card") and player.selected_card is not None:
                selected_card = player.selected_card
                x = (SCREEN_WIDTH - CARD_WIDTH) // 2
                y = (SCREEN_HEIGHT - CARD_HEIGHT) // 2
                selected_card.rect = selected_card.image.get_rect(topleft=(x, y))
                selected_card.update()
                selected_card.draw(screen, x, y)

        pygame.display.flip()

    @staticmethod
    def load_music():
        pygame.mixer.music.set_volume(0.5)
        load_track("background_music.mp3")

    @staticmethod
    def play_music():
        pygame.mixer.music.play(-1)

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
