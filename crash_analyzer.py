from config_loader import load_config

import subprocess
import threading
import argparse
import pathlib
import queue
import sys

def run_bugid(tasks : queue.Queue, worker_id : int, args : dict):
    while True:
        params = tasks.get()
        crash_path  = params['crash_path']
        reports_dir = params['reports_dir']
        current     = params['current']
        total       = params['total']
        delete      = params['delete']

        print(f'({worker_id}) Processing: "{crash_path}". ({current}/{total})')

        cmdline = [
            args['CRASH_ANALYZER']['BUGID_DIR'] + 'BugId.cmd',
            ' '.join(args['CRASH_ANALYZER']['ADDITIONAL_CMD']),
            args['CRASH_ANALYZER']['TARGET_APP'],
            '--',
            crash_path
        ]

        sp = subprocess.Popen(
            cmdline,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            cwd=reports_dir
        )
        sp.wait()

        # no crash was detected
        if sp.returncode == 0 and delete:
            crash_path.unlink()

        tasks.task_done()

def main():
    if len(sys.argv) > 1:
        args = load_config(sys.argv[1])

        if args == None:
            exit(1)

        crashes_dir = pathlib.Path(args['CRASH_ANALYZER']['INP_DIR'])
        reports_dir = pathlib.Path(args['CRASH_ANALYZER']['REPORTS_DIR'])

        if not crashes_dir.exists():
            print('Crashes directory doesnt exist! Check if file path is correct!')
            exit(1)

        if not reports_dir.exists():
            print('Out directory doesnt exist! Creating new one.')
            reports_dir.mkdir(parents=True, exist_ok=True)

        tasks = queue.Queue()

        for worker_id in range( args['CRASH_ANALYZER']['WORKERS']):
            worker = threading.Thread(target=run_bugid, args=(tasks, worker_id, args))
            worker.setDaemon(True)
            worker.start()

        crash_samples = list(crashes_dir.iterdir())
        current = 0
        total   = len(crash_samples)

        for crash_path in crash_samples:
            tasks.put(
                {
                    'crash_path'  : crash_path.absolute().as_posix(),
                    'reports_dir' : reports_dir.absolute().as_posix(),
                    'current'     : current,
                    'total'       : total,
                    'delete'      : args['CRASH_ANALYZER']['DELETE_NON_CRASHING']
                }
            )
            current += 1

        tasks.join()
    else:
        print(f'Usage: {sys.argv[0]} <config_file>')


if __name__ == "__main__":
    main()