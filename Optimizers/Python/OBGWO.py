# matlab conversion from chatGPT

import numpy as np

class OBGWO:
    def __init__(self, fobj, lb, ub, dim, SearchAgents_no, Max_iteration, OP=0.1):
        self.fobj = fobj  # Objective function
        self.lb = lb  # Lower bounds
        self.ub = ub  # Upper bounds
        self.dim = dim  # Dimension of the problem
        self.SearchAgents_no = SearchAgents_no  # Number of search agents
        self.Max_iteration = Max_iteration  # Maximum number of iterations
        self.OP = OP  # Opposition probability
        
        # Initialize alpha, beta, delta
        self.Alpha_score = float("inf")
        self.Beta_score = float("inf")
        self.Delta_score = float("inf")
        
        self.Alpha_pos = np.zeros(dim)
        self.Beta_pos = np.zeros(dim)
        self.Delta_pos = np.zeros(dim)

    def initialization(self, SearchAgents_no, dim, ub, lb):
        return lb + (ub - lb) * np.random.rand(SearchAgents_no, dim)

    def optimize(self):
        # Initialization of positions
        Positions = self.initialization(self.SearchAgents_no, self.dim, self.ub, self.lb)
        
        # Evaluate initial fitness
        Fitness = np.array([self.fobj(ind) for ind in Positions])
        
        # Opposition-based learning
        O_Positions = self.ub + self.lb - Positions
        O_Positions = np.clip(O_Positions, self.lb, self.ub)
        O_Fitness = np.array([self.fobj(ind) for ind in O_Positions])
        
        # Merge populations and sort
        New_mat = np.vstack((np.hstack((Fitness.reshape(-1, 1), Positions)),
                             np.hstack((O_Fitness.reshape(-1, 1), O_Positions))))
        New_mat = New_mat[np.argsort(New_mat[:, 0])]
        
        # Update positions and fitness
        Positions = New_mat[:self.SearchAgents_no, 1:]
        Fitness = New_mat[:self.SearchAgents_no, 0]
        
        # Initialize Alpha, Beta, Delta
        self.update_leaders(Fitness, Positions)
        Saved_matrix = np.vstack((self.Alpha_score, self.Alpha_pos,
                                  self.Beta_score, self.Beta_pos,
                                  self.Delta_score, self.Delta_pos)).reshape(3, -1)
        
        l = 0
        while l < self.Max_iteration:
            a = 2 - 2 * l / self.Max_iteration  # Decrease a linearly
            
            # Update positions of search agents
            U_Positions = self.update_positions(Positions, a)
            U_Positions = np.clip(U_Positions, self.lb, self.ub)
            U_Fitness = np.array([self.fobj(ind) for ind in U_Positions])
            
            # Create updated matrix
            U_matrix = np.hstack((U_Fitness.reshape(-1, 1), U_Positions))
            
            if np.random.rand() <= self.OP:
                # Opposition-based learning
                O_Positions = self.ub + self.lb - Positions
                O_Positions = np.clip(O_Positions, self.lb, self.ub)
                O_Fitness = np.array([self.fobj(ind) for ind in O_Positions])
                
                # Merge and sort the matrices
                O_matrix = np.hstack((O_Fitness.reshape(-1, 1), O_Positions))
                mat = np.vstack((U_matrix, O_matrix, Saved_matrix))
                mat = mat[np.argsort(mat[:, 0])]
                
                # Update leaders
                self.update_leaders(mat[:, 0], mat[:, 1:])
                
                # Update saved matrix
                Saved_matrix = mat[:3, :]
                
                # Select new positions for next iteration
                Positions = mat[:self.SearchAgents_no, 1:]
                Fitness = mat[:self.SearchAgents_no, 0]
            else:
                # Merge U_matrix with saved matrix
                mat = np.vstack((U_matrix, Saved_matrix))
                mat = mat[np.argsort(mat[:, 0])]
                
                # Update leaders
                self.update_leaders(mat[:, 0], mat[:, 1:])
                
                # Update saved matrix
                Saved_matrix = mat[:3, :]
                
                # Positions for next iteration
                Positions = U_Positions
                Fitness = U_Fitness
            
            l += 1
            
        return self.Alpha_score, self.Alpha_pos
    
    def update_leaders(self, fitness, positions):
        self.Alpha_score = fitness[0]
        self.Alpha_pos = positions[0, :]
        
        self.Beta_score = fitness[1]
        self.Beta_pos = positions[1, :]
        
        self.Delta_score = fitness[2]
        self.Delta_pos = positions[2, :]
    
    def update_positions(self, Positions, a):
        r1, r2 = np.random.rand(), np.random.rand()
        A1, C1 = 2 * a * r1 - a, 2 * r2
        X1 = self.Alpha_pos - A1 * np.abs(C1 * self.Alpha_pos - Positions)
        
        r1, r2 = np.random.rand(), np.random.rand()
        A2, C2 = 2 * a * r1 - a, 2 * r2
        X2 = self.Beta_pos - A2 * np.abs(C2 * self.Beta_pos - Positions)
        
        r1, r2 = np.random.rand(), np.random.rand()
        A3, C3 = 2 * a * r1 - a, 2 * r2
        X3 = self.Delta_pos - A3 * np.abs(C3 * self.Delta_pos - Positions)
        
        return (X1 + X2 + X3) / 3


