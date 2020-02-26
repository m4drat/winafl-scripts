import subprocess
import threading
import time
import sys

TARGET = 0x24620 # 0x6DF0: 3

D_RIO_HOME = 'C:\\Users\\madrat\\Desktop\\RE\\DynamoRIO-Windows-7.91.18278-0\\'
W_AFL_HOME = 'C:\\Users\\madrat\\Desktop\\RE\\winafl\\'
BASE_DIR   = 'C:\\Users\\madrat\\Desktop\\fuzz\\'
APP = 'CFF_Explorer_check_patched.exe'

INP_DIR = BASE_DIR + 'testcases\\minset\\'
OUT_DIR = BASE_DIR + 'out\\'

# debug run:
# Z:\DynamoRIO-Windows-7.1.0-1\bin32\drrun.exe -c Z:\winafl\bin32\winafl.dll -debug -coverage_module CFF_Explorer.exe -target_module CFF_Explorer.exe -target_offset 0x6df0 -nargs 3 -call_convention thiscall -- CFF_Explorer.exe Z:\fuzz\testcases\pe_small\tinydll.dll

# WORKERS = 4

ARCH = '32' # can be 32 or 64

def spawn_fuzzer(worker : int, is_master : bool):
    cmdline = [
        W_AFL_HOME + f'bin{ARCH}\\afl-fuzz.exe',
        '-D',
        D_RIO_HOME + f'bin{ARCH}',
        '-i',
        '-', # INP_DIR,
        '-o',
        OUT_DIR,
        '-M' if is_master else '-S',
        f'fuzzer_{worker}',
        '-t',
        '3000',
        '-I',
        '15000+',
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
        '-fuzz_iterations',
        '5000',
        '--',
        BASE_DIR + APP,
        '@@'
    ]

    print('[+] Fuzzer commad-line: ' + ' '.join(cmdline))

    while True:
        try:
            sp = subprocess.Popen(
                cmdline,
                # stdout=subprocess.PIPE, 
                # stderr=subprocess.PIPE,
                cwd=W_AFL_HOME + f'bin{ARCH}\\'
            )
            sp.wait()
        except:
            print(f'[-] fuzzer_{worker} died! Restarting instance!')

        cmdline[cmdline.index('-i') + 1] = '-'

        print(f'Restarting fuzzer with new cmdline: {" ".join(cmdline)}')

        time.sleep(2)
        
def main():
    # print(f'[+] Spawning {WORKERS} fuzzers!')
    if len(sys.argv) > 1:
        worker = int(sys.argv[1])
        # for worker in range(0, WORKERS):
        threading.Timer(0.0, spawn_fuzzer, args=[worker, True if worker == 0 else False]).start()

        if worker == 0:
            time.sleep(5.0)

        # while threading.active_count() > 1:
        #     time.sleep(5.0)

        #     try:
        #         subprocess.check_call(['py', '-3', W_AFL_HOME + 'winafl-whatsup.py', "-s", OUT_DIR])
        #     except:
        #         pass
    else:
        print(f'Usage: {sys.argv[0]} <fuzzer_id>')

if __name__ == "__main__":
    main()