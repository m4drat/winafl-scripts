import subprocess
import threading
import argparse
import pathlib
import queue

D_RIO_HOME = 'C:\\Users\\madrat\\Desktop\\RE\\DynamoRIO-Windows-7.91.18278-0\\'
BASE_DIR   = 'C:\\Users\\madrat\\Desktop\\fuzz\\'
APP = 'CFF_Explorer_check_patched.exe'

INP_DIR = BASE_DIR + 'testcases\\minset\\'
OUT_DIR = BASE_DIR + 'out\\'

ARCH = '32' # can be 32 or 64

def run_drrun(q : queue.Queue, worker_id : int):
    while True:
        params = q.get()

        cmdline = [
            D_RIO_HOME + f'bin{ARCH}\\drrun.exe',
            '-s', # timeout
            '6',  
            '-t', # module to use
            'drcov',
            '--',
            BASE_DIR + APP,
            fname
        ]
        
        sp = subprocess.Popen(
            cmdline,
            # stdout=subprocess.PIPE, 
            # stderr=subprocess.PIPE,
            cwd=OUT_DIR
        )
        sp.wait()

        q.task_done()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_dir',  dest='inp',   help='fuzzers sync dir')
    parser.add_argument('-o', '--out_dir',    dest='out',   help='output dir')
    args = parser.parse_args() 

    tasks = queue.Queue()

if __name__ == '__main__':
    main()