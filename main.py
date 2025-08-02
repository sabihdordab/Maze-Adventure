import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game.game import Game

def main():
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    except Exception as e:
        print("Error running game")
        # import traceback
        # traceback.print_exc()
    finally:
        print("Game ended")

if __name__ == "__main__":
    main()