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

def createNFA(reg):
  ebaratha = []
  i=0
  while i < len(reg):
    ebarat = []

    if reg[i] == '(':
      flag = 1
      ebarat.append(reg[i])
      while flag != 0:
        i+=1
        ebarat.append(reg[i])
        if(reg[i] == ')'):
          flag -= 1
        if(reg[i] == '('):
          flag += 1
      i+=1
      if reg[i] == '*':
        ebarat.append(reg[i])
      ebaratha.append(''.join(ebarat))
      i+=1
      continue

    if i + 1 < len(reg) and reg[i+1]=='*':
      ebaratha.append(''.join([reg[i], '*']))
      i+=2
      continue

    ebaratha.append(reg[i])
    i+=1
  
  print("ebaratha: ", ebaratha)

###############################################################################
  allStates = []
  i=0
  initialState = State("init")
  acceptState = State("accept")
  nfa = NFA(initialState, acceptState)
  allStates.append(initialState)
  currentState = initialState
  while i < len(ebaratha):
    if(ebaratha[i] == '+'):
      currentState.addEdge(('.', acceptState))
      tempState = State(currentState.label + '+')
      allStates.append(tempState)
      initialState.addEdge(('.', tempState))
      nextState = tempState
    else:
      nextState = State(ebaratha[i])
      allStates.append(nextState)
      if(ebaratha[i][-1] == '*'):
        currentState.addEdge(('.', nextState))
        currentState.addEdge((ebaratha[i][0], currentState))
      else:
        currentState.addEdge((ebaratha[i][0], nextState))

    currentState = nextState
    i+=1

  currentState.addEdge(('.', acceptState))
  allStates.append(acceptState)
  for i in allStates:
    print("\n\nname : ", i.label, " edges : ", [(j[0], j[1].label) for j in i.edges])
  return nfa

# print(createNFA("(a+b)*c*+(bc*)*a+b"))
nfa = createNFA("a*+b*")

