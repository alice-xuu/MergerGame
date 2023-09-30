import pygame


class ScoreHandler:
    def __init__(self):
        self.score = 0
        self.gameover = False

    def update_score(self, score_increase):
        # Increase the score based on the scoring event
        self.score += score_increase

    def update_gameover(self):
        self.gameover = True

    def get_score(self):
        return self.score