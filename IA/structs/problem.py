"""
    initial_state: initial state.
    fn_nextStates: Function that generates the successors of a state!
    fn_isGoal: A function that identifies an objective state.
    fn_h: Estimated heuristic function!
"""
import structs.carState as State

class Problem:
    def  _init_(self,initial_state):
        self.initial_state = initial_state
    
    def fn_isGoal(self):
        if(self.initial_state.track.env[self.initial_state.pos[0]][self.initial_state.pos[1]] == 'E'):
            return 'T'
        return 'NIL'

    def fn_nextState(self, s, a):
        st = State.State()
        xa=s.pos[0]
        ya=s.pos[1]
        x = s.pos[0] + s.vel[0] + a[0]
        y = s.pos[1] + s.vel[1] + a[1]
        vX = s.vel[0] + a[0]
        vY = s.vel[1] + a[1]
        if -1<x and x<s.track.size[0]:
            if -1<y and y<s.track.size[1]:
                if(s.track.env[x][y] == 'E'):
                    cost = -100
                elif(s.track.env[x][y] == 'X'):
                    x = xa
                    y = ya
                    vX = 0
                    vY = 0
                    cost = 20
                else:
                    cost = 1
                st._init_([x,y],[vX,vY],a,cost,s.track)
                return st
            st._init_([x,y],[vX,vY],a,-300,s.track)
            return st
        st._init_([x,y],[vX,vY],a,-300,s.track)
        return st

    def fn_nextStates(self, state):   
        actions = []
        statesAux = []

        for i in range(-1,2):
            for j in range(-1,2):
                statesAux.append(state)
                actions.append([i,j])

        states = []

        for i in range(9):
            state = State.State()
            state = self.fn_nextState(statesAux[i], actions[i])
            if -300 != state.cost:
                states.append(self.fn_nextState(statesAux[i], actions[i]))

        return states
    
    def fn_h(self):
        print("Estimated heuristic function!")