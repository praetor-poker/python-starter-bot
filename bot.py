import argparse
import asyncio
import logging 

from python_starter_bot import WebsocketClient, MessageMaker, MatchState, HandState


def main():

    parser = argparse.ArgumentParser(description='Run a bot player for a Praetor Poker match')
    parser.add_argument('match_id',  type=int, help='Match ID for the match that the bot will participate in')
    args = parser.parse_args()


    logging.basicConfig(filename='game_log.log', level=logging.INFO)
    my_logger = logging.getLogger("main")
    
    # These parameters are hardcoded because they will remain constant across all matches
    # Substitute the placeholder values below with your actual information
    

    my_player_id = 0 
    my_public_username = '<MY USERNAME>'
    my_secret_string = '<MY HMAC SECRET>' 


    my_match_id = args.match_id
    my_match = MatchState(my_player_id, my_match_id, my_public_username)

    # Create hand state object
    my_hand_state = HandState()

    # Create message maker object
    my_message_maker = MessageMaker(my_player_id, my_match_id, my_secret_string)

    # Create and run websocket client
    my_websocket_client = WebsocketClient(my_message_maker, my_hand_state)
    loop = asyncio.get_event_loop()
    connection = loop.run_until_complete(my_websocket_client.connect('wss://praetorpoker.com/gameserver'))
    
    tasks = [
        asyncio.ensure_future(my_websocket_client.receiveMessage(connection))
    ]


    loop.run_until_complete(asyncio.wait(tasks))
    



    

if __name__ == '__main__':
    main()