import subprocess

def get_number_of_lines(filename):
    cmd = 'cat ' + filename + ' | wc -l'
    result = subprocess.check_output(cmd, shell=True)
    nrow = int(result.decode().split('\n')[0])
    return nrow 
