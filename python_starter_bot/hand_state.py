import json
import treys

class HandState:
    """
    Hand state object to maintain information about the current hand. 

    The purpose of this class is to always keep the current hand's current state. 
    It has no memory of previous hands.

    """
    def __init__(self):
        """
        Initialize a new hand.
        """
        self.board_cards = []
        self.hole_cards_as_treys = []
        self.i_am_big_blind = False
        self.pot_size = 0
        self.current_stage = ''
        self.evaluator = treys.Evaluator()
        


    def update_state_from_new_hand(self, new_hand_message):
        """
        Update hand state with information from a new_hand message
        """
        self.hole_card_string = new_hand_message["hole_cards"]
        self.current_stage = new_hand_message["current_stage"]
        self.hole_cards_as_treys = self.parse_card_string_as_treys(new_hand_message["hole_cards"])


    def update_state_from_action(self, effective_action_message):
        """
        Update hand state with information from an effective_action message
        """
        self.pot_size = effective_action_message["pot_size"]

    def update_state_from_stage(self, stage_message):
        """
        Update hand state with information from a stage message
        """
        self.board_cards += self.parse_card_string_as_treys(stage_message["board_update"])
        self.current_stage = stage_message["current_stage"]

    def update_state_from_end_hand(self, end_hand_message):
        """
        Reset state at the end end of a hand
        """
        self.board_cards = []
        self.pot_size = 0
        self.current_stage = ''
        self.hole_card_string = ''

    def parse_card_string_as_treys(self, card_string):
        """
        Parse a card_string into treys.Card objects 

        Args:
            card_string (string): A string representing cards formatted according to the Praetor card_string type
        """
        return [treys.Card.new(individual_card) for individual_card in card_string.split('_')]
        
    def get_hand_strength(self):
        """
        Use the treys library to evaluate strength of a hand with at least 5 cards
        """
        hand_score = self.evaluator.evaluate(self.hole_cards_as_treys, self.board_cards)
        return hand_score

    def get_hole_card_strength(self):
        """
        Evaluate our hole cards.
        
        For this example, hole cards will be assigned the following integer strength values:
        2: Good
        1: Decent
        0: Bad

        """

        hole_cards_parsed = self.hole_card_string.split('_')
        decent_ranks = ['T', 'J', 'Q', 'K', 'A']

        # Check for a pocket pair. We will designate these hands as "Good"
        if hole_cards_parsed[0][0] == hole_cards_parsed[1][0]:
            return 2

        # Else check that both cards are Ten or better and designate these hands as "Decent"
        elif (hole_cards_parsed[0][0] in decent_ranks) and (hole_cards_parsed[1][0] in decent_ranks):
            return 1

        # All other hole card combinations are designated "Bad"
        else:
            return 0

