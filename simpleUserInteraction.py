

def game_display (game_list):
    print("Here is the current list")
    print(game_list)

def replace_pos():
    replace=""
    while replace not in ['0','1','2']:
        replace= input("Pick a position to replace (0,1,2): ")
        if replace not in ['0','1','2']:
            print("Sorry, invaild postion")
    return int(replace)

def replacement_choice(game_list,position):
    user_res=input("Type a string to place at position: ")
    game_list[position]= user_res
    return game_list

def game_on_choice():
    choice=""
    while choice not in ['Y','N']:
        choice= input("Wanna go again? (Y or N): ")
        if choice not in ['Y','N']:
            print("Sorry, invaild choice")

    if choice =="Y": 
        return True 
    else: 
        return False




game_on=True
game_list=[0,1,2]
while game_on:
    game_display(game_list)
    position=replace_pos()
    game_list=replacement_choice(game_list,position)
    game_on=game_on_choice()

