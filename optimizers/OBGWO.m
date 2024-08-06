 function [Alpha_score,Alpha_pos]=OBGWO(SearchAgents_no,Max_iteration,lb,ub,dim,fobj,run);
 
     OP=0.1;
     
 %initialization of the population uniformly
  Positions=initialization(SearchAgents_no,dim,ub,lb,run);
  
  %evaluate their fitness
  for i=1:SearchAgents_no
        Fitness(i)=fobj(Positions(i,:));
  end
  fitness=Fitness';
  
  %GENERATE POP WITH OPPOSITION
  
  for i=1:SearchAgents_no
       for j=1:dim
            O_Positions(i,j)=(ub+lb)-Positions(i,j);
           
             if O_Positions(i,j)>ub 
                O_Positions(i,j)=ub;
             end
             if O_Positions(i,j)<lb
                O_Positions(i,j)=lb;
            
             end
       end
     O_Fitness(i)=fobj(O_Positions(i,:));
  end
  O_fitness=O_Fitness';
  
  %MERGE THESE TWO POP TO PICK INITIAL  POPULATION
  
        New_mat1=[fitness Positions;O_fitness O_Positions];
        [values, order]=sort(New_mat1(:,1));
        New_mat2=New_mat1(order,:);
        
        Positions=New_mat2(1:SearchAgents_no,2:size(New_mat2,2));
        fitness=New_mat2(1:SearchAgents_no,1);
        
        %SELECT THE LEADERS OF GWO
        
        Alpha_score= fitness(1,1); % Update alpha
        Alpha_pos= Positions(1,:);
            
        Beta_score= fitness(2,1); % Update alpha
        Beta_pos= Positions(2,:);
       
        Delta_score= fitness(3,1); % Update alpha
        Delta_pos= Positions(3,:);
        
        Saved_matrix=[Alpha_score Alpha_pos;Beta_score Beta_pos;Delta_score Delta_pos];
        
  l=0;
  
  while l<Max_iteration

   
         a=2-2*(l/Max_iteration);   % linearly decreasing vector from 2 to 0

    % Update the Position of search agents including omegas
    for i=1:size(Positions,1)
        for j=1:size(Positions,2)     
                       
            r1=rand(); 
            r2=rand(); 
            
            A1=2*a*r1-a; 
            C1=2*r2; 
            
            D_alpha=abs(C1*Alpha_pos(j)-Positions(i,j)); 
            X1=Alpha_pos(j)-A1*D_alpha; 
                       
            r1=rand();
            r2=rand();
            
            A2=2*a*r1-a; 
            C2=2*r2; 
            
            D_beta=abs(C2*Beta_pos(j)-Positions(i,j)); 
            X2=Beta_pos(j)-A2*D_beta;       
            
            r1=rand();
            r2=rand(); 
            
            A3=2*a*r1-a; 
            C3=2*r2; 
            
            D_delta=abs(C3*Delta_pos(j)-Positions(i,j)); 
            X3=Delta_pos(j)-A3*D_delta;             

            U_Positions(i,j)=(X1+X2+X3)/3;
   
             if U_Positions(i,j)>ub 
                U_Positions(i,j)=ub;
             end
             if U_Positions(i,j)<lb
                U_Positions(i,j)=lb;
            
             end
         end
          U_Fitness(i)=fobj(U_Positions(i,:));
    end
         U_fitness=U_Fitness';
         
         %UPDATED POSITIONS WITH GWO
         U_matrix=[U_fitness U_Positions];
         
  if rand()<=OP
      
    for i=1:SearchAgents_no
        for j=1:dim
             O_Positions(i,j)=(ub+lb)-Positions(i,j);
           
             if O_Positions(i,j)>ub 
                O_Positions(i,j)=ub;
             end
             if O_Positions(i,j)<lb
                O_Positions(i,j)=lb;
            
             end
       end
       O_Fitness(i)=fobj(O_Positions(i,:));
    end
    O_fitness=O_Fitness';
  
    %OPPOSITION MATRIX
    
       O_matrix=[O_fitness O_Positions];
       
        mat1=[U_matrix;O_matrix;Saved_matrix];
        [values, order]=sort(mat1(:,1));
        mat2=mat1(order,:);
        
      Alpha_score=mat2(1,1);
      Beta_score=mat2(2,1);
      Delta_score=mat2(3,1);
      Alpha_pos=mat2(1,2:size(New_mat2,2));
      Beta_pos=mat2(2,2:size(New_mat2,2));
      Delta_pos=mat2(3,2:size(New_mat2,2));
 
       
        New_mat1=[U_matrix;O_matrix];
        [values, order]=sort(New_mat1(:,1));
        New_mat2=New_mat1(order,:);
        
        Positions=New_mat2(1:SearchAgents_no,2:size(New_mat2,2));
        fitness=New_mat2(1:SearchAgents_no,1);
        
        %SAVED MATRIX
        Saved_matrix=[Alpha_score Alpha_pos;Beta_score Beta_pos;Delta_score Delta_pos];
  else
      
        mat1=[U_matrix;Saved_matrix];
        [values, order]=sort(mat1(:,1));
        mat2=mat1(order,:);
        
        %SELECT LEADERS
       Alpha_score=mat2(1,1);
      Beta_score=mat2(2,1);
      Delta_score=mat2(3,1);
      Alpha_pos=mat2(1,2:size(New_mat2,2));
      Beta_pos=mat2(2,2:size(New_mat2,2));
      Delta_pos=mat2(3,2:size(New_mat2,2));
      
      %SAVED_MATRIX
      Saved_matrix=[Alpha_score Alpha_pos;Beta_score Beta_pos;Delta_score Delta_pos];
      
      %POSITION FOR NEXT ITERATION
      Positions=U_Positions;
      fitness=U_fitness;
  end
  
%   
%   if rem(l,1)==0
%       display(num2str(Alpha_score));
%   end
  l=l+1;
  end
 end
        
        

  
   