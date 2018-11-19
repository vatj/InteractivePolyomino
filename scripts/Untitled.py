
# coding: utf-8

# In[15]:


import pandas as pd

df = pd.read_csv('http://files.tcm.phy.cam.ac.uk/~vatj2/Polyominoes/data/gpmap/V8/interactive/' + 'Neighbourhood_N2_C7_T25_B40_Cx9_J3.txt', sep=' ', names=['genomes', 'pIDs'], index_col=False)


# In[16]:


def neighbourhood_reshape(df, n_genes, colours):
    neighbours = 4 * n_genes * (colours - 1)
    new_df = pd.DataFrame()
    
    for index in range(1, (len(df) // neighbours) + 1):
        new_df['genomes' + str(index)] = pd.Series()
        new_df['pIDs' + str(index)] = pd.Series()
        
    return new_df


# In[17]:


new_df = neighbourhood_reshape(df, 2, 9)


# In[18]:


new_df

