"""
    isObstaclep: function that checks for obstacles. Returns T if true, and NIL if false.
    isGoalp: function that checks if the state is the objective state. Returns T if true, and Nil if false.
    nextStates: function that returns a State that results from applying the action to the state.
    readTrack: function that reads tracks and returns track. O:track, X:obstacles, S:start position, E:end position.
"""

import structs.track as Track, structs.carState as State, structs.searchNode as Node, structs.problem as Problem

"""
    Optional Functions: These functions were created for better organization and understanding of the code.
    findInitPosition(t): is a function that, given a matrix, returns the position of the first S it finds.
    findFinalPositions(t): is a function that, given a matrix, returns a matrix of positions of the found E.
"""

def findInitPosition(t):
    for i in range(len(t)):
        for j in range(len(t[i])):
            if( t[i][j]=='S'):
                return [i,j]

def findFinalPositions(t):
    obs = 'X'*len(t[0])
    eP = []
    for i in range(len(t)):
        if(obs==str(t[i])):
            i+=1
        else:
            for j in range(len(t[i])):
                if( t[i][j]=='E'):
                    eP.append([i,j])
    return eP

def loadTrack(trackfile):
    #Matrix reading according to the website: https://stackoverflow.com/questions/53000522/how-to-read-text-file-into-matrix-in-python
    with open(trackfile, 'r') as f:
        #Read lines to matrix
        linha = f.readlines()
    #Creation of the matrix
    trackInicial = []
    cleanTrack = []
    #i represents the number of lines
    i=0
    #Read array from file
    for linha1 in linha:
        #Read the lines
        trackInicial.append(linha1)
        # increment of i
        i=i+1
        #Cleaning the track: we eliminate the \n
        cleanTrack.append(str(trackInicial[i-1]).replace('\n',''))
    size = [len(cleanTrack),len(cleanTrack[0])]
    startpos = findInitPosition(cleanTrack)
    endpositions = findFinalPositions(cleanTrack)
    tRack = Track.Track() 
    tRack._init_(size,cleanTrack,startpos, endpositions)
    return tRack

def make_state(posInicial, vel, action, cost, track):
    state = State.State()
    state._init_(posInicial,vel,action,cost,track)
    return state

def make_problem(state):
    problem = Problem.Problem()
    problem._init_(state)
    return problem

def isObstaclep(pos, track):
    if(track.env[pos[0]][pos[1]]=='X'):
        print('T')
    else: 
        print('NIL')

def isGoalp(state):
    eP = findFinalPositions(state.track.env)
    for i in eP:
        if state.pos[0] == i[0] and state.pos[1]== i[1]:
            return 'T'
    return 'NIL'

def state_to_str(state):
    print(state.toString())

"""
    This pseudocode was based on:
    function DEPTH-LIMITED-SEARCH(problem,limit) returns a solution, or failure/cutoff
        return RECURSIVE-DLS(MAKE-NODE(problem.INITIAL-STATE),problem,limit)
    function RECURSIVE-DLS(node,problem,limit) returns a solution, or failure/cutoff
         if problem.GOAL-TEST(node.STATE) then return SOLUTION(node)
         else if limit = 0 then return cutoff
         else
           cutoff_occurred? ← false
           for each action in problem.ACTIONS(node.STATE) do
              child ← CHILD-NODE(problem,node,action)
              result ← RECURSIVE-DLS(child,problem,limit-1)
              if result = cutoff then cutoff_occurred? ← true
              else if result ≠ failure then return result
           if cutoff_occurred? then return cutoff else return failure
"""
def limdepthfirstsearch(problem, limit):
    node = Node.Node()
    node._init_(None, problem.initial_state, 1,1,1)
    s = recursivelimdepthfirstsearch(node, problem, limit)
    if s=="cut" or s=="NIL":
        return s
    else:
        p = s.parent
        c = s
        sts = []
        while p != None:
            sts.append(c.state)
            c = p
            p = c.parent
        sts.append(c.state)
        sts.reverse()
        return sts

def recursivelimdepthfirstsearch(node, problem, limit):
    p = Problem.Problem()
    p._init_(node.state)
    goal = p.fn_isGoal()
    if(goal=='T'):
        return node
    elif limit == 0:
        return "cut"
    else:  
        thereWasCut = False
        successorStates = problem.fn_nextStates(node.state)
        for s in successorStates:
            nodeC = Node.Node()
            nodeC._init_(node, s, 1, 1, 1)
            result = recursivelimdepthfirstsearch(nodeC, problem, limit-1)
            if result == "cut":
                thereWasCut = True
            elif result != "NIL":
                return result
        if thereWasCut == True:
            return "cut"
        else:
            return "NIL"

def aStar(problem):
    node = Node.Node()
    h=compute_heuristic1(problem.initial_state)
    node._init_(None, problem.initial_state, h,0,h)
    s = recursiveastar(node, problem)
    if s=="cut" or s=="NIL":
        return s
    else:
        p = s.parent
        c = s
        sts = []
        while p != None:
            sts.append(c.state)
            c = p
            p = c.parent
        sts.append(c.state)
        sts.reverse()
        return sts

def k(e):
    return e[1]

def recursiveastar(node, problem):
    p = Problem.Problem()
    p._init_(node.state)
    goal = p.fn_isGoal()
    if(goal=='T'):
        return node
    else:  
        successorStates = problem.fn_nextStates(node.state)

        fns=[]

        for i in successorStates:
            h=compute_heuristic1(i)
            if h == "<M>":
                f = i.cost +node.g  + 1000000
                fns.append([i, f, i.cost+node.g, 1000000])
            else:
                f = i.cost+node.g + h
            fns.append([i, f, i.cost+node.g, h])
        fns.sort(key=k)

        for s in fns:
            if s[1] < 1000000 and s[0].cost!=20:
                nodeC = Node.Node()
                nodeC._init_(node, s[0], s[1], s[2], s[3])
                result = recursiveastar(nodeC, problem)
                if result != "NIL":
                    return result
        return "NIL"

def bestsearch(problem):
    node = Node.Node()
    h=compute_heuristic1(problem.initial_state)
    node._init_(None, problem.initial_state, h,0,h)
    s=recursivebestsearch(node, problem, 2000000)
    if s=="cut" or s=="NIL":
        return s
    else:
        p = s.parent
        c = s
        sts = []
        while p != None:
            sts.append(c.state)
            c = p
            p = c.parent
        sts.append(c.state)
        sts.reverse()
        return sts

def recursivebestsearch(node, problem, limit):
    p = Problem.Problem()
    p._init_(node.state)
    goal = p.fn_isGoal()
    if(goal=='T'):
        return node
    else:  
        childs = []
        fns=[]
        sucessors = problem.fn_nextStates(node.state)
        for i in sucessors:
            h=compute_heuristic1(i)
            if h == "<M>":
                f = max((i.cost +node.g  + 1000000), node.f)
                fns.append([i, f, i.cost+node.g, 1000000])
            else:
                f = max((i.cost+node.g + h), node.f)
            fns.append([i, f, i.cost+node.g, h])
        fns.sort(key=k)

        for s in fns:
            nodeC = Node.Node()
            nodeC._init_(node, s[0], s[1], s[2], s[3])
            childs.append(nodeC)
        
        if(childs.__len__()==0):
            return "NIL"

        for s in childs:
            if s.f > limit:
                return "NIL"
            if childs.__len__()>1:
                alternative = childs[1].f
                result = recursivebestsearch(s,problem, min(limit, alternative))
                if result != "NIL":
                    return result
        return "NIL"
"""
    This pseudocode was based on:
    function ITERATIVE-DEEPENING-SEARCH(problem) returns a solution, or failure
     for depth = 0 to ∞ do
       result ← DEPTH-LIMITED-SEARCH(problem,depth)
       if result ≠ cutoff then return result
""" 
def iterlimdepthfirstsearch(problem):
    i=0
    s = limdepthfirstsearch(problem, i)

    while (s=="cut" or s=="NIL") and i<problem.initial_state.track.size[1]:
        s=limdepthfirstsearch(problem, i)
        i+=1
    if s != "cut" or s !="NIL":
        return s
    else:
        return "NIL"

"""
    Just a function to help print results from search.
"""
def printResult(s):
    if s=="cut" or s=="NIL":
        print(s)
    else:
        for i in s:
            print("Pos: "+str(i.pos) +" Vel: "+str(i.vel) +" Action: "+str(i.action) +" Cost: "+str(i.cost))

"""
    Was based on Manhattan distance.
    Manhattan distance: The distance between two points measured along axes at right angles. In a plane with p1 at (x1, y1) and p2 at (x2, y2), it is |x1 - x2| + |y1 - y2|.
    Chooses the smallest heuristic from the state to the final state.
"""
def compute_heuristic1(state):
    finalStates = findFinalPositions(state.track.env)
    if state.track.env[state.pos[0]][state.pos[1]] == "S" or state.track.env[state.pos[0]][state.pos[1]] == "0":
        fS = finalStates[0]
        x = abs(state.pos[0] - fS[0])
        y = abs(state.pos[1] - fS[1])
        h = x+y
        for i in finalStates:
            x = abs(state.pos[0] - i[0])
            y = abs(state.pos[1] - i[1])
            if h > x+y:
                h = x+y
        return h
    elif state.track.env[state.pos[0]][state.pos[1]] == "E":
        return 0
    else:
        return "<M>"

def compute_heuristic(state):
    finalStates = findFinalPositions(state.track.env)
    fS = finalStates[0]
    hM = []
    for i in range(state.track.size[0]):
        hL = []
        x = abs(state.pos[0] - fS[0])
        y = abs(state.pos[1] - fS[1])
        h = x+y
        for j in range(state.track.size[1]):
            if state.track.env[i][j] != 'X' and state.track.env[i][j] != 'E':
                for k in finalStates:
                    x = abs(i - k[0])
                    y = abs(j - k[1])
                    if h > x+y:
                        h = x+y
                hL.append(h)
            elif state.track.env[i][j] == 'E':
                hL.append(0)
            else:
                hL.append("<M>")
        hM.append(hL)
    hM
    return hM

def main():
    trackFile = input("Digite o nome do ficheiro: ")
    #trackFile = str(a)+".txt"
    track = loadTrack(trackFile)
    StateInicial = make_state(track.startpos, [0,1], None, 0, track)
    action = [1,-1]
    prev_goal_state = make_state([2,13], [0,4], [1,1], 1, track)
    goal_state = make_state([3,16], [1,3], [1,-1], -100, track)
    goal_state1 = make_state([5,16], [-1,2],[-1,0],1,track)

    non_goal_state = make_state([3,6],[-1,2],[-1,0], 1, track)
    non_goal_state1 = make_state([5,7], [-1,2],[-1,0],1,track)

    obstacle = [2,2]
    obstacle1 = [1,2]
    obstacle2 = [6,16]

    non_obstacle = [2,8]
    non_obstacle1 = [3,3]
    non_obstacle2 = [2,10]

    print("\nExercise 1.1 - isObstaclep")
    isObstaclep(obstacle, track)
    isObstaclep(obstacle1, track)
    isObstaclep(obstacle2, track)

    isObstaclep(non_obstacle, track)
    isObstaclep(non_obstacle1, track)
    isObstaclep(non_obstacle2, track)

    print("\nExercise 1.2 - isGoalp")
    print(isGoalp(goal_state))
    print(isGoalp(goal_state1))

    print(isGoalp(non_goal_state))
    print(isGoalp(non_goal_state1))

    prob = make_problem(StateInicial)

    print("\nExercise 1.3 - nextState")
    state_to_str(prob.fn_nextState(prev_goal_state, action))
    state_to_str(prob.fn_nextState(StateInicial, action))

    print("\nExercise 3.1 - nextStates")
    prob = make_problem(StateInicial)
    states = prob.fn_nextStates(StateInicial)
    for i in states:
        state_to_str(i)
    
    print("\nExercise 3.2 - Limited Depth-First Search")
    s = limdepthfirstsearch(prob, 3)
    printResult(s)

    print("\nExercise 3.3 - Iterative Depth-First Search")
    s = iterlimdepthfirstsearch(prob)
    printResult(s)

    print("\nExercise 4.1 - Compute Heuristic")
    s = compute_heuristic1(StateInicial)
    print(s)

    print("\nExercise 4.1 - Compute Heuristic, Matrix")
    s = compute_heuristic(StateInicial)
    z = 0
    for i in s:
        print(str(s[z]))
        z = z+1

    print("\nExercise 4.2 - A*")
    s = aStar(prob)
    printResult(s)

    print("\nExercise 4.3 - Best Search")
    s = bestsearch(prob)
    printResult(s)

main()


"""# NÃO 
def orderlistofcoordinates():
    print("Compara estruturas do tipo Track")
"""