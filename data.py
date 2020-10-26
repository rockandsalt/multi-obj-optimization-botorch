from os import path 
import pandas as pd 
import numpy as np

F_PATH = path.join('.','data')

def load_data():
    doe = pd.read_excel(path.join(F_PATH, 'doe_lhsmu_locked.xlsx'),
                    header = 0, usecols = 'A:J')

    sample_dimension = pd.read_excel(path.join(F_PATH, 'process_map_data.xlsx'),
                                 header = 0, usecols = 'A:E')
    
    archimedes = pd.read_excel(path.join(F_PATH, 'process_map_data_archimedes.xlsx'),
                                 header = 0, usecols = 'A:F')
    
    arch_iso = pd.read_excel(path.join(F_PATH, 'process_map_data_archimedes.xlsx'), sheet_name = 'Run', header = 0, usecols='A,D')
    arch_iso = arch_iso.groupby(by = ['run']).mean().reset_index()

    mean_archimedes = archimedes.groupby(by = ['batch','id']).mean()
    mean_archimedes = mean_archimedes.merge(arch_iso, on = 'run', right_index = True)

    sample_dimension['x_dev'] = np.abs(sample_dimension['x'] - 20)
    sample_dimension['y_dev'] = np.abs(sample_dimension['y'] - 15)
    sample_dimension['z_dev'] = np.abs(sample_dimension['z'] - 10)

    max_dev = sample_dimension.groupby(by = ['batch','id']).max()
    max_dev = max_dev.drop(['x','y','z'], axis = 1)

    ss316 = 8000

    porosity = (1.0 - mean_archimedes['dry weight']/
                (mean_archimedes['soaked weight']-mean_archimedes['immersed weight'])*mean_archimedes['Isoden']/ss316)*100
                
    porosity = pd.DataFrame(porosity, columns=['porosity'])
    process_results = doe.merge(porosity, how='left', on='batch').dropna()

    dimension_res = doe.merge(max_dev, how='left', on='batch').dropna()

    return doe, process_results, dimension_res

def load_time():
    doe = pd.read_excel(path.join(F_PATH, 'doe_lhsmu_locked.xlsx'),
                    header = 0, usecols = 'A:J')
    df_time = pd.read_excel(path.join(F_PATH, 'printing_time.xlsx'),header = 0)
    print_time = doe.merge(df_time, how='left', on='batch')
    return print_time