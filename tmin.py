from pathlib import Path
from typing import List

import subprocess
import threading
import queue
import sys

TARGET = 0x24620 # 0x40C2D0 # 0x40C680

D_RIO_HOME = 'Z:\\DynamoRIO-Windows-7.1.0-1\\'
W_AFL_HOME = 'Z:\\winafl\\'
BASE_DIR   = 'Z:\\fuzz\\'
APP = 'CFF_Explorer_hash_calc_patched.exe'

INP_DIR = BASE_DIR + 'testcases\\minset\\'
MIN_DIR = BASE_DIR + 'testcases\\minimised\\'

WORKERS = 4

ARCH = '32' # can be 32 or 64

EXCLUDE : List[str] = []

def tmin_runner(q : queue.Queue, worker_id : int):
    while True:
        params = q.get()
        inp_file = params['inp_file']
        out_file = params['out_file']

        print(f'Worker: {worker_id} processing file: {inp_file}')

        cmdline = [
            W_AFL_HOME + f'bin{ARCH}\\afl-tmin.exe',
            '-D',
            D_RIO_HOME + f'bin{ARCH}',
            '-i',
            inp_file,
            '-o',
            out_file,
            '-t',
            '15000',
            '--',
            '-target_module',
            APP,
            '-target_offset',
            hex(TARGET),
            '-nargs',
            '1',
            '-call_convention',
            'thiscall',
            '-coverage_module',
            APP,
            '-covtype',
            'edge',
            '--',
            BASE_DIR + APP,
            '@@'
        ]

        sp = subprocess.Popen(
            cmdline,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            cwd=W_AFL_HOME + f'bin{ARCH}\\'
        )
        sp.wait()

        q.task_done()

def main():
    out_dir_path = Path(MIN_DIR)
    if not out_dir_path.exists():
        print('Out dir doesnt exist. Creating new!')
        out_dir_path.mkdir(parents=True, exist_ok=True)

    q = queue.Queue()

    for worker_id in range(WORKERS):
        worker = threading.Thread(tmin_runner, args=(q, worker_id))
        worker.setDaemon(True)
        worker.start()

    for f_path in Path(INP_DIR).iterdir():
        if not f_path.name in EXCLUDE:
            q.put({'inp_file': f_path.as_posix(), 'out_file': MIN_DIR + f_path.name})

    q.join()

if __name__ == "__main__":
    main()