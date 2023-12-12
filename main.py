import random
import typing
from helpers import *

def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "snakezilla",
        "color": "#36454F",  
        "head": "mlh-gene",  
        "tail": "mlh-gene", 
    }


def start(game_state: typing.Dict):
    print("GAME START")


def end(game_state: typing.Dict):
    print("GAME OVER\n")


def move(game_state: typing.Dict) -> typing.Dict:
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}
    
    my_head = game_state["you"]["body"][0]
    my_neck = game_state["you"]["body"][1]
    my_body = game_state['you']['body']
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    opponents = game_state['board']['snakes']
    
    prevent_backwards_movement(my_head, my_neck, is_move_safe)    
    
    prevent_out_of_bounds(my_head, board_width, board_height, is_move_safe)
    
    prevent_self_collision(my_head, my_body, is_move_safe)
        
    prevent_opp_collision(my_head, opponents, is_move_safe)
    
    prevent_head_to_head(my_head, my_body, opponents, is_move_safe)
    
    safe_moves = get_safe_moves(is_move_safe)
    next_move = ""
    
    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        
        desperate_moves = {"up": True, "down": True, "left": True, "right": True}
        prevent_out_of_bounds(my_head, board_width, board_height, desperate_moves)
        
        next_move = random.choice(get_safe_moves(desperate_moves))
    else:
        next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # next_move_to_food = get_move_to_closest_food(my_head, game_state["board"], safe_moves)
    
    # if next_move_to_food is not None:
    #     next_move = next_move_to_food

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
