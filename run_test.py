import subprocess
import threading
import time
import sys

TARGET = 0x24620 # 0x40C2D0 more_parsers

D_RIO_HOME = 'C:\\Users\\madrat\\Desktop\\RE\\DynamoRIO-Windows-7.91.18278-0\\'
W_AFL_HOME = 'C:\\Users\\madrat\\Desktop\\RE\\winafl\\'
BASE_DIR   = 'C:\\Users\\madrat\\Desktop\\fuzz\\'

INP_DIR = BASE_DIR + 'testcases\\pe_small\\'

# debug run:
# Z:\DynamoRIO-Windows-7.1.0-1\bin32\drrun.exe -c Z:\winafl\bin32\winafl.dll -debug -coverage_module CFF_Explorer.exe -target_module CFF_Explorer.exe -target_offset 0x6df0 -nargs 3 -call_convention thiscall -- CFF_Explorer.exe Z:\fuzz\testcases\pe_small\tinydll.dll

# WORKERS = 4

ARCH = '32' # can be 32 or 64

def run_dbg():
    cmdline = [
        D_RIO_HOME + f'bin{ARCH}\\drrun.exe',
        '-c',
        W_AFL_HOME + f'bin{ARCH}\\winafl.dll',
        '-debug',
        '-coverage_module',
        'CFF_Explorer.exe',
        '-target_module',
        'CFF_Explorer.exe',
        '-target_offset',
        hex(TARGET),
        '-nargs',
        '0',
        '-call_convention',
        'thiscall',
        '--',
        BASE_DIR + 'CFF_Explorer.exe',
        INP_DIR + 'injector.exe'
    ]

    print('Cmdline: ' + ' '.join(cmdline))

    sp = subprocess.Popen(
        cmdline,
        # stdout=subprocess.PIPE, 
        # stderr=subprocess.PIPE,
        cwd=BASE_DIR
    )
    sp.wait()
        
def main():
    run_dbg()

if __name__ == "__main__":
    main()