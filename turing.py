#ab*ab*a
#(q0, a)-> (q1, a, R)
#(q1, b)-> (q1, b, R)
#(q1, a)-> (q2, a, R)
#(q2, b)-> (q2, b ,R)
#(q2, a)-> (q3, a, R)
#(q3, .)-> (qf, ., L)


class State:
    def __init__(self, label=None):
        self.label = label
        # edge = (ebarat, (next_state, write, direction))
        self.edges = []
        
    def addEdge(self, edge):
        self.edges.append(edge)

class Turing:
    def __init__(self, initial:State, accept:State):
        self.initial = initial
        self.accept = accept

def createTuring():
  q0 = State("q0")
  q1 = State("q1")
  q2 = State("q2")
  q3 = State("q3")
  qf = State("qf")

  q0.addEdge(('a', (q1, 'a', 'R')))
  q1.addEdge(('b', (q1, 'b', 'R')))
  q1.addEdge(('a', (q2, 'a', 'R')))
  q2.addEdge(('b', (q2, 'b', 'R')))
  q2.addEdge(('a', (q3, 'a', 'R')))
  q3.addEdge(('.', (qf, '.', 'L')))

  return Turing(q0, qf)

def check(touring, navar, index):
  initialState = touring.initial
  currentStates = [initialState, ]
  while touring.accept not in currentStates:
    nextStates = []
    for j in currentStates:
      for k in j.edges:
        if k[0] == navar[index]:
          if(k[1][0] not in nextStates):
            nextStates.append(k[1][0])
    if(len(nextStates) == 0):
       return False
    currentStates = nextStates
    index += 1
  return True

print(check(createTuring(), ".aaa.", 1))

