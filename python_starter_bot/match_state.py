import json

class MatchState:

    def __init__(self, match_key, my_player_id, my_username):
        self.match_key = match_key
        self.my_player_id = my_player_id
        self.my_username = my_username
        self.my_chips = 0
        self.opponent_chips = 0
        self.is_running = True
        

    def initialze_state(self, initial_state_message):

        """
        Initialize match state with instance-specific parameters given by the initial_game_state message

        Args: 
            initial_state_message (json) : initial_game_state message sent by the game server
        """

        self.big_blind = initial_state_message["blind_amounts"]["big"]
        self.small_blind = initial_state_message["blind_amounts"]["small"]
        
        self.my_chips = initial_state_message["starting_stack"]
        self.opponent_chips = initial_state_message["starting_stack"]

        self.player_1_name = initial_state_message["player_names"]["player_1"]
        self.player_2_name = initial_state_message["player_names"]["player_2"]