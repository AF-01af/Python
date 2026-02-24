import random
def display_msg():
    print("Welcome to Tic-Tac-Toe!")

def display_block(block):
    print(block[1]+' | '+ block[2] +' | '+ block[3])
    print("--+---+--")
    print(block[4]+' | '+ block[5] +' | '+ block[6])
    print("--+---+--")
    print(block[7]+' | '+ block[8] +' | '+ block[9])


def player_input():
    marker=''
    while marker not in ['X','O']:
        marker= input("Player 1 choice your marker X or O: ").upper()
        player1=marker
        if player1=='X':
            player2='O'
        else:
            player2='X'
    return (player1,player2)

def place_marker(block, marker, position):
    block[position] = marker
    


def win_check(block):

    winner_combos=[(1,2,3),(4,5,6),(7,8,9),
                    (1,4,7),(2,5,8),(3,6,9),
                    (1,5,9),(3,5,7)]
    for a,b,c in winner_combos:
        if block[a]!=' ' and block[a]==block[b]==block[c]:
            return block[a]
    return None


def choose_first():
    return random.choice(["Player 1", "Player 2"])
def space_check(block, position):
    return block[position]==' '

def full_board_check(block):
    return ' ' not in block[1:]


def player_choice(block):
    while True:
        next_pos= input("Pick next position where you want to place your marker (1-9):")

        if not next_pos.isdigit():
            print("Invaid input. try again!")
            continue
        next_pos=int(next_pos)
        if next_pos not in range(1,10):
            print("Try between 1-9.")
            continue
        if not space_check(block, next_pos):
            print("Position not available. Try another position")
            continue
        return next_pos

def replay():
    choice=""
    while choice not in ['Y','N']:
        choice= input("Wanna play again? (Y or N): ").upper()
        if choice not in ['Y','N']:
            print("Sorry, invaild choice")

    if choice =="Y": 
        return True 
    else: 
        return False


#______________________Game Loop__________________________________
game_on=True


while True:
    board = ['#',' ',' ',' ',' ',' ',' ',' ',' ',' ']
    display_msg()
    player1_marker,player2_marker=player_input()

    current_player=choose_first()
    print(f"{current_player} will go first!")
    
    current_marker = player1_marker if current_player == "Player 1" else player2_marker

    while game_on:
        display_block(board)
        # Ask current player for position
        print(f"{current_player}'s turn ({current_marker})")
        position=player_choice(board)
        place_marker(board,current_marker,position)

        winner =win_check(board)
        if winner:
            display_block(board)
            print(f"{current_player} is the winner!")
            game_on=False
            continue
        if full_board_check(board):
            display_block(board)
            print("The game is a Tie!")
            game_on=False
            continue
        # Switch players for next turn
        if current_player == "Player 1":
            current_player = "Player 2"
            current_marker = player2_marker
        else:
            current_player = "Player 1"
            current_marker = player1_marker
    if not replay():
        print("Thanks for playing!")
        break


