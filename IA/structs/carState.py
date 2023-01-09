"""
    pos(position): is a list with two elements, pos = [row, column]
    vel: is the speed at which the car moves. It is a list of two elements: v = [vx,vy], where vx is the velocity in the horizontal direction and vy is the velocity in the vertical direction.
    action: is the action that gave rise to the state. It is a list of two elements: action = [ax, ay].
    cost: is the cost of the action that caused the state transition. It is not cumulative.
    track: is the track.
    other: additional information
"""
class State:
    def  _init_(self,pos,vel,action,cost,track):
         self.pos = pos
         self.vel=vel
         self.action=action
         self.cost= cost
         self.track=track
         #self.other=other

    def toString(self):
        return "Pos: "+str(self.pos) +" Vel: "+str(self.vel) +" Action: "+str(self.action) +" Cost: "+str(self.cost)