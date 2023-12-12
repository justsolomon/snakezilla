from collections import deque

def prevent_backwards_movement(head, neck, is_move_safe): 
    if neck["x"] < head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif neck["x"] > head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif neck["y"] < head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif neck["y"] > head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False
                
def prevent_out_of_bounds(head, board_width, board_height, is_move_safe):
    if head["x"] == 0:
        is_move_safe["left"] = False
    if head["x"] == board_width - 1:
        is_move_safe["right"] = False
    if head["y"] == 0:
        is_move_safe["down"] = False
    if head["y"] == board_height - 1:
        is_move_safe["up"] = False
                
def prevent_self_collision(head, body, is_move_safe):
    for coord in body:
        if coord["x"] == head["x"] - 1 and coord["y"] == head["y"]:
            is_move_safe["left"] = False
        if coord["x"] == head["x"] + 1 and coord["y"] == head["y"]:
            is_move_safe["right"] = False
        if coord["x"] == head["x"] and coord["y"] == head["y"] - 1:
            is_move_safe["down"] = False
        if coord["x"] == head["x"] and coord["y"] == head["y"] + 1:
            is_move_safe["up"] = False
                     
def prevent_opp_collision(head, opps, is_move_safe):
    for opp in opps:
        for coord in opp["body"]:
            if coord["x"] == head["x"] - 1 and coord["y"] == head["y"]:
                is_move_safe["left"] = False
            if coord["x"] == head["x"] + 1 and coord["y"] == head["y"]:
                is_move_safe["right"] = False
            if coord["x"] == head["x"] and coord["y"] == head["y"] - 1:
                is_move_safe["down"] = False
            if coord["x"] == head["x"] and coord["y"] == head["y"] + 1:
                is_move_safe["up"] = False
                       
def prevent_head_to_head(head, body, opps, is_move_safe):
    for opp in opps:
        if len(opp["body"]) > len(body):
            opp_head = opp["body"][0]
            if opp_head["x"] == head["x"] - 1 and opp_head["y"] == head["y"]:
                is_move_safe["left"] = False
            if opp_head["x"] == head["x"] + 1 and opp_head["y"] == head["y"]:
                is_move_safe["right"] = False
            if opp_head["x"] == head["x"] and opp_head["y"] == head["y"] - 1:
                is_move_safe["down"] = False
            if opp_head["x"] == head["x"] and opp_head["y"] == head["y"] + 1:
                is_move_safe["up"] = False
                                     
def get_safe_moves(is_move_safe):
    safe_moves = []
    
    for move, is_safe in is_move_safe.items():
        if is_safe:
            safe_moves.append(move)
            
    return safe_moves

def is_valid_move(r, c, rows, cols, filled_cells, visited):
    return 0 <= r < rows and 0 <= c < cols and not (r, c) not in filled_cells and not (r, c) not in visited

def get_direction(prev, curr):
    # inverse since y is rows and x is cols
    x1, y1 = prev
    x2, y2 = curr
    if x1 < x2:
        return 'up'
    elif x1 > x2:
        return 'down'
    elif y1 < y2:
        return 'left'
    elif y1 > y2:
        return 'right'

def get_filled_cells(board):
    filled_cells = set()
    
    for hazard in board["hazards"]:
        filled_cells.add((hazard["y"], hazard["x"]))
    
    for snake in board["snakes"]:
        for coord in snake["body"]:
            filled_cells.add((coord["y"], coord["x"]))
    
    return filled_cells

def bfs_shortest_path(start, end, board):
    visited = set()
    filled_cells = get_filled_cells(board)

    queue = deque([(start[0], start[1], 0, None)])  # (x, y, distance, direction)
    visited.add(start)

    while queue:
        r, c, distance, prev_direction = queue.popleft()

        # check if the current position is the destination
        if (r, c) == end:
            return distance, prev_direction

        # explore all valid neighbors
        neighbors = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
        for nr, nc in neighbors:
            if is_valid_move(r, c, board["height"], board["width"], filled_cells, visited):
                direction = get_direction((r, c), (nr, nc))
                queue.append((nr, nc, distance + 1, direction))
                visited.add((nr, nc))

    # if no path is found
    return -1, None

def get_move_to_closest_food(head, board, safe_moves):
    if not board["food"]:
        return None
    
    prev_distance = float("inf")
    move = None
    
    for food in board["food"][0]:
        distance, curr_move = bfs_shortest_path((head["y"], head["x"]), (food["y"], food["x"]), board)
        
        if distance <= prev_distance and curr_move in safe_moves:
            prev_distance = distance
            move = curr_move
                
    return move