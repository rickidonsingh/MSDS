
# coding: utf-8

# ## Week Three - Part 2 - Network Analysis: 2-Mode Networks:
# ## CUNY MSDS DATA620 - Web Analytics
# ---
# ### Team5: Christopher Estevez, Meaghan Burke, Rickidon Singh,  Ritesh Lohiya, Rose Koh
# ### 06/25/2018 (due date)
# ##### python version: 2.7
# ---
# 
# ## Assignment Description
# 
# Here is a dataset that shows a simple 2-node network:  the attendance of 18 Southern Women at 14 social events:
#    
#    1.Brief Description: http://vlado.fmf.uni-lj.si/pub/networks/data/ucinet/ucidata.htm#davis.   
#     [For more background information, see also:http://rpackages.ianhowson.com/cran/latentnet/man/davis.html].  
#     Small “musty” datasets like that from this 1941 study have proven very valuable in testing and comparing new network 
#     algorithms.
#    
#    2.Dataset: http://vlado.fmf.uni-lj.si/pub/networks/data/Ucinet/davis.dat
#    
#    3.Python code to create dataset: https://networkx.readthedocs.io/en/stable/examples/algorithms/davis_club.html

# **BACKGROUND**
# These data were collected by Davis et al in the 1930s. They represent observed attendance at 14 social events by 18 Southern women. The result is a person-by-event matrix: cell (i,j) is 1 if person i attended social event j, and 0 otherwise. 
# 
# **REFERENCES**
# * Breiger R. (1974). The duality of persons and groups. Social Forces, 53, 181-190. 
# * Davis, A et al. (1941). Deep South. Chicago: University of Chicago Pres

# In[16]:


import matplotlib.pyplot as plt
import networkx as nx
import networkx.algorithms.bipartite as bipartite
import math
import pandas as pd
import scipy as sp
from prettytable import PrettyTable


# In[2]:


G = nx.davis_southern_women_graph()
women = G.graph['top']
clubs = G.graph['bottom']
#print("Biadjacency matrix")
#print(bipartite.biadjacency_matrix(G, women, clubs))
print nx.info(G)


# In[3]:


# project bipartite graph onto women nodes
W = bipartite.projected_graph(G, women)
pd.DataFrame(list(W.degree()),columns=["Member","#Friends"]).sort_values('#Friends', ascending=False)


# In[4]:


# project bipartite graph onto women nodes keeping number of co-occurence
# the degree computed is weighted and counts the total number of shared contacts
W = bipartite.weighted_projected_graph(G, women)
pd.DataFrame(list(W.degree(W, weight='weight')),columns=["Member","#Meetings"]).sort_values('#Meetings', ascending=False)


# In[5]:


plt.figure(figsize=(14, 10))
nx.draw(G,with_labels = True)
plt.show()


# In[6]:


#Women Network and relationship:
plt.figure(figsize=(15,8))
W = bipartite.weighted_projected_graph(G, women, ratio=False)
nx.draw_networkx(W, with_labels=True)


# In[7]:


print(nx.info(W))


# In[8]:


plt.figure(figsize=(15,8))
nx.draw_circular(W, with_labels=True)


# In[9]:


def PTable(graph):
   degree = nx.degree(graph)
   degree_centrality = nx.degree_centrality(graph)
   betweenness_centrality = nx.betweenness_centrality(graph)
   closeness_centrality = nx.closeness_centrality(graph)
   eigenvector_centrality = nx.eigenvector_centrality_numpy(graph)
   
   table = [[name,degree[name], round(degree_centrality[name],3), round(betweenness_centrality[name],3),
             round(closeness_centrality[name],3), round(eigenvector_centrality[name],3)] for name in graph.nodes()]
   table = sorted(table,key = lambda x: -x[2])
   Ptable = PrettyTable(['Subject','Degree','Degree Centrality','Betweenness','Closeness','Eigenvector'])
   
   for i in range(0, len(table)):
       Ptable.add_row(table[i])
   return Ptable


# In[10]:


print((PTable(W)))


# In[11]:


#Clubs Network and relationship:
plt.figure(figsize=(15,8))
C = bipartite.weighted_projected_graph(G, clubs, ratio=False)
nx.draw_networkx(C, with_labels=True)


# In[12]:


print(nx.info(C))


# In[13]:


plt.figure(figsize=(15,8))
nx.draw_circular(C, with_labels=True)


# In[17]:


print((PTable(C)))


# #### Conclusions: 
# Well connected closed network and the degree centrality along with closeness seems to be high. Events E7, E8, E9 have very large attendance when compared to the others. There’s a few strong sub networks between (Laura, Brenda, Theresa, Evelyn) and (Sylvia, Helen, Katherine, Nora). Ruth and Verne aren’t part of the two strong networks, they are considered boundary spanners when compared to other members. As a next step if more information is available on the nodes one can look deeper into why some events are more popular and why a subgroup would attend same events i.e. location of the women.
