class State:
    def __init__(self, label=None):
        self.label = label
        # edge = (ebarat, next_state)
        self.edges = []
    def addEdge(self, edge):
        self.edges.append(edge)

class NFA:
    def __init__(self, initial:State, accept:State):
        self.initial = initial
        self.accept = accept

