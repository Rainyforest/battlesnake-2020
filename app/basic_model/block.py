from basic_model.occupant import Occupant
from basic_model.direction import Direction


class Block:
    def __init__(self,occupant):
        self.occupant = occupant
        self.id = -1  # If occupied by snake, store index of snake

    def __str__(self):
        return str(self.occupant.value)

    def place(self, occupant):
        if self.occupant != Occupant.Empty:
            print("Some problem, have to replace existing occupant")
        self.occupant = occupant

    def empty(self):
        self.occupant = Occupant.Empty
        self.id = -1

    def set_dir(self,d):
        self.direction = d

    def set_id(self,id):
        self.id = id

    def set(self,occupant,id):
        self.occupant = occupant
        self.id = id
