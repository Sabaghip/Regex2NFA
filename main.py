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
      if i < len(reg) and reg[i] == '*':
        ebarat.append(reg[i])
      ebaratha.append(''.join(ebarat))
      if i < len(reg) and reg[i] != '*':
        ebaratha.append(reg[i])
      i+=1
      continue

    if i + 1 < len(reg) and reg[i+1]=='*':
      ebaratha.append(''.join([reg[i], '*']))
      i+=2
      continue

    ebaratha.append(reg[i])
    i+=1
  
  queue = [ebaratha, ]
  while len(queue)>0:
    z= queue[0]
    queue.pop(0)
    i=0
    while i < len(z):
      if z[i][0] == '(':
        res = []
        #TODO
        j=0
        x = z[i][1:]
        while j < len(x):
          ebarat = []
          if x[j] == ')':
            j+=1
            continue
    
          if x[j] == '(':
            flag = 1
            ebarat.append(x[j])
            while flag != 0:
              j+=1
              ebarat.append(x[j])
              if(x[j] == ')'):
                flag -= 1
              if(x[j] == '('):
                flag += 1
            j+=1
            if j < len(x) and x[j] == '*':
              ebarat.append(x[j])
            res.append(''.join(ebarat))
            j+=1
            continue
        
          if j + 1 < len(x) and x[j+1]=='*':
            res.append(''.join([x[j], '*']))
            j+=2
            continue
        
          res.append(x[j])
          j+=1

        z[i] = res
        queue.append(z[i])
      
      i+=1

  print("ebaratha: ", ebaratha)

###############################################################################
  allStates = []
  initialState = State("init")
  acceptState = State("accept")
  nfa = NFA(initialState, acceptState)
  queue = [(ebaratha, initialState, acceptState), ]
  allStates.append(initialState)
  while(len(queue) > 0):
    z= queue[0]
    queue.pop(0)
    initialState = z[1]
    acceptState = z[2]
    currentState = initialState
    i=0
    while i < len(z[0]):
      if isinstance(z[0][i], str):
        print(z[0][i])
        if(z[0][i] == '+'):
          currentState.addEdge(('.', acceptState))
          tempState = State(currentState.label + '+')
          allStates.append(tempState)
          initialState.addEdge(('.', tempState))
          nextState = tempState
        else:
          nextState = State(z[0][i])
          allStates.append(nextState)
          if(z[0][i][-1] == '*'):
            currentState.addEdge(('.', nextState))
            currentState.addEdge((z[0][i][0], currentState))
          else:
            currentState.addEdge((z[0][i][0], nextState))
        currentState = nextState
        i+=1
      else:
        startState = State("parantez start")
        finishState = State("parantez end")
        allStates.append(finishState)
        allStates.append(startState)
        currentState.addEdge(('.', startState))
        if(z[0][i][-1] == '*'):
          startState.addEdge(('.', finishState))
          finishState.addEdge(('.', startState))
          z[0][i].pop(-1)
        print(z[0][i])
        queue.append((z[0][i], startState, finishState))
        i+=1
        currentState = finishState

    currentState.addEdge(('.', acceptState))
    allStates.append(acceptState)
  for i in allStates:
    print("\n\nname : ", i.label, " edges : ", [(j[0], j[1].label) for j in i.edges])
  return nfa

###############################################################################


def check(nfa:NFA, text):
  initialState = nfa.initial
  currentStates = [initialState, ]
  for z in currentStates:
    for k in z.edges:
      if k[0] == '.':
        if(k[1] not in currentStates):
          currentStates.append(k[1])
  nextStates = []
  for i in text:
    nextStates = []
    for j in currentStates:
      for k in j.edges:
        if k[0] == i:
          if(k[1] not in nextStates):
            nextStates.append(k[1])

      for m in nextStates:
        for k in m.edges:
          if k[0]=='.':
            if(k[1] not in nextStates):
              nextStates.append(k[1])
    currentStates = nextStates
  for j in nextStates:
    if(j == nfa.accept):
      return True
  return False

nfa = createNFA("bc*(ab)*aab*")
# nfa = createNFA("(a+b)*a")

print(check(nfa,"abab")) #False
print(check(nfa,"aab")) #False
print(check(nfa,"baa")) #True
print(check(nfa,"bcccababaa")) #True
