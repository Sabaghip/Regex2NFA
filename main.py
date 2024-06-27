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

createNFA("(a+b)*c*+(bc*)*a+b")
# nfa = createNFA("a*+b*")

