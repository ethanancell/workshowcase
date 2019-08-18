import random

# Returns number that occurs from the addition of two
# dice rolls with numbers on the dice up to dice_range
def roll_dice(dice_range):
    die_one = random.randint(1, dice_range)
    die_two = random.randint(1, dice_range)
    return [die_one + die_two, die_one == die_two]

# Returns spot to travel to if it is a movement card,
# if not then it will return -1
def chance(current_position):
    decision = random.randint(1, 16)
    # Advance to GO
    if decision == 1:
        return 0
    # Go to JAIL
    elif decision == 2:
        return 10
    # Go to C1
    elif decision == 3:
        return 11
    # Go to E3
    elif decision == 4:
        return 24
    # Go to H2
    elif decision == 5:
        return 39
    # Go to R1
    elif decision == 6:
        return 5
    # Two cards of go to next railroad. Uses the current_position inputed
    # to tell what the next railroad is.
    elif decision == 7 or decision == 8:
        if current_position >= 35 or current_position < 5:
            return 5
        elif current_position >= 5 and current_position < 15:
            return 15
        elif current_position >= 15 and current_position < 25:
            return 25
        elif current_position >= 25 and current_position < 35:
            return 35
    # Go to next utility company. Uses current_position to find what next
    # utility company location will be.
    elif decision == 9:
        if current_position >= 28 or current_position < 12:
            return 12
        else:
            return 28
    # Go back three squares. If three spaces back brings you before GO, then
    # the number gets wrapped to accomodate that
    elif decision == 10:
        if current_position >= 3:
            return current_position - 3
        else:
            return current_position - 3 + 40
    # Card drawn doesn't imply movement
    else:
        return -1

# Returns a spot to either GO or JAIL, but will return
# -1 if no movement occurs
def community_chest():
    decision = random.randint(1, 16)
    # Advance to GO
    if decision == 1:
        return 0
    # Go to JAIL
    elif decision == 2:
        return 10
    # Insignificant card for movement
    else:
        return -1


# Standard move from the player.
# Returns what place you end up after giving your
# starting position.

player_doubles_in_a_row = 0
def player_move(start_position):
    global player_doubles_in_a_row
    player_roll = roll_dice(4)
    player_movement = player_roll[0]

    # Keep track of doubles and whether they
    # need to go to jail or not
    player_doubles = player_roll[1]
    if player_doubles:
        if player_doubles_in_a_row == 2:
            # go to jail
            player_doubles_in_a_row = 0
            return 10
        else:
            player_doubles_in_a_row += 1
    else:
        player_doubles_in_a_row = 0


    # where does the player end up right after
    # the dice land?
    initial_move = start_position + player_movement
    if initial_move > 39:
        initial_move -= 40

    # Landed on a Community Chest
    if initial_move == 2 or initial_move == 17 or initial_move == 33:
        cc = community_chest()
        if cc != -1:
            return cc

    # Landed on a Chance
    if initial_move == 7 or initial_move == 22 or initial_move == 36:
        c = chance(initial_move)
        if c != -1:
            # We must move to a different place
            return c

    # Landed on Go to Jail
    if initial_move == 30:
        return 10

    # If we make it here, then we haven't landed on any special place and we will
    # simply return where we land after our dice roll.
    return initial_move




# Start with an array of zeroes with each index for each spot landed on.
# Increment by 1 each time we land on a spot.
board = [0] * 40
total_moves = 0

# Repeat one million times for a good chance at statistical significance
current_player_position = 0
for i in range(0, 500000):
    current_player_position = player_move(current_player_position)
    board[current_player_position] += 1
    total_moves += 1

# Dictionary later used to display the numbers found in a nice format
board_dict = {}

# Divide each index by the total number of moves to obtain a percentage of total rolls
# that end in that location
for i in range(0, 40):
    board[i] = (board[i] / total_moves) * 100
    board_dict[i] = board[i]

# Sort and then neatly display the information we found.
board_sorted = sorted(board_dict.items(), reverse=True, key = lambda kv:(kv[1], kv[0]))
print("Most commonly landed upon spots:")
for i in board_sorted:
    print(f"Square: {i[0]}  |  Percentage: {i[1]}%")

# Print modal string required for project euler solution
print("\nThe modal string required by Project Euler will be:")
print(f"{board_sorted[0][0]}{board_sorted[1][0]}{board_sorted[2][0]}")
