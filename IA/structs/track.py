"""
    size: is a list with two elements: size = [num_of_rows, num_of_columns]
    env: is a list of lists(array), which represents the track. The X represents obstacles, 0 the track, S the starting position, and E the ending positions.
    startpos: it is a list with two elements: startpos = [number_of_rows, num_of_columns], which represents the starting position
    endpositions: list of end positions.
"""
class Track:
    def  _init_(self,size,env,startpos,endpositions):
         self.size= size
         self.env=env
         self.startpos=startpos
         self.endpositions= endpositions
    
    
    