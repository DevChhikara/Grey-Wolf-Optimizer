function [Alpha_score,Alpha_pos]=RWGWO(fhd,pop_size,iter_max,Xmin,Xmax,D,func_num)
 
Positions=initialization(pop_size,D,Xmax,Xmin);

    for i=1:size(Positions,1)  
       fitness1(i)=fhd((Positions(i,:))',func_num);
    end
    
    fitness=fitness1';
    
     New_mat1=[fitness Positions];
     [values, order]=sort(New_mat1(:,1));
      New_mat2=New_mat1(order,:);
      
      Alpha_score= New_mat2(1,1); % Update alpha
      Alpha_pos= New_mat2(1,2:size( New_mat2,2));  
      Beta_pos= New_mat2(2,2:size( New_mat2,2));
       
      Delta_pos= New_mat2(3,2:size( New_mat2,2));
            
      Positions=New_mat2(:,2:size(New_mat2,2));
      fitness=New_mat2(:,1);
      U_Positions=zeros(pop_size,D);

l=0;
while l<iter_max
    xo=0;
    gamma=1;
 par=2-2*(l/iter_max);
    for i=1:3
        for j=1:D
            y=rand();
            randomwalk=xo+gamma*tan(pi*(y-0.5));      
            k=rand();
            U_Positions(i,j)=Positions(i,j)+randomwalk*par;
        end  
    end
        
     
            a=2-2*(l/iter_max);   % linearly decreasing vector from 2 to 0

    % Update the Position of search agents including omegas
    for i=4:size(Positions,1)
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
          
        end
     
    end     
 
   for i=1:size(U_Positions,1)
       for j=1:size(U_Positions,2)
             if U_Positions(i,j)>Xmax 
                U_Positions(i,j)=Xmax;
             end
             if U_Positions(i,j)<Xmin
                U_Positions(i,j)=Xmin;
            
             end
       end
       U_fitness(i)=fhd((U_Positions(i,:))',func_num);
              if  U_fitness(i)>fitness(i) 
           U_fitness(i)=fitness(i);
           U_Positions(i,:)=Positions(i,:);
       end
   end
  
  
     
        New_mat1=[U_fitness' U_Positions];
        [values, order]=sort(New_mat1(:,1));
        New_mat2=New_mat1(order,:);

        
        Alpha_score= New_mat2(1,1); % Update alpha
        Alpha_pos= New_mat2(1,2:size( New_mat2,2));
        Beta_pos= New_mat2(2,2:size( New_mat2,2));
        Delta_pos= New_mat2(3,2:size( New_mat2,2));
        Positions=New_mat2(:,2:size(New_mat2,2));
        fitness=New_mat2(:,1);
 l=l+1;   
end   
end


