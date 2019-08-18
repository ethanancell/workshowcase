import random

# Returns number that occurs from the addition of two
# dice rolls with numbers on the dice up to dice_range
def roll_dice(dice_range):
    die_one = random.randint(1, dice_range)
    die_two = random.randint(1, dice_range)
    return [die_one + die_two, die_one == die_two]

# Returns spot to travel to if it is a movement card,
# if not then it will return 666
def chance(current_position):
    decision = random.randint(1, 16)
    if decision == 1:
        return 0
    elif decision == 2:
        return 10
    elif decision == 3:
        return 11
    elif decision == 4:
        return 24
    elif decision == 5:
        return 39
    elif decision == 6:
        return 5
    elif decision == 7 or decision == 8:
        # Next railroad
        if current_position >= 35 or current_position < 5:
            return 5
        elif current_position >= 5 and current_position < 15:
            return 15
        elif current_position >= 15 and current_position < 25:
            return 25
        elif current_position >= 25 and current_position < 35:
            return 35
    elif decision == 9:
        # Next utility
        if current_position >= 28 or current_position < 12:
            return 12
        else:
            return 28
    elif decision == 10:
        if current_position >= 3:
            return current_position - 3
        else:
            return current_position - 3 + 40
    else:
        return 666

# Returns a spot to either GO or JAIL, but will return
# 666 if no movement occurs
def community_chest():
    decision = random.randint(1, 16)
    if decision == 1:
        return 0
    elif decision == 2:
        return 10
    else:
        return 666


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

    # Community chest possibilities
    if initial_move == 2 or initial_move == 17 or initial_move == 33:
        cc = community_chest()
        if cc != 666:
            return cc

    # Chance spot possibilities
    if initial_move == 7 or initial_move == 22 or initial_move == 36:
        c = chance(initial_move)
        if c != 666:
            # We must move to a different place
            return c

    # Possibility you land on GO TO JAIL
    if initial_move == 30:
        return 10

    # If we have made it this far, then we will just
    # return the initial_move
    return initial_move




# For the core part of the program, we will want
# to repeat a ton of times and then keep adding to the original
# board array at the top at the number of times visiting
# each spot, and then finally we will figure out
# the percentages
board = [0] * 40
board_percentages = []
board_sorted = []

total_moves = 0

current_player_position = 0
for i in range(1, 1000000):
    current_player_position = player_move(current_player_position)
    board[current_player_position] += 1
    total_moves += 1

# Now do the stats
for i in range(0, 40):
    board_percentages.append((board[i] / total_moves) * 100)

# Print out the board percentages
for i, content in enumerate(board_percentages):
    print(f"Space: {i}  |   Percentage: {content}")
