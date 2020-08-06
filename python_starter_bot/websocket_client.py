import asyncio
import websockets
import json
import sys
import random
import treys
import logging

evaluator = treys.Evaluator()

class WebsocketClient():

    def __init__(self, message_maker, hand_state):
        self.message_maker = message_maker
        self.hand_state = hand_state
        self.game_logger = logging.getLogger(__name__)
        self.hand_count = 0

    async def connect(self, uri):
        '''
        Connect to a websocket server 

        Args:
            uri (string) : the uri address for the websocket server 
        '''
        self.connection = await websockets.client.connect(uri, ping_interval=None, ping_timeout=None)
        if self.connection.open:
            self.game_logger.info(f'Established connection with game server')
            
            # Send match checkin
            await self.sendMessage(self.message_maker.make_checkin_message())
            return self.connection


    async def sendMessage(self, message):
        '''
        Send a message to webSocket server

        Args:
            message (string) : a json-serializable string that will be sent to the game server
        '''
        
        await self.connection.send(message)
        self.game_logger.info(f'Sent message {message}')
        


    async def receiveMessage(self, connection):
        '''
        Receiving and handle messages on this connection

        Args: 
            connection (websockets.connection object) : The connection object through which this bot communicates with the game server
        '''
        while True:
            try:
                message = await connection.recv()
                self.parse_message(message)
            except websockets.exceptions.ConnectionClosed:
                print('Connection with server closed')
                break


    def parse_message(self, incoming_message):
        """
        Digest a message received from the game server and respond appropriately

        Args:
            incoming_message (string) : A json-serializable string message received from the game server
        """

        self.game_logger.info(f'Received message {incoming_message}')
        try:
            incoming_message_json = json.loads(incoming_message)
        
        except json.decoder.JSONDecodeError:
            print(incoming_message)
            sys.exit(1)
            return
         
        message_type = incoming_message_json["message_type"]


        
        if message_type == 'checkin_confirmation':
            # We sent the checkin message when we opened the websocket connection
            pass
        

        elif message_type == 'initial_game_state':
            pass

        elif message_type == 'new_hand':
            # Update our hand state object with information from the new_hand message
            self.hand_count += 1
            if self.hand_count % 50 == 0:
                print(f'played {self.hand_count} hands')
                
            self.hand_state.update_state_from_new_hand(incoming_message_json)

        elif message_type == 'next_to_act':
            # Our turn to act. This starter bot's decisions only take into account the current hand state.
            # However, your decision logic can (and should) be more complex!
            if self.hand_state.current_stage == 'preflop':
                self.make_preflop_decision()
            elif self.hand_state.current_stage in ['flop', 'turn', 'river']:
                my_current_round_bet = incoming_message_json["current_round_bet"]
                self.make_postflop_decision(my_current_round_bet)


        elif message_type == 'effective_action':
            self.hand_state.update_state_from_action(incoming_message_json)


        elif message_type == 'stage':
            self.hand_state.update_state_from_stage(incoming_message_json)

        elif message_type == 'end_hand':
            self.hand_state.update_state_from_end_hand(incoming_message_json)

        elif message_type == 'end_match':
            pass

        else:
            pass
            


    def make_preflop_decision(self):
        """
        Make a decision for preflop actions based on the output of the get_hole_card_strength() method

        If our hole card strength is 2, we always call.
        If our hole card strength is 1, we call 75% of the time and fold 25% of the time .
        If our hole card strength is 0, we always fold.
        """
        strength_val = self.hand_state.get_hole_card_strength()


        if strength_val == 2:
            action = 'call'
        elif strength_val == 1:
            random_choice = random.random()
            if random_choice < 0.75: 
                action = 'call'
            else:
                action = 'fold'

        else:
            action = 'fold'

        
        asyncio.ensure_future(self.sendMessage(self.message_maker.make_action_message(action)))


    def make_postflop_decision(self, current_round_bet):
        """
        Make a decision for postflop actions

        Here we use similar decision-making as our preflop decision function, except now we are using the treys library to determine hand strength.
        According to the treys lookup table, the maximum integer hand rank for a pair is 6185. So if our hand score is at most that value,
        then we have at least one pair. 

        If we have at least a pair then we will usually call, however if action arrives to us and nobody has bet yet then we will sometimes make a 10-chip bet.

        Args:
            current_round_bet (int) : The amount of chips we have already bet during the current round
        """

        postflop_hand_strength = self.hand_state.get_hand_strength()
        random_choice = random.random()
        action = 'call'
        
        if current_round_bet == 0:
            if postflop_hand_strength <= 6185 and random_choice < 0.5:
                action = 'bet_10'

        asyncio.ensure_future(self.sendMessage(self.message_maker.make_action_message(action)))

  