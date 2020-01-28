import heapq
import networkx as nx
import read_graph as rg
import sys
import math
import time
import numpy as np

i=0

def merge_infected_node(G,Iset):
    I='0'

    G.add_node(I)
    G1=G.copy()
    #print(G.edges())
    for node in Iset:
        #print(node)
        for nbr in G.successors(node):
            #print(node,nbr)
            w=G[node][nbr]['weight']
            if G1.has_edge(I,nbr)==False:
                G1.add_edge(I,nbr,weight=w)
            else:
                temp=G1[I][nbr]['weight']
                G1[I][nbr]['weight']=temp+(1-temp)*w
    #remove nodes
    G=G1
    for node in Iset:
        if node in G:
            G.remove_node(node)
    G1=G
    if G1.has_edge(I,I):
        G1.remove_edge(I,I)
    #print(I)
    return [G1,I]

def get_dominator_tree(g,I):
    g1=nx.DiGraph()
    #print(2)
    # with open('users.csv','w') as f:
    #     for e in g.edges():
    #         f.write(str(e)+'\n')
    mi=float('inf')
    ma=float('-inf')
    # for i in g.nodes():
    #     f=0
    #     for (j,k) in nx.immediate_dominators(g,I).items():
    #         if (i==j):
    #             f=1
    #             break
    #     if (f==0):
    #         print(i)
    #print(len(nx.immediate_dominators(g,I).items()))
    for (i,j) in nx.immediate_dominators(g,I).items():
        #print(i,j)
        if (i==j):
            #print(i)
            continue;
        #if (j==0)
        if (j,i) in g.edges:
            wt=g[j][i]['weight']
        else:
            s=0
            #print(len(nx.all_simple_paths(g, source=j, target=i)))
            for path in nx.all_shortest_paths(g, source=j, target=i):
                #s+=1
                p=1
                for x in range(len(path)-1):
                    #print(g[path[x]][path[x+1]]['weight'])
                    p*=g[path[x]][path[x+1]]['weight']
                    #print(x,p)
                s+=p
                #print(s)
            #print(s)
            wt=s
            # if (i=='240649814'):
            #     break
        #     l=list(g.predecessors(i))
        #     print(l)
        # #print(l
        #     s=0.0
        #     for k in l:
        #    # print(k)
        #         print(k,i,j)
        #         s+=(g[k][i]['weight']*g[j][k]['weight'])
        # #print(s)
        #     wt=s
        g1.add_edge(j,i,weight=wt)
        mi=min(mi,wt)
        ma=max(ma,wt)
    m=float('inf')
    f=open('edProb'+str(i)+'.csv','w')
    import csv
    wr=writer=csv.writer(f)
        #print(i,j)
    for u,v,d in g1.edges(data=True):
        #print (d['weight'])
        if (ma-mi!=0):
            d['weight']=(d['weight']-mi)/(ma-mi)
        #print (d['weight'])
        if (d['weight']!=0):
            m=min(m,d['weight'])
        writer.writerow([u,v,d['weight']])

    #print(m)
    return g1
    """domtree=nx.DiGraph()

    num_nodes=len(G)
    dicts={}
    #using graph_tool
    g=Graph()
    vlist=g.new_vertex_property("int")
    elist_weight=g.new_edge_property("double")
    for n,nbrs in G.adjacency_iter():
        for nbr, weight in nbrs.items():
            if str(n) in dicts:
                v1=int(dicts[str(n)])
            else:
                v1=g.add_vertex()
                dicts[str(n)]=str(v1)
                vlist[v1]=n

            if str(nbr) in dicts:
                v2=int(dicts[str(nbr)])
            else:
                v2=g.add_vertex()
                dicts[str(nbr)]=str(v2)
                vlist[v2]=nbr
            log_w=-math.log(weight['weight'])
            edge=g.add_edge(v1,v2)
            elist_weight[edge]=log_w

    #infected node
    I0=int(dicts[str(I)])

    #run shortest path to get weights for dominator tree
    dist=shortest_distance(g,I0,target=None,weights=elist_weight)
    dist_list=dist.a
    #for value in dist_list:
        #print math.exp(-value)


    #get dominator tree
    dom=dominator_tree(g,I0)
    dom_list=dom.a

    for i in range(1,len(dom_list)):
        wei=0
        if g.vertex(dom_list[i])==I0:
            wei=math.exp(-dist_list[g.vertex(i)])
        else:
            wei=math.exp(dist_list[g.vertex(dom_list[i])]-dist_list[g.vertex(i)])
        domtree.add_edge(vlist[g.vertex(dom_list[i])],vlist[g.vertex(i)],weight=(wei))
        #domtree.add_edge(vlist[g.vertex(i)],vlist[g.vertex(dom_list[i])])

    #for n, nbrs in domtree.adjacency_iter():
     #   for nbr in nbrs:
      #      print("%d\t%d" % (n,nbr))
    #printline(domtree)
    return domtree
    """

def compute_nei_footprint(domtree,I):
#get the footprint of I's neighbors
    E_nei={}
    for nei in domtree.successors(I):
        #print nei
        pij=domtree[I][nei]['weight']
        E_nei[str(nei)]=(pij*cal_footprint(domtree,nei))
    return E_nei

def cal_footprint(G,v):
    footprint=1
    if len(G[v])==0:
        footprint=1
    else:
        for nei in G[v]:
            footprint=footprint+cal_footprint(G,nei)*G[v][nei]['weight']

    return footprint


def dava_fast(filename,infected_node_file,K):

    #read graph
    print ("dava_fast begin")
    g=rg.create_undirected_graph_IC(filename)
    #print(type(g))
    G=g
    # for i in G.nodes():
    #     if (not nx.has_path(G,'227653209',i)):
    #         print(i)
    #read infected nodes set
    infected_set=rg.read_infected_node(infected_node_file)
    total_inf=len(infected_set)
    infList=[]

    while (infected_set and G.edges()):
    #start_time=time.time()
    #merge infected node
        [G,I]=merge_infected_node(g,infected_set)
        disconn=[]
        for i in G.nodes():
            if (not nx.has_path(G,I,i)):
                disconn.append(i)
        #print(disconn)
        for i in disconn:
            G.remove_node(i)
        #graphs=list(nx.connected_component_subgraphs(G))
        print(nx.info(G))

        if (not G.edges()):
            break

        #get dominator tree
        domtree=get_dominator_tree(G,I)
        print(nx.info(domtree))

        #get the benefit of I's neighbors
        E_nei=compute_nei_footprint(domtree,I)
        #print (E_nei)

        #select k nodes in dava-fast
        selected_nodes=[]
        selected_nodes=heapq.nlargest(K,E_nei,key=E_nei.get)
        Iset=[]

        for i in domtree.successors(I):
            rdm=round(np.random.uniform(0,.1) ,13)
            if (rdm<=domtree[I][i]['weight']):
                #print(rdm,domtree[I][i]['weight'])
                Iset.append(i)
        #print(len(Iset))
        #infected_set=Iset

        G.remove_node(I)

        for s in selected_nodes:
            G.remove_node(s)
        infected_set=[]

        for i in Iset:
            if i in G.nodes():
                infected_set.append(i)
        total_inf+=len(infected_set)
        infList.append(int(total_inf))
        #f.write(str(total_inf)+',')
        #print(total_inf)
        g=G
        f=open('users.csv','w')
        f.write(str(G.edges()))
    #print(nx.info(G))
    import csv
    with open('davExt.csv','w') as f:
        writer=csv.writer(f)
        writer.writerow(infList)

    # end_time=time.time()
    # cost_time=end_time-start_time
    #return  [selected_nodes, cost_time]

def printline(g):
    print ("edgelist")
    for n, nbrs in g.adjacency_iter():
        for nbr,weight in nbrs.items():
            print("%d,%d,%f" %(n,nbr,weight['weight']))

def main():
    filename=sys.argv[1]
    infected_node_file=sys.argv[2]

    K=int(sys.argv[3])

    dava_fast(filename,infected_node_file,K)


if __name__=='__main__':
    main()
