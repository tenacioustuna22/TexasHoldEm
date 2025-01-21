class GameStats():
    """ Track stats for poker trainer """

    def __init__(self):
        # Initial settings, phase of game and card images
        self.phase = 0
        self.hand_count = 0
        self.card_0_val = 'card_back'
        self.card_1_val = 'card_back'
        self.card_2_val = 'card_back'
        self.card_3_val = 'card_back'
        self.card_4_val = 'card_back'
        self.card_5_val = 'card_back'
        self.card_6_val = 'card_back'


    def stats_reset(self):
        # Reset the stats
        # Phase to -1 because the call to this function happens before the += 1
        self.phase = -1
        self.card_0_val = 'card_back'
        self.card_1_val = 'card_back'
        self.card_2_val = 'card_back'
        self.card_3_val = 'card_back'
        self.card_4_val = 'card_back'
        self.card_5_val = 'card_back'
        self.card_6_val = 'card_back'

    def move_forward(self):
        # Update the game phase counter
        self.phase += 1

