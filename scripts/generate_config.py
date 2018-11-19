
# coding: utf-8

# In[1]:


import os


# In[2]:


# cwd = os.getcwd()
cwd = '/rscratch/vatj2/cloud/PolyominoDash/InteractivePolyomino'
filename = '/configure.cfg'


# In[3]:


# print(cwd + filename)


# In[4]:


parameters = dict()

parameters['ngenes'] = 2
parameters['generate_colours'] = 7
parameters['metric_colours'] = 9


parameters['builds'] = 40
parameters['n_jiggle'] = 3
parameters['threshold'] = 0.25
parameters['n_samples'] = 10
parameters['iso'] = True
parameters['dup_aware'] = False


# In[5]:


execute_parameters = dict()

execute_parameters['simple'] = True
execute_parameters['distribution'] = False


# In[6]:


io_parameters = dict()

io_parameters['file_path'] = '/rscratch/vatj2/public_html/Polyominoes/data/gpmap/V8/interactive/'
io_parameters['out_genome_file'] = 'SampledGenotypes'
io_parameters['in_genome_file'] = 'SampledGenotypes'
io_parameters['duplicate_genome_file'] = 'DuplicateSampledGenotypes'
io_parameters['out_phenotype_file'] = 'PhenotypeTables/PhenotypeTable'
io_parameters['in_phenotype_file'] = 'PhenotypeTable'
io_parameters['set_file'] = 'SetTable'
io_parameters['preprocess_file'] = 'PreProcessGenotypes'
io_parameters['set_metric_file'] = 'SetMetrics'
io_parameters['genome_metric_file'] = 'GenomeMetrics'
io_parameters['neighbour_file'] = 'Neighbourhood'


# In[7]:


hidden_parameters = dict()

hidden_parameters['preprocess_build'] = 250
hidden_parameters['allow_duplicates'] = True
hidden_parameters['steric_forbidden'] = False


# In[8]:


with open(cwd+filename, 'w') as f:
    f.write('# Main Options\n')
    for key, value in parameters.items():
        f.write(''.join([key, ' = ', str(value), '\n']))
    f.write('\n')


# In[9]:


with open(cwd+filename, 'a') as f:
    f.write('# Execution, only one option is executed\n')
    for key, value in execute_parameters.items():
        f.write(''.join([key, ' = ', str(value), '\n']))
    f.write('\n')


# In[10]:


with open(cwd+filename, 'a') as f:
    f.write('# IO Options\n')
    for key, value in io_parameters.items():
        f.write(''.join([key, ' = ', str(value), '\n']))
    f.write('\n')


# In[11]:


with open(cwd+filename, 'a') as f:
    f.write('# Hidden options\n')
    for key, value in hidden_parameters.items():
        f.write(''.join([key, ' = ', str(value), '\n']))

