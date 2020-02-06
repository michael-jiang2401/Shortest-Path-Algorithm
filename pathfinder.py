from lab1_utilities import *


def get_installations_from_file(file_name):
    myfile=open(file_name, 'r')
    myfile.readline()
    installations=[]
    for line in myfile:
        data=[x for x in line.split('\t')]
        name=data[0]
        ward=int(data[2])
        position=(float(data[7]), float(data[8]))
        data[15]=data[15].replace('\n', '')
        if data[15]=="INDOORS": 
            indoors=True
        else:
            indoors=False
        installation = Installation(name, ward, position, indoors)
        installations+=[installation]
    return installations
        

def euclidean_distance(position1, position2):
    x1=position1[0]
    y1=position1[1]
    x2=position2[0]
    y2=position2[1]
    return ((x2-x1)**2 +(y2-y1)**2)**(1/2)


def get_adjacency_mtx(installations):
    matrix=[]
    for i in range(len(installations)):
        row=[]
        
        ward1=installations[i].ward
        position1=installations[i].position
        indoor1=installations[i].indoor
        
        for j in range(len(installations)):
            
            ward2=installations[j].ward
            position2=installations[j].position
            indoor2=installations[j].indoor  
            
            distance = euclidean_distance(position2, position1)
            
            if installations[i]==installations[j]:
                row+=[0]
            elif abs(ward2-ward1)>1:
                row+=[0]
            else:
                if not indoor1 and not indoor2:
                    row+=[distance]
                else:
                    row+=[1.5*distance]
        matrix += [row]
    return matrix
        


def make_graph(installations):
    names=[]
    for installation in installations:
        names.append(installation.name)
    mtx=get_adjacency_mtx(installations)
    graph=Graph(names, mtx)
    return graph


def find_shortest_path(installation_A, installation_B, graph):
    
    
    installations=graph.installations
    matrix=graph.adjacency_mtx
    
    #finding index of start and end nodes
    for i in range(len(installations)):
        if installations[i]==installation_A:
            start=i
        if installations[i]==installation_B:
            end=i
          
    #checks if starting node is end node      
    if start==end:
        return (float(0), [])
    
    visited=[start]
    visited.append(start)
    paths=[]
    for i in range(len(installations)):
        paths+=[[start]]
    cost = []
    for i in range(len(installations)):
        cost.append(0)
    
    

    for i in range(len(installations)):
        for j in range(len(installations)):
            if matrix[i][j]==0:
                matrix[i][j]=float('inf')
    
    for j in range(len(installations)):
        cost[j]=matrix[start][j]
    
    
    for i in range(len(installations)):
        minimum = float('inf')
        for j in range(len(installations)):
            if cost[j] <= minimum and j not in visited:
                minimum = cost[j]
                
                curr=j
                
                
        visited.append(curr)
        for j in range(len(installations)):
            if cost[j] >= cost[curr] + matrix[curr][j]:
                cost[j] = cost[curr] + matrix[curr][j]   
                paths[j].append(curr)
    
    '''
    paths[start]=[0]
    for i in range(len(paths)):
        if not paths[i]==[0]:
            paths[i].append(i)
        '''   
    
    
    paths[start]=[start]
    for i in range(len(paths)):
        if i==start:
            pass
        if cost[i]<float('inf'):
            paths[i].append(i)
        else:
            paths[i]=None

    
    val=float(cost[end])
    if val <float('inf'):
        val=float(cost[end])
    else:
        val =float(0)
    pathnames=[]
    
    
    if not paths[end] ==None:
        for ward in paths[end]:
            pathnames+=[installations[ward]]
    else:
        pathnames=None
    
    return (val, pathnames)
    
        
            
