from pathlib import Path
from typing import List

import subprocess
import threading
import queue
import sys

TARGET = 0x24620 # 0x40C2D0 # 0x40C680

D_RIO_HOME = 'C:\\Users\\madrat\\Desktop\\RE\\DynamoRIO-Windows-7.91.18278-0\\'
W_AFL_HOME = 'C:\\Users\\madrat\\Desktop\\RE\\winafl\\'
BASE_DIR   = 'C:\\Users\\madrat\\Desktop\\fuzz\\'
APP = 'CFF_Explorer_check_patched.exe'

INP_DIR = BASE_DIR + 'testcases\\minset\\'
MIN_DIR = BASE_DIR + 'testcases\\minimised\\'

WORKERS = 8

ARCH = '32' # can be 32 or 64

EXCLUDE : List[str] = []

def tmin_runner(q : queue.Queue, worker_id : int):
    while True:
        params = q.get()
        inp_file = params['inp_file']
        out_file = params['out_file']

        print(f'({worker_id}) Processing file: {inp_file}')

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

        try:
            sp = subprocess.Popen(
                cmdline,
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                cwd=W_AFL_HOME + f'bin{ARCH}\\'
            )
            sp.wait()
            if sp.returncode != 0:
                raise Exception()
        except:
            print(f'[-] ({worker_id}) Minimiser returned with non-null code!')
        else:
            print(f'[+] ({worker_id}) File {inp_file} is successfully minimised!')
            q.task_done()
        finally:
            q.task_done()
            q.put(params)

def main():
    out_dir_path = Path(MIN_DIR)
    if not out_dir_path.exists():
        print('Out dir doesnt exist. Creating new!')
        out_dir_path.mkdir(parents=True, exist_ok=True)

    q = queue.Queue()

    for worker_id in range(WORKERS):
        worker = threading.Thread(target=tmin_runner, args=(q, worker_id))
        worker.setDaemon(True)
        worker.start()

    for f_path in Path(INP_DIR).iterdir():
        if not f_path.name in EXCLUDE:
            q.put({'inp_file': f_path.as_posix(), 'out_file': MIN_DIR + f_path.name})

    q.join()

if __name__ == "__main__":
    main()