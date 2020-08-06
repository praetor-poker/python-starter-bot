import hmac
import hashlib
import json

class MessageMaker:

    def __init__(self, player_id, match_id, secret):
        self.player_id = player_id
        self.match_id = match_id
        self.secret = secret

    def make_signature(self, message_component):
        """
        Create the HMAC signature. key is the player's secret key and message varies depending on the message_type

        Args:
            message_component (string):    If we are signing a check_in message, the message_component is the match_id as a string type. 
                                           If we are signing an input_action message, the message_component is the action string. 
        """
        key_bytes= bytes(self.secret , 'utf-8')
        data_bytes = bytes(message_component, 'utf-8')
        return hmac.new(key_bytes, data_bytes , hashlib.sha256).hexdigest()

    def make_checkin_message(self):
        """
        Create the check_in json message to be sent to the game server
        """
        check_in_params = {'message_type':'check_in', 'player_id':self.player_id, 'match_id':self.match_id, 'signature':self.make_signature(f'{self.match_id}')}
        check_in_json = json.dumps(check_in_params)
        return check_in_json

    def make_action_message(self, action):
        """
        Create the input_action json message to be sent to the game server

        Args:
            action (string): The action we will take
        """
        action_params = {'message_type':'input_action', 'player_id':self.player_id, 'match_id':self.match_id, 'action':action, 'signature':self.make_signature(action)}
        action_json = json.dumps(action_params)
        return action_json