
# coding: utf-8

# In[15]:


import pandas as pd


# In[177]:


get_ipython().magic('matplotlib inline')


# In[32]:


address = 'http://files.tcm.phy.cam.ac.uk/~vatj2/Polyominoes/data/gpmap/V8/interactive/'

df = pd.read_csv(address + 'GenomeMetrics_N2_C7_T25_B40_Cx9_J3.txt', sep=' ')
dfn = pd.read_csv(address + 'Neighbourhood_N2_C7_T25_B40_Cx9_J3.txt', sep=' ', names=['genome', 'pIDs'], index_col=False)


# In[ ]:


def neighbourhood_reshape(df, dfn, n_genes, colours):
    neighbours = 4 * n_genes * (colours - 1)
    columns = pd.MultiIndex.from_product([df['genome'].tolist(), ['genome', 'pIDs']], names=['original', 'neighbour'])
    
    new_df = pd.DataFrame(index=pd.Series(range(0, neighbours)), columns=columns)
    
    for genome, index in zip(df['genome'], range(0, len(df['genome']))):
        new_df.T.loc[(genome, 'genome'), :] = dfn[(index * neighbours):((index + 1) * neighbours)]['genome'].values
        new_df.T.loc[(genome, 'pIDs'), :] = dfn[(index * neighbours):((index + 1) * neighbours)]['genome'].values

    return new_df


# In[155]:


new_df = neighbourhood_reshape(df, dfn, 2, 9)


# In[178]:


new_df.loc[slice(None),('(0,0,0,1,0,0,0,2)','pIDs')].hist()

