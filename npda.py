#function for convert context-free grammer to chaomwski normal form
def CFG2CNF(automata = {
     'terminals': [],
     'non_terminals': [],
     'start': '',
     'productions': {
     }
    }):
    # phase1: remove RHS start_state
    flag = False
    for head in automata['productions']:
       for bodies in automata['productions'][head]:
          for body in bodies:
              if body == automata['start']:
                automata['productions']['S0S0'] = [automata['start']]
                automata['start'] = 'S0S0'
                automata['non_terminals'].append("S0S0")
                flag = True
                break
          if flag:
             break
       if flag:
          break
       
    # phase2: remove null

    flag = True
    while flag:
        flag = False
        for head in automata['productions']:
           for body in automata['productions'][head]:
                  if body == '':
                    flag = True
                    automata['productions'][head].remove('')
                    for head2 in automata['productions']:
                       for body2 in automata['productions'][head2]:
                          letterIndex = 0
                          while letterIndex < len(body2):
                            if body2[letterIndex] == head:
                               if body2[0:letterIndex] + body2[letterIndex +1:] not in automata['productions'][head2] and len(body2) > 1:
                                    automata['productions'][head2].append(body2[0:letterIndex] + body2[letterIndex +1:])
                            letterIndex +=1

    # phase3: remove unit
    flag = True
    while flag:
        flag = False
        for head in automata['productions']:
           for body in automata['productions'][head]:
                  if len(body) == 1 and body[0] not in automata['terminals']:
                    flag = True
                    automata['productions'][head].remove(body)
                    if(head != body[0]):
                        for body2 in automata['productions'][body[0]]:
                            automata['productions'][head].append(body2)
    
    i=1
    #phase4: format
    flag = True
    while flag:
        flag = False
        heads = []
        for u in automata['productions']:
           heads.append(u)
        for head in heads:
           for body in automata['productions'][head]:
                  if len(body) > 1:
                    for letterIndex in range(len(body)):
                       if body[letterIndex] in automata['terminals']:
                          if len(body[letterIndex + 1:]) > 0:
                            automata['productions']['X' + str(i)] = [ [r for r in body[:letterIndex + 1]]]
                            i+=1
                            automata['productions']['X' + str(i)] = [ [r for r in body[letterIndex + 1:]]]
                            i+=1
                            automata['productions'][head].append(['X' + str(i - 2), 'X' + str(i - 1)])
                            automata['productions'][head].remove(body)
                            flag = True
                            break
                          else:
                             automata['productions']['X' + str(i)] = [ [r for r in body[:letterIndex]]]
                             i+=1
                             automata['productions']['X' + str(i)] = [ [r for r in body[letterIndex:]]]
                             i+=1
                             automata['productions'][head].append(['X' + str(i - 2), 'X' + str(i - 1)])
                             automata['productions'][head].remove(body)
                             flag = True
                             break

        for head in heads:
           for body in automata['productions'][head]:
                  if len(body) > 2:
                        automata['productions']['X' + str(i)] = [ [r for r in body[:len(body)//2]]]
                        i+=1
                        automata['productions']['X' + str(i)] = [ [r for r in body[len(body)//2:]]]
                        i+=1
                        automata['productions'][head].append(['X' + str(i - 2), 'X' + str(i - 1)])
                        automata['productions'][head].remove(body)
                        flag = True
                        break         

    return automata

#function for convert chaomwski normal form to greybakh normal form
def CNF2GNF(automata):
    newCfg = {
     'terminals': automata['terminals'],
     'non_terminals': [],
     'start': '',
     'productions': {
     }
    }
    
    #phase1: Change vars names
    temp = {}
    i = 1
    for head in automata['productions']:
        if head not in temp:
          newCfg['productions']["A" + str(i)] = []
          temp[head] = "A" + str(i)
          i+=1
          newCfg['non_terminals'].append(temp[head])

        if temp[head] not in newCfg['productions']:
          newCfg['productions'][temp[head]] = []

        if head == automata['start']:
           newCfg['start'] = temp[head]

        for body in automata['productions'][head]:
          newBody = []
          for letter in body:
            if letter not in temp and letter not in newCfg['terminals']:
                temp[letter] = "A" + str(i)
                i+=1
                newCfg['non_terminals'].append(temp[letter])
            if(letter not in newCfg['terminals']):
                newBody.append(temp[letter])
            else:
                newBody.append(letter)
          newCfg['productions'][temp[head]].append(newBody)
    
    #phase2: check Am>An
    flag = True
    while flag:
        flag = False
        heads = []
        for u in newCfg['productions']:
           heads.append(u)
        for head in heads:
           for body in newCfg['productions'][head]:
              if len(body)>0 and len(body[0])>0 and body[0][0] == 'A' and head[0] == 'A':
                 if int(head.split('A')[1]) > int(body[0].split('A')[1]):
                    for q in newCfg['productions'][body[0]]:
                       if(q + body[1:] not in newCfg['productions'][head]):
                          newCfg['productions'][head].append(q + body[1:])
                    newCfg['productions'][head].remove(body)
                    flag=True
                 elif int(head.split('A')[1]) == int(body[0].split('A')[1]):
                    newCfg['productions']['Z'+str(i)] = []
                    newCfg['non_terminals'].append('Z'+str(i))
                    newCfg['productions']['Z'+str(i)].append(body[1:])
                    newCfg['productions']['Z'+str(i)].append(body[1:] + ['Z'+str(i)])
                    newCfg['productions'][head].remove(body)
                    zzz = len(newCfg['productions'][head])
                    for q in range(zzz):
                       if(newCfg['productions'][head][q] + ['Z'+str(i)] not in newCfg['productions'][head]):
                          newCfg['productions'][head].append(newCfg['productions'][head][q] + ['Z'+str(i)])
                    i+=1
                    flag=True

    #phase3
    flag = True
    while flag:
        flag = False
        heads = []
        for u in newCfg['productions']:
           heads.append(u)
        for head in heads:
           for body in newCfg['productions'][head]:
              if len(body)>0 and body[0] not in newCfg['terminals']:
                for q in range(len(newCfg['productions'][body[0]])):
                    newCfg['productions'][head].append(newCfg['productions'][body[0]][q] + body[1:])
                newCfg['productions'][head].remove(body)
                flag = True

    return newCfg

# class for save configs and models
class NPDA:
    def __init__(self, cfg):
        self.cfg = cfg
        self.states = set()
        self.transitions = []
        self.start_state = 'q0'
        self.accept_state = 'q_accept'
        self.stack_start_symbol = 'Z'
        self.automata = self._convert()
    
    def _convert(self):
        self.cfg = CFG2CNF(self.cfg)
        self.cfg = CNF2GNF(self.cfg)

        # # Add initial transition to push start symbol onto the stack
        self.transitions.append((self.start_state, '', self.stack_start_symbol, 'q1', [self.cfg['start'], self.stack_start_symbol]))
        self.states.update([self.start_state, 'q1', self.accept_state])

        for head, bodies in self.cfg['productions'].items():
            for body in bodies:
                self.transitions.append(('q1', body[0], head, 'q1', body[1:]))
        self.transitions.append(('q1', '', self.stack_start_symbol, self.accept_state, []))

        
        return {
            'states': self.states,
            'transitions': self.transitions,
            'start_state': self.start_state,
            'accept_state': self.accept_state,
            'stack_start_symbol': self.stack_start_symbol
        }
    
    def check(self, text:str):
        initialState = self.start_state
        currentStates = [(initialState, [self.stack_start_symbol, ]), ]
        for z in currentStates:
          for k in self.transitions:
            if k[0] == z[0] and k[1] == '' and k[2] == self.stack_start_symbol:
              if((k[3], [i for i in k[4][::-1]]) not in currentStates):
                currentStates.append((k[3], [i for i in k[4][::-1]]))
        nextStates = []
        for i in text:
          nextStates = []
          for j in currentStates:
            for k in self.transitions:
              if k[0] == j[0] and k[1] == i and self._isStackOk(j[1], [k[2]]):
                if((k[3], self._changeStack(j[1], k[2], [k[4]])) not in nextStates):
                    nextStates.append((k[3], self._changeStack(j[1], [k[2]], k[4])))

            for m in nextStates:
              for k in self.transitions:
                if k[0] == m[0] and k[1] == '' and self._isStackOk(m[1], [k[2]]):
                  if((k[3], self._changeStack(m[1], k[2], [k[4]])) not in nextStates):
                    nextStates.append((k[3], self._changeStack(m[1], [k[2]], k[4])))
          currentStates = nextStates
        for j in nextStates:
          if(j[0] == self.accept_state):
            return True
        return False
    
    def _isStackOk(self, stack, states):
        if(len(states) > len(stack)):
          return False
        for i in range(len(states)):
          if states[i] != stack[len(stack) - 1 - i]:
             return False
        return True
    
    def _changeStack(self, stack, states, newStates):
        return stack[ : len(stack) - len(states)] + [i for i in newStates[::-1]]
    
# configs of context free grammer
cfg = {
    'terminals': ['a', 'b'],
    'non_terminals': ['S'],
    'start': 'S',
    'productions': {
        'S': [['a','S','b'], ['a','b']],
    }
}

# convert cfg to npda
npda = NPDA(cfg)

#show resukt for a^nb^n
print("NPDA States:")
print(npda.automata['states'])
print("\nNPDA Transitions:")
for t in npda.automata['transitions']:
    print(t)
print("\nStart State:", npda.automata['start_state'])
print("Accept State:", npda.automata['accept_state'])
print("Stack Start Symbol:", npda.automata['stack_start_symbol'])
print(npda.check("ab"))