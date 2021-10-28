# -*- coding: utf-8 -*-
"""
Created on Thu May  6 21:40:34 2021

@author: Reese
"""

from math import sqrt

class Player():
  name = "BFS"
  group = "HELP"
  members = [
    ["Matthew Ng Yee Chun", "18031930"],
    ["Phang Chin Ter", "xxxxxxxx"],
    ["Hela", "87654654"],
    ["Reese", "14085906"]
  ]
  informed = True
  
  
  def __init__(self, setup):
    # setup = {
    #   maze_size: [int, int],
    #   static_snake_length: bool
    # }
    self.setup = setup

  def distanceFromParent(self, search_tree, currentNode):
    parent = currentNode["parent"]
    distance = -1
    while parent is not None:
      for s in search_tree:
        if s['id'] == parent:
          parent = s['parent']
          distance += 1
    return distance

  def run(self, problem):
    # problem = {
    #   snake_locations: [[int,int],[int,int],...],
    #   current_direction: str,
    #   food_locations: [[int,int],[int,int],...],
    # }
    
    found_goal = False
    goalie = problem['food_locations']
    
    expansionsequence = 0

    search_tree= []
    frontier = []
    explored = []
    
    parent = None
    directions = "nswe"
    directionsMap = {'w':[-1,0],'e':[1,0],'n':[0,-1], 's':[0,1]}
    
    frontier.append({'state': problem['snake_locations'][0],'action': []})
    
    search_tree.append({
      'id': (len(search_tree)+1),
      'state': problem['snake_locations'][0],
      'expansionsequence': expansionsequence,
      'children': [],      
      'actions': [],
      'removed': False,
      'parent': None
      })
    
    while not found_goal:
      # Create frontier
      for i, s in enumerate(search_tree):
        
        # Check if node in search tree is first element in frontier
        if s['state'] == frontier[0]['state']:
          expansionsequence += 1
          actions = []
          #print(s['state'])
          [x, y] = s['state']
          explored.append(s['state'])
          del frontier[0]
          
          # Check Goal
          if s['state'] in goalie:
            found_goal = True
            parent = s["parent"]
            break
          
          children = []
          for direction in directions:
            d = directionsMap.get(direction)
            coord = [x + d[0], y + d[1]]
              
            if -1 not in coord:
              if coord[0] < self.setup['maze_size'][0] and coord[1] < self.setup['maze_size'][1]:
                if coord not in problem['snake_locations'][0:len(problem["snake_locations"])-self.distanceFromParent(search_tree, s)]:
                  # Add children
                  childrenId = len(search_tree) + 1
                  children.append(childrenId)
                  
                  # Check duplicate
                  removed = False
                  for f in frontier:
                    if f['state'] == coord:
                      removed = True
                  if coord in explored:
                    removed = True
                    
                  #print("adding children: ", state)
                  search_tree.append({
                    "id": childrenId,
                    "state": coord,
                    "expansionsequence": -1,
                    "children": [],
                    "actions": [],
                    "removed": removed,
                    "parent": s['id']
                    })
                  
                  
                  
                  actions.append(direction)
                  if not removed:
                    frontier.append({'state': coord, 'action': direction})        
                             
          
          # Update parent node
          parent = search_tree.pop(i)
          new_parent = ({
            "id": parent["id"],
            "state": parent["state"],
            "expansionsequence": expansionsequence,
            "children": children,
            "actions": actions,
            "removed": parent["removed"],
            "parent": parent["parent"]
            })
          search_tree.insert(i , new_parent)
          
          # No actions
          if (len(frontier) == 0):
            found_goal = True
            parent = s["parent"]
            break
              
    solution = []
    currentLocation = explored[-1]
    
    while parent is not None:
      for s in search_tree:
        if s['id'] == parent:
          parent = s['parent']
          
          currentAction = ""
          translation = [currentLocation[0]-s['state'][0], currentLocation[1]-s['state'][1]]
          
          currentLocation = s['state']
          
          for key, value in directionsMap.items():
            if value == translation:
              currentAction = key
              break
            
          solution.insert(0, currentAction)  
            
    if len(solution) == 0:
      if (problem['current_direction'] == 'n'):
        solution = ['e']
      else:
        solution = ['n']
        
    print(search_tree)     
    
    return solution, search_tree  

if __name__ == "__main__":
  p1 = Player({ "maze_size": [10,10], "static_snake_length": True })
  sol, st = p1.run({'snake_locations': [[0, 5]], 'current_direction': 'e', 'food_locations': [[0, 6]]})
  print("Solution is:", sol)
  print("Search tree is:")
  #print(st)