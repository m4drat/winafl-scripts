from config_loader import load_config
from pathlib import Path
from typing import List

import subprocess
import threading
import queue
import json
import sys

def tmin_runner(q : queue.Queue, worker_id : int, args : dict):
    while True:
        params = q.get()
        inp_file = params['inp_file']
        out_file = params['out_file']

        print(f'({worker_id}) Processing file: {inp_file}')

        cmdline = [
            args['W_AFL_HOME'] + f'bin{args["ARCH"]}\\afl-tmin.exe',
            '-D',
            args['D_RIO_HOME'] + f'bin{args["ARCH"]}',
            '-i',
            inp_file,
            '-o',
            out_file,
            '-t',
            args['AFL_TMIN']['TIMEOUT'],
            '--',
            '-target_module',
            args['AFL_TMIN']['TARGET_MODULE'],
            '-coverage_module',
            args['AFL_TMIN']['COVERAGE_MODULE'],
            '-target_offset',
            hex(int(args['AFL_TMIN']['TARGET_OFFSET'], 16)),
            '-nargs',
            args['AFL_TMIN']['NARGS'],
            '-call_convention',
            args['AFL_TMIN']['CALL_CONVENTION'],
            '-covtype',
            args['AFL_TMIN']['COVTYPE'],
            '--',
            ' '.join(args['FUZZ']['TARGET_CMD'])
        ]

        try:
            sp = subprocess.Popen(
                cmdline,
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                cwd=args['W_AFL_HOME'] + f'bin{args["ARCH"]}\\'
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
    if len(sys.argv) > 1:
        args = load_config(sys.argv[1])

        if args == None:
            exit(1)

        out_dir_path = Path(args['AFL_TMIN']['MIN_DIR'])
        if not out_dir_path.exists():
            print('Out dir doesnt exist. Creating new!')
            out_dir_path.mkdir(parents=True, exist_ok=True)

        q = queue.Queue()

        for worker_id in range(args['AFL_TMIN']['WORKERS']):
            worker = threading.Thread(target=tmin_runner, args=(q, worker_id, args))
            worker.setDaemon(True)
            worker.start()

        for f_path in Path(args['AFL_TMIN']['INP_DIR']).iterdir():
            if not f_path.name in args['AFL_TMIN']['EXCLUDE']:
                q.put({'inp_file': f_path.as_posix(), 'out_file': args['AFL_TMIN']['MIN_DIR'] + f_path.name})

        q.join()
    else:
        print(f'Usage: {sys.argv[0]} <config_file>')

if __name__ == "__main__":
    main()