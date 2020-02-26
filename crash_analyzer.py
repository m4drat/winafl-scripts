import subprocess
import threading
import argparse
import pathlib
import queue
import sys

APP = 'CFF_Explorer_check_patched.exe'
BUGID_DIR = 'C:\\Users\\madrat\\Desktop\\RE\\BugId\\'
BASE_DIR  = 'C:\\Users\\madrat\\Desktop\\fuzz\\'

WORKERS = 8

def run_bugid(tasks : queue.Queue, worker_id : int):
    while True:
        params = tasks.get()
        crash_path  = params['crash_path']
        reports_dir = params['reports_dir']
        current     = params['current']
        total       = params['total']
        delete      = params['delete']

        print(f'({worker_id}) Processing: "{crash_path}". ({current}/{total})')

        cmdline = [
            BUGID_DIR + 'BugId.cmd',
            '--nApplicationMaxRunTimeInSeconds=6',
            '--isa=x86',
            BASE_DIR + APP,
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
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-c', '--crashes_dir', dest='inp',     help='fuzzers sync dir')
    # parser.add_argument('-o', '--out_dir',     dest='out',     help='output dir')
    # parser.add_argument('-d', '--delete',      dest='delete',  help='delete test cases, that didnt lead to crash', default=False)
    # args = parser.parse_args() 

    crashes_dir = pathlib.Path('C:\\Users\\madrat\\Desktop\\fuzz\\fuzzers_results\\crashes\\')
    reports_dir = pathlib.Path('C:\\Users\\madrat\\Desktop\\fuzz\\fuzzers_results\\crash_analysis_results\\')

    if not crashes_dir.exists():
        print('Crashes directory doesnt exist! Check if file path is correct!')
        exit(1)

    if not reports_dir.exists():
        print('Out directory doesnt exist! Creating new one.')
        reports_dir.mkdir(parents=True, exist_ok=True)

    tasks = queue.Queue()

    for worker_id in range(WORKERS):
        worker = threading.Thread(target=run_bugid, args=(tasks, worker_id))
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
                'delete'      : False
            }
        )
        current += 1

    tasks.join()

if __name__ == "__main__":
    main()