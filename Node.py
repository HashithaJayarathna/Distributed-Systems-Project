class Node:
    def __init__(self, x_coord, y_coord, energy):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.energy = energy

    def __repr__(self):
        return f"Node(x={self.x_coord}, y={self.y_coord}, E={self.energy})"