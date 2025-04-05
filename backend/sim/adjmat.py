class AdjacencyMatrix:

    def __init__(self, size=10, symmetrical=False):
        
        self.size = 10
        self.symmetrical = symmetrical

        self.mat = [[None for __ in range(self.size)] for _ in range(self.size)]

    def update(self, id1, id2, val):
        self.mat[id1][id2] = val
        if self.symmetrical:
            self.mat[id2][id1] = val

    def get(self, id1, id2):
        return self.mat[id1][id2]


