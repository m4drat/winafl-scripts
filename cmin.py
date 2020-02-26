import subprocess
import sys

TARGET = 0x24620 # 0x40C2D0 # 0x40C680

D_RIO_HOME = 'C:\\Users\\madrat\\Desktop\\RE\\DynamoRIO-Windows-7.91.18278-0\\'
W_AFL_HOME = 'C:\\Users\\madrat\\Desktop\\RE\\winafl\\'
BASE_DIR   = 'C:\\Users\\madrat\\Desktop\\fuzz\\'
APP = 'CFF_Explorer_check_patched.exe'

def main():
    cmdline = [
        'py',
        '-2',
        W_AFL_HOME + 'winafl-cmin.py',
        '-D',
        D_RIO_HOME + 'bin32',
        '-i',
        BASE_DIR + 'testcases\\favourite',
        '-o',
        BASE_DIR + 'testcases\\minset',
        '-t',
        '100000',
        '-covtype',
        'edge',
        '-coverage_module',
        APP,
        '-target_module',
        APP,
        '-target_offset',
        hex(TARGET),
        '-nargs',
        '1',
        '-call_convention',
        'thiscall',
        '--',
        BASE_DIR + APP,
        '@@'
    ]

    print(' '.join(cmdline))

    subprocess.run(
        cmdline,
        cwd=W_AFL_HOME + 'bin32'
    )

if __name__ == "__main__":
    main()