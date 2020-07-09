from config_loader import load_config
from pathlib import Path

import subprocess
import threading
import argparse
import pathlib
import queue
import sys

def run_drrun(tasks : queue.Queue, worker_id : int, args : dict):
    while True:
        params = tasks.get()
        inp_file = params['input']

        print(f'Worker: {worker_id} processing file: {inp_file}')

        cmdline = [
            args['D_RIO_HOME'] + f'bin{args["ARCH"]}\\drrun.exe',
            '-t',
            'drcov',
            '--',
            args['COVERAGE']['TARGET_APP'],
            inp_file
        ]
        
        sp = subprocess.Popen(
            cmdline,
            # stdout=subprocess.PIPE, 
            # stderr=subprocess.PIPE,
            cwd=args['COVERAGE']['OUT_DIR']
        )
        sp.wait()

        tasks.task_done()

def main():
    if len(sys.argv) > 1:
        args = load_config(sys.argv[1])

        if args == None:
            exit(1)

        out_dir_path = Path(args['COVERAGE']['OUT_DIR'])
        if not out_dir_path.exists():
            print('Out dir doesnt exist. Creating new!')
            out_dir_path.mkdir(parents=True, exist_ok=True)

        tasks = queue.Queue()

        for worker_id in range(args['COVERAGE']['WORKERS']):
            worker = threading.Thread(target=run_drrun, args=(tasks, worker_id, args))
            worker.setDaemon(True)
            worker.start()

        for f_path in Path(args['COVERAGE']['INP_DIR']).iterdir():
            tasks.put({'input': f_path.as_posix()})

        tasks.join()
    else:
        print(f'Usage: {sys.argv[0]} <config_file>')

if __name__ == '__main__':
    main()