class CFGtoNPDAConverter:
    def __init__(self, cfg):
        self.cfg = cfg
        self.states = set()
        self.transitions = []
        self.start_state = 'q0'
        self.accept_state = 'q_accept'
        self.stack_start_symbol = 'Z'
    
    def convert(self):
        # # Add initial transition to push start symbol onto the stack
        self.transitions.append(('q0', '', self.stack_start_symbol, 'q1', self.cfg['start'] + self.stack_start_symbol))
        self.states.update(['q0', 'q1'])

        for head, bodies in self.cfg['productions'].items():
            for body in bodies:
                self.transitions.append(('q1', body[0], head, 'q1', body[1:]))
        self.transitions.append(('q1', '.', self.stack_start_symbol, self.accept_state, ''))

        
        return {
            'states': self.states,
            'transitions': self.transitions,
            'start_state': self.start_state,
            'accept_state': self.accept_state,
            'stack_start_symbol': self.stack_start_symbol
        }

# Define the CFG
cfg = {
    'terminals': ['a', 'b'],
    'non_terminals': ['S', 'B'],
    'start': 'S',
    'productions': {
        'S': ['aSB', 'aB'],
        'B': ['b', ]
    }
}

# Convert CFG to NPDA
converter = CFGtoNPDAConverter(cfg)
npda = converter.convert()

print("NPDA States:")
print(npda['states'])
print("\nNPDA Transitions:")
for t in npda['transitions']:
    print(t)
print("\nStart State:", npda['start_state'])
print("Accept State:", npda['accept_state'])
print("Stack Start Symbol:", npda['stack_start_symbol'])