import argparse
from game_of_life.gui import GUI
from game_of_life.game import GameOfLife

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Game of Life')
    parser.add_argument('--width', type=int, default=640, help='Width of the screen')
    parser.add_argument('--height', type=int, default=480, help='Height of the screen')
    parser.add_argument('--cell-size', type=int, default=10, help='Size of the cell')
    parser.add_argument('--speed', type=int, default=10, help='Speed of the game')
    args = parser.parse_args()

    rows = args.height // args.cell_size
    cols = args.width // args.cell_size

    life = GameOfLife((rows, cols))
    ui = GUI(life, cell_size=args.cell_size, speed=args.speed)
    ui.run()
