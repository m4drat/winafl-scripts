from pathlib import Path

import subprocess
import threading
import argparse
import pathlib
import queue

D_RIO_HOME = 'C:\\Users\\madrat\\Desktop\\RE\\DynamoRIO-Windows-7.91.18278-0\\'
BASE_DIR   = 'C:\\Users\\madrat\\Desktop\\fuzz\\'
APP = 'CFF_Explorer_check_patched.exe'

INP_DIR = BASE_DIR + 'testcases\\minset\\'
OUT_DIR = BASE_DIR + 'testcases\\minset_coverage\\'

WORKERS = 8

ARCH = '32' # can be 32 or 64

def run_drrun(tasks : queue.Queue, worker_id : int):
    while True:
        params = tasks.get()
        inp_file = params['input']

        print(f'Worker: {worker_id} processing file: {inp_file}')

        cmdline = [
            D_RIO_HOME + f'bin{ARCH}\\drrun.exe',
            '-t', # module to use
            'drcov',
            '-dump_binary',
            '--',
            BASE_DIR + APP,
            inp_file
        ]
        
        sp = subprocess.Popen(
            cmdline,
            # stdout=subprocess.PIPE, 
            # stderr=subprocess.PIPE,
            cwd=OUT_DIR
        )
        sp.wait()

        tasks.task_done()

def main():
    global OUT_DIR, INP_DIR
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_dir',  dest='inp',   help='fuzzers sync dir')
    parser.add_argument('-o', '--out_dir',    dest='out',   help='output dir')
    args = parser.parse_args() 

    OUT_DIR = args.out
    INP_DIR = args.inp

    out_dir_path = Path(OUT_DIR)
    if not out_dir_path.exists():
        print('Out dir doesnt exist. Creating new!')
        out_dir_path.mkdir(parents=True, exist_ok=True)

    tasks = queue.Queue()

    for worker_id in range(WORKERS):
        worker = threading.Thread(target=run_drrun, args=(tasks, worker_id))
        worker.setDaemon(True)
        worker.start()

    for f_path in Path(INP_DIR).iterdir():
        tasks.put({'input': f_path.as_posix()})

    tasks.join()

if __name__ == '__main__':
    main()