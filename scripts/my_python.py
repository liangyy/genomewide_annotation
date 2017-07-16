import subprocess
import h5py

def get_number_of_lines(filename):
    cmd = 'cat ' + filename + ' | wc -l'
    result = subprocess.check_output(cmd, shell=True)
    nrow = int(result.decode().split('\n')[0])
    return nrow

def read_hdf5_by_name(filename, name):
    f_scores = h5py.File(filename, 'r')
    scores = f_scores[name][()]
    f_scores.close()
    return scores
