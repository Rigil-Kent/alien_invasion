class Stats():
    """ Track statistics for Alien Invasion."""

    def __init__(self, settings):
        """ Initialize Statistics"""

        self.settings = settings
        self.game_active = False
        self.high_score = 0
        self.reset_stats_hard()
        self.reset_stats_soft()


    def reset_stats_hard(self):
        """ Initialize statistics that can change during the game."""

        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def reset_stats_soft(self):

        self.score = 0