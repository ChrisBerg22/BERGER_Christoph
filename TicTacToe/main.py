import tictactoe
import sys
sys.modules["tictactoe"] = tictactoe


from tictactoe import Game
#from tictactoe import load

def main():
    """main:
    Query for names.
    Query for a stats file name. If none is entered, use "stats.json" as a default
    if a TimeoutError occurs, exit the program using sys.exit(0).
    if a EOFError occures, exit the program using sys.exit(0).
    """
    print("Player 1: Alice(X)\nPlayer 2: Bob(O)")
    game = Game()
    game.board.__str__()
    print("Note: Enter q or Q to quit the Game")
    try:
        for i in range(10):
            game.make_move()
    except:
        print("Game Over")
        sys.exit(0)


if __name__ == "__main__":
    main()
