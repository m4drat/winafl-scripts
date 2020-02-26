import subprocess
import argparse
import pathlib
import sys

APP = 'CFF_Explorer_check_patched.exe'
BUGID_DIR = 'C:\\Users\\madrat\\Desktop\\RE\\BugId\\'
BASE_DIR  = 'C:\\Users\\madrat\\Desktop\\fuzz\\'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--crashes_dir', dest='inp',     help='fuzzers sync dir')
    parser.add_argument('-o', '--out_dir',     dest='out',     help='output dir')
    parser.add_argument('-d', '--delete',      dest='delete',  help='delete test cases, that didnt lead to crash', default=False)
    args = parser.parse_args() 

    crashes_dir = pathlib.Path(args.inp)
    reports_dir = pathlib.Path(args.out)

    if not reports_dir.exists():
        print('Out directory doesnt exist! Creating new one.')
        reports_dir.mkdir(parents=True, exist_ok=True)

    crash_samples = list(crashes_dir.iterdir())
    current = 0
    total   = len(crash_samples)

    for crash_path in crash_samples:
        print(f'Processing: "{crash_path.as_posix()}". ({current}/{total})')
        cmdline = [
            BUGID_DIR + 'BugId.cmd',
            '--nApplicationMaxRunTimeInSeconds=6',
            '--isa=x86',
            BASE_DIR + APP,
            '--',
            crash_path.absolute().as_posix()
        ]
        sp = subprocess.Popen(
            cmdline,
            # stdout=subprocess.PIPE, 
            # stderr=subprocess.PIPE,
            cwd=reports_dir.absolute().as_posix()
        )
        sp.wait()

        # no crash was detected
        if sp.returncode == 0 and args.delete:
            crash_path.unlink()
        
        current += 1

if __name__ == "__main__":
    main()