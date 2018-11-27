
# coding: utf-8

# In[1]:


import os


# In[2]:


# cwd = os.getcwd()
cwd = '/rscratch/vatj2/cloud/PolyominoDash/InteractivePolyomino'
filename = '/configuration.cfg'


# In[3]:


# print(cwd + filename)


# In[4]:


parameters = dict()


# In[5]:


main = dict()

main['n_genes'] = 2
main['generate_colours'] = 7
main['metric_colours'] = 9
main['builds'] = 40
main['n_jiggle'] = 3
main['threshold'] = 25
main['n_samples'] = 10
main['iso'] = False
main['dup_aware'] = False


# In[6]:


execute = dict()

execute['simple'] = True
execute['distribution'] = False


# In[7]:


io = dict()

io['file_path'] = '/rscratch/vatj2/public_html/Polyominoes/data/gpmap/V8/test/'
io['out_genome_file'] = 'SampledGenotypes'
io['in_genome_file'] = 'SampledGenotypes'
io['duplicate_genome_file'] = 'DuplicateSampledGenotypes'
io['out_phenotype_file'] = 'PhenotypeTables/PhenotypeTable'
io['in_phenotype_file'] = 'PhenotypeTable'
io['set_file'] = 'SetTable'
io['preprocess_file'] = 'PreProcessGenotypes'
io['set_metric_file'] = 'SetMetrics'
io['genome_metric_file'] = 'GenomeMetrics'
io['neighbour_file'] = 'Neighbourhood'


# In[8]:


hidden = dict()

hidden['preprocess_builds'] = 250
hidden['allow_duplicates'] = True
hidden['steric_forbidden'] = False


# In[9]:


parameters['main'] = main
parameters['execute'] = execute
parameters['io'] = io
parameters['hidden'] = hidden


# In[10]:


def write_config(parameters, file):
    with open(file, 'w') as f:
        f.write('# Main Options\n')
        for key, value in parameters['main'].items():
            if key == 'threshold':
                f.write(''.join([key, ' = ', str(round(value/100, 2)), '\n']))
            else:
                f.write(''.join([key, ' = ', str(value), '\n']))
        f.write('\n# Execution, only one option is executed\n')
        for key, value in parameters['execute'].items():
            f.write(''.join([key, ' = ', str(value), '\n']))
        f.write('\n# IO Options\n')
        for key, value in parameters['io'].items():
            f.write(''.join([key, ' = ', str(value), '\n']))
        f.write('\n# Hidden options\n')
        for key, value in parameters['hidden'].items():
            f.write(''.join([key, ' = ', str(value), '\n']))

