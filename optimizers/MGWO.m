

function [Alpha_score,Alpha_pos]=MGWO(SearchAgents_no,Max_iter,lb,ub,dim,fobj,run)

 Positions=initialization(SearchAgents_no,dim,ub,lb);

% fitness1=zeros(1,dim);
% fitness2=zeros(1,dim);

    for i=1:size(Positions,1)  
       fitness1(i)=fobj(Positions(i,:));
    end
    
    fitness=fitness1';
    
     New_mat1=[fitness Positions];
     [values, order]=sort(New_mat1(:,1));
      New_mat2=New_mat1(order,:);
       
           % Update Alpha, Beta, and Delta
      
      Alpha_score= New_mat2(1,1); % Update alpha
      Alpha_pos= New_mat2(1,2:size( New_mat2,2));
            
      Beta_score= New_mat2(2,1); % Update alpha
      Beta_pos= New_mat2(2,2:size( New_mat2,2));
       
      Delta_score= New_mat2(3,1); % Update alpha
      Delta_pos= New_mat2(3,2:size( New_mat2,2));
            
%       Positions=New_mat2(:,2:size(New_mat2,2));
%       fitness=New_mat2(:,1);
      U_Positions=zeros(SearchAgents_no,dim);
      
      Saved_matrix=New_mat2(1:3,:);
      pbest_pos=Positions;
      pbest_score=fitness;

l=0;% Loop counter

% Main loop
while l<Max_iter

            a=2-l*((2)/Max_iter);    % linearly decreasing vector from 2 to 0

    % Update the Position of search agents including omegas
    for i=1:size(Positions,1)
        for j=1:size(Positions,2)     
                       
            r1=rand(); 
            r2=rand(); 
            
            A1=2*a*r1-a; 
            C1=2*r2; 
            
            D_alpha=abs(C1*Alpha_pos(j)-pbest_pos(i,j)); 
            X1=Alpha_pos(j)-A1*D_alpha; 
                       
            r1=rand();
            r2=rand();
            
            A2=2*a*r1-a; 
            C2=2*r2; 
            
            D_beta=abs(C2*Beta_pos(j)-pbest_pos(i,j)); 
            X2=Beta_pos(j)-A2*D_beta;       
            
            r1=rand();
            r2=rand(); 
            
            A3=2*a*r1-a; 
            C3=2*r2; 
            
            D_delta=abs(C3*Delta_pos(j)-pbest_pos(i,j)); 
            X3=Delta_pos(j)-A3*D_delta;             
            
       
       k=rand();
       n11=randperm(SearchAgents_no);
       num1=n11(1);
       num2=n11(2);
       if k<0.5       
            U_Positions(i,j)=(X1+X2+X3)/3;
       else
           AA=1-l*(1/Max_iter); 
           U_Positions(i,j)=pbest_pos(i,j)+AA*(Positions(num1,j)-Positions(num2,j));
           
       end

      
             if U_Positions(i,j)>ub
                U_Positions(i,j)=lb+rand()*(ub-lb);
             end
             if U_Positions(i,j)<lb
                U_Positions(i,j)=lb+rand()*(ub-lb);
             end
        end
     fitness2(i)=fobj(U_Positions(i,:));
     
    end     
 
   
  
  
    U_fitness=fitness2';
    for i=1:size(Positions,1)             %greedy technique
        
        if U_fitness(i)<=pbest_score(i)
            pbest_pos(i,:)=U_Positions(i,:);
            pbest_score(i)=U_fitness(i);
        end
       if  U_fitness(i)>fitness(i) 
           U_fitness(i)=fitness(i);
           U_Positions(i,:)=Positions(i,:);
       end
    end
    
  
        New_mat1=[U_fitness U_Positions;Saved_matrix];
        [values, order]=sort(New_mat1(:,1));
        New_mat2=New_mat1(order,:);

        
        Alpha_score= New_mat2(1,1); % Update alpha
        Alpha_pos= New_mat2(1,2:size( New_mat2,2));
            
        Beta_score= New_mat2(2,1); % Update alpha
        Beta_pos= New_mat2(2,2:size( New_mat2,2));
       
        Delta_score= New_mat2(3,1); % Update alpha
        Delta_pos= New_mat2(3,2:size( New_mat2,2));
        
        Saved_matrix=New_mat2(1:3,:);


Positions=U_Positions;
fitness=U_fitness;
 l=l+1; 
    
end

     
end