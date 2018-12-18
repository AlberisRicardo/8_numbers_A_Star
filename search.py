
import random
import copy

class Board(object):

    def __init__(self, tiles):

        self.tiles = tiles

    def is_goal(self):

        goal = Board([1, 2, 3, 4, 5, 6, 7, 8, "x"])
        return self.__eq__(goal) 

    def heuristic(self):

        goal = [1, 2, 3, 4, 5, 6, 7, 8, "x"]
        cont = 0
        for a in range (len(self.tiles)):
            if(goal[a] != self.tiles[a]):
                cont+=1
        return cont

    def get_neighbors(self):
.
        moves = []
        x_index = self.tiles.index("x")
        move_to = {
            "line_above": x_index - 3, 
            "line_below": x_index + 3, 
            "left_column": x_index - 1,
            "right_column": x_index + 1
        }
        column = {
            "left":move_to["left_column"] % 3,
            "right":move_to["right_column"] % 3
        }
        limit ={
            "up": 0,
            "down": 8,
            "sides": x_index % 3
        }

        if (move_to["line_above"] >= limit["up"]):
            moves.append(move_to["line_above"])

        if (move_to["line_below"] <= limit["down"]):
            moves.append(move_to["line_below"])

        if column["left"] < limit["sides"]:
            moves.append(move_to["left_column"])

        if column["right"] > limit["sides"]:
            moves.append(move_to["right_column"])
        
        return self.create_neighbors(moves)


    def create_neighbors(self,moves):
    
        neighbors = []
        x_index = self.tiles.index("x")
        for value in moves:
            temp = copy.copy(self.tiles)
            temp[x_index] = temp[value]
            temp[value] = "x"
            neighbors.append(Board(temp))
        return neighbors


    def __eq__(self, other):
        return self.tiles == other.tiles

    def __hash__(self):
        return hash(tuple(self.tiles))

    def __str__(self):
        return str(self.tiles)

    def __repr__(self):
        return str(self.tiles)

    def print_board(self):
        print(self.tiles[:3])
        print(self.tiles[3:6])
        print(self.tiles[6:])

    


class Node(object):

    def __init__(self, state, cost):

        self.state = state
        self.cost = cost
        self.parent = None

    def __str__(self):
        return str(self.state.tiles) + " - " + str(self.cost)

    def __repr__(self):
        return str(self.state.tiles) + " - " + str(self.cost)


class AStar(object):

    def __init__(self, initial_state):

        self.initial_state = initial_state
        self.frontier = [Node(self.initial_state, 0 + self.initial_state.heuristic())]
        self.explored = set()
        self.current_node = None

    def choose_from_frontier(self):

        current_cost = self.frontier[0]
        cont = 0
        for a in range(len(self.frontier)):
            if self.frontier[a].cost < current_cost.cost:
                current_cost = self.frontier[a]
                cont = a
        return self.frontier.pop(cont)

    def update_frontier(self):

        neighbors = self.current_node.state.get_neighbors()
        path_cost = self.current_node.cost - self.current_node.state.heuristic() + 1
        new_node_cost = path_cost
        
        for neighbor in neighbors:
            new_node_cost += neighbor.heuristic()
            
            if self.is_neighbor_in_frontier(neighbor):
                node = self.frontier[self.get_frontier_index(neighbor)]
                
                if new_node_cost < node.cost:
                    node.parent = self.current_node
                    node.cost = new_node_cost
            
            elif not (neighbor in self.explored):
                new_node = Node(neighbor, new_node_cost)
                new_node.parent = self.current_node
                self.frontier.append(new_node)       
            
            new_node_cost -= neighbor.heuristic()

    def get_frontier_index(self, neighbor):

        for index in range(len(self.frontier)):
            if self.frontier[index].state == neighbor:
                return index


    def is_neighbor_in_frontier(self, neighbor):

        for node in self.frontier:
            if node.state == neighbor:
                return True
        
        return False

    def get_path(self, node):
.
        if (node.parent.state == self.initial_state): 
            node_list = []
            node_list.append(self.initial_state)
            node_list.append(node.state)
            return node_list
            
        node_list = self.get_path(node.parent)
        node_list.append(node.state)
        return node_list

    def search(self):

        while True:
            if len(self.frontier) == 0:
                return False

            self.current_node = self.choose_from_frontier()
            
            self.explored.add(self.current_node.state)

            if self.current_node.state.is_goal():
                return self.current_node

            self.update_frontier()
            
        
if __name__ == "__main__":
 
    tiles = [3, 2, 8, 1, 5, 4, 7, 6, "x"]
    #tiles = [1, 2, 3, 4, 5, 6, 7, 8, "x"]
    #tiles = [1,2,3,4,"x",6,7,5,8]
    #tiles = [1,"x",3,4,2,6,7,5,8]
    #tiles = [1,3,6,4,"x",2,7,5,8]
    #tiles = ["x",1,6,4,3,2,7,5,8]
    #tiles = [2,7,8,6,"x",4,5,3,1]
    #tiles = [3, 1, 4, 2, 'x', 7, 5, 8, 6]
    #tiles = [3, 2, 4, 'x', 7, 6, 5, 1, 8]
    initial_state = Board(tiles)

    astar = AStar(initial_state)
    final_node = astar.search()
    path = astar.get_path(final_node)
    print("caminho")
    
    for state in path:
        state.print_board()
        print("---")
    print(len(path))