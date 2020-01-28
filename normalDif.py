import networkx as nx
import read_graph as rg
import sys
import numpy as np

def normalDif(filename,infected_node_file):
    g=rg.create_undirected_graph_IC(filename)
    infected_set=rg.read_infected_node(infected_node_file)
    mi=float('inf')
    ma=float('-inf')
    for u,v,d in g.edges(data=True):
        mi=min(mi,d['weight'])
        ma=max(ma,d['weight'])
    for u,v,d in g.edges(data=True):
        #m=float()
        #print (d['weight'])
        if (ma-mi!=0):
            d['weight']=(d['weight']-mi)/(ma-mi)

    total_inf=0
    infList=[]
    while (infected_set):
        newInf=[]

        for i in infected_set:
            if (i not in g.nodes()):
                continue
            for j in g.successors(i):
                # if (j not in g.nodes()):
                #     continue
                rdm=round(np.random.uniform(0,.1) ,13)
                if (rdm<=g[i][j]['weight']):
                    if (j not in newInf):
                        newInf.append(j)
        total_inf+=len(newInf)
        infList.append(total_inf)

        for i in infected_set:
            if i in g.nodes():
                g.remove_node(i)

        infected_set=newInf
    import csv
    with open('normExt.csv','w') as f:
        writer=csv.writer(f)
        writer.writerow(infList)


def main():
    filename=sys.argv[1]
    infected_node_file=sys.argv[2]

    #K=int(sys.argv[3])

    normalDif(filename,infected_node_file)

if __name__=='__main__':
    main()
