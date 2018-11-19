import json
import os

# cwd = os.getcwd()
cwd = '/home/phd/Projects/Github/InteractivePolyomino'
filename = '/configure.cfg'

print(cwd + filename)

configure = dict()

configure['ngenes'] = 2
configure['generate_colours'] = 7
configure['metric_colours'] = 9


configure['builds'] = 40
configure['n_jiggle'] = 3
configure['threshold'] = 0.25
configure['n_samples'] = 10
configure['iso'] = True
configure['dup_aware'] = False

json.



# # Execution, only one option is executed
# simple = false
# distribution = false
#
# # IO options
# file_path = /rscratch/vatj2/public_html/Polyominoes/data/gpmap/V8/interactive/
# out_genome_file = SampledGenotypes
# in_genome_file = SampledGenotypes
# duplicate_genome_file = DuplicateSampledGenotypes
# out_phenotype_file = PhenotypeTables/PhenotypeTable
# in_phenotype_file = PhenotypeTable
# set_file = SetTable
# preprocess_file = PreProcessGenotypes
# set_metric_file = SetMetrics
# genome_metric_file = GenomeMetrics
# neighbour_file = Neighbourhood
#
# # Hidden options
# preprocess_builds = 250
# allow_duplicates = true
# steric_forbidden = false
