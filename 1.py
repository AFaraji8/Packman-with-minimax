import numpy as np
import random



def ghostmove(gg,A):
    g=gg.copy()
    #0->up,1->right,2->down,3->left
    m=random.randint(0, 3)
    #print('m=',m)
    print(" ")
    if m==0:
        print("ghost moves up.")
        if (g[0]==0 or A[g[0]-1,g[1]]==-1):
            return g
        else:
            g[0]=g[0]-1
            return g
    elif m==2:
        print("ghost moves down.")
        if (g[0]==8 or A[g[0]+1,g[1]]==-1):
            return g
        else:
            g[0]=g[0]+1
            return g
    elif m==1:
        print("ghost moves right.")
        if (g[1]==17 or A[g[0],g[1]+1]==-1):
            return g
        else:
            g[1]=g[1]+1
            return g
    elif m==3:
        print("ghost moves left.")
        if (g[1]==0 or A[g[0],g[1]-1]==-1):
            return g
        else:
            g[1]=g[1]-1
            return g




def nextstartp(gg,m):
        #0->up,1->right,2->down,3->left
    g=gg.copy()
    if m==0:
        if (g[0]==0 or A[g[0]-1,g[1]]==-1):
            return g
        else:
            g[0]=g[0]-1
            return g
    elif m==2:
        if (g[0]==8 or A[g[0]+1,g[1]]==-1):
            return g
        else:
            g[0]=g[0]+1
            return g
    elif m==1:
        if (g[1]==17 or A[g[0],g[1]+1]==-1):
            return g
        else:
            g[1]=g[1]+1
            return g
    elif m==3:
        if (g[1]==0 or A[g[0],g[1]-1]==-1):
            return g
        else:
            g[1]=g[1]-1
            return g
    return(gg)









def score(plnew,pastscor,B,pp):
    if (B[plnew[0],plnew[1]]==True):
        B[plnew[0],plnew[1]]=False
        return(int(pastscor+9))
    elif (plnew!=pp):
        return(int(pastscor-1))
    else:
        return(int(pastscor))


def finish(B,pl,g1l,g2l):
    if((pl[0]==g1l[0] and pl[1]==g1l[1]) or (pl[0]==g2l[0] and pl[1]==g2l[1]) ):
        return ([True,False])  #finished,lost
    elif np.any(B):
        return([False,False])  # not finished,-
    else:
        return([True,True])  #finished,win
         



def find_nearest_true(matrix, start):
    indices = np.argwhere(matrix)  # Find indices of True values
    if len(indices) > 0:
        distances = np.linalg.norm(indices - start, axis=1)  # Calculate distances from start index
        nearest_index = indices[np.argmin(distances)]
        nearest_distance = np.min(distances)
        return nearest_distance
    else:
        return None


def find_nearest_value(matrix, value, start):
    indices = np.argwhere(matrix == value)  # Find indices where the ghosts are
    if len(indices) > 0:
        distances = np.linalg.norm(indices - start, axis=1)  # Calculate distances from start index
        nearest_index = indices[np.argmin(distances)]
        nearest_distance = np.min(distances)
        return nearest_distance
    else:
        return None



def eutility(pl,A,B,g1,g2):
    start=pl
    v=finish(B,start,g1,g2)
    if (v==[True,False]):
        return (-85500)
    elif(v==[True,True]):
        return(85000)
    else:
        tl=find_nearest_true(B,start)
        if tl is None:
            return(0)
        d=find_nearest_value(A,4,start)
        i=0
        for k in range(4):
            nps=nextstartp(start,k)
            if(nps==start):
                i=i+1

        return(round(d*3)-(round(tl*3)+18-int(i/2)))

    






def minimax(depth, start,alpha, beta,A,B,g1l,g2l):  #depth:0->MAX,1->MIN1,2->MIN2,3->MAXU   Output->[value,move]
  
    if depth == 3:
        if (B[start[0],start[1]]):
            return ([eutility(start,A,B,g1l,g2l)+9,5])
        else:
            return ([eutility(start,A,B,g1l,g2l),5])        
 
    if (depth==0): 
      
        best =[-80000,3]
 
        bb=B.copy()
        bb[start[0],start[1]]=False

        
        for i in range(4): 

            nexts=nextstartp(start,i)
            aa=A.copy()



            val =[(minimax(depth + 1,nexts, alpha, beta,aa,bb,g1l,g2l))[0],i]
            if(best[0]<val[0]):
                best = val 
            alpha = max(alpha, best[0]) 
 
            # Alpha Beta Pruning 
            if beta <= alpha: 
                break
          
        return best 
    
    elif(depth==1):
        best = [80000,6]

        for i in range(0, 4): 
            nexts=nextstartp(g1l,i)
            aa=A.copy()
            aa[g1l[0],g1l[1]]=0
            aa[nexts[0],nexts[1]]=4

            val =[(minimax(depth + 1,start, alpha, beta,aa,B,nexts,g2l))[0],i]
            if(best[0]>val[0]):
                best = val 

            beta = min(beta, best[0]) 
 
            # Alpha Beta Pruning 
            if beta <= alpha: 
                break
          
        return best
      
    else:
        best = [80000,6]


        for i in range(0, 4): 
            nexts=nextstartp(g2l,i)
            aa=A.copy()
            aa[g2l[0],g2l[1]]=0
            aa[nexts[0],nexts[1]]=4

            val =[(minimax(depth + 1,start, alpha, beta,aa,B,g1l,nexts))[0],i]
            if(best[0]>val[0]):
                best = val 

            beta = min(beta, best[0]) 
 
            # Alpha Beta Pruning 
            if beta <= alpha: 
                break
          
        return best











print("Game environment  (hedge= -1 , pacman= 8 , ghosts=4):")

A=np.zeros([9,18],dtype=int)
    #hedges:
A[1:4,1]=(-1)
A[1:4,16]=(-1)
A[1,2]=(-1)
A[1,15]=(-1)
A[5:8,1]=(-1)
A[5:8,16]=(-1)
A[0:2,4]=(-1)
A[0:2,13]=(-1)
A[7,2]=(-1)
A[7,15]=(-1)
A[3,3:5]=(-1)
A[5,3:5]=(-1)
A[3,13:15]=(-1)
A[5,13:15]=(-1)
A[7:9,4]=(-1)
A[7:9,13]=(-1)
A[1,6:12]=(-1)
A[5,6:12]=(-1)
A[7,6:12]=(-1)
A[3:5,6]=(-1)
A[3:5,11]=(-1)
A[3,7]=(-1)
A[3,10]=(-1)
A[3,10]=(-1)



B=np.zeros([9,18],dtype=bool)
for i in range(9):
    for j in range(18):
        if (A[i,j]==0):
            B[i,j]=True

print(B)






# fist location of pacman


p_x=9
p_y=0
Pl=[p_y,p_x]
A[p_y,p_x]=8
print('first pacman location(',p_y,',',p_x,')')

g1_y=1
g1_x=5
g1l=[g1_y,g1_x]
A[g1_y,g1_x]=4
print('first ghost1 location(',g1_y,',',g1_x,')')

g2_y=1
g2_x=14
g2l=[g2_y,g2_x]
A[g2_y,g2_x]=4
print('first ghost2 location(',g2_y,',',g2_x,')')


print(A)


v=finish(B,Pl,g1l,g2l)
pscor=10
B[Pl[0],Pl[1]]=False
while(v[0]==False):
    move=minimax(0,Pl,-80000,80000,A,B,g1l,g2l)
    nexts=nextstartp(Pl,move[1])
    pscor=score(nexts,pscor,B,Pl)
    A[nexts[0],nexts[1]]=8
    A[Pl[0],Pl[1]]=0
    Pl[0]=nexts[0]
    Pl[1]=nexts[1]
    print('PACMAN MOVES TO (',Pl[0],',',Pl[1],')')
    print('score: ',pscor)

    A[g1l[0],g1l[1]]=0
    g1l=ghostmove(g1l,A)
    A[g1l[0],g1l[1]]=4
    print('GHOST1 MOVES TO (',g1l[0],',',g1l[1],')')

    A[g2l[0],g2l[1]]=0
    g2l=ghostmove(g2l,A)
    A[g2l[0],g2l[1]]=4
    print('GHOST2 MOVES TO (',g2l[0],',',g2l[1],')')
    print('---------------------------------------------------------------------------')
    v=finish(B,Pl,g1l,g2l)
    
if(v[1]==False):
    print("GAME OVER")
else:
    print("WIN")

