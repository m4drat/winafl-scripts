import subprocess
import threading
import time
import json
import sys

def load_config(path):
    cfg = open(path).read()
    return json.loads(cfg)

def spawn_fuzzer(worker : int, is_master : bool, args : dict):
    cmdline = [
        args['W_AFL_HOME'] + f'bin{args["ARCH"]}\\afl-fuzz.exe',
        '-D',
        args['D_RIO_HOME'] + f'bin{args["ARCH"]}\\',
        '-i',
        args['FUZZ']['INP_DIR'],
        '-o',
        args['FUZZ']['OUT_DIR'],
        '-M' if is_master else '-S',
        f'fuzzer_{worker}',
        '-t',
        args['FUZZ']['TIMEOUT'],
        '-I',
        '15000+',
        '--',
        '-target_module',
        args['FUZZ']['TARGET_MODULE'],
        '-coverage_module',
        args['FUZZ']['COVERAGE_MODULE'],
        '-target_offset',
        hex(int(args['FUZZ']['TARGET_OFFSET'], 16)),
        '-nargs',
        args['FUZZ']['NARGS'],
        '-call_convention',
        args['FUZZ']['CALL_CONVENTION'],
        '-covtype',
        args['FUZZ']['COVTYPE'],
        '-fuzz_iterations',
        args['FUZZ']['FUZZ_ITER'],
        '--',
        ' '.join(args['FUZZ']['TARGET_CMD'])
    ]

    print('[+] Fuzzer commad-line: ' + ' '.join(cmdline))

    while True:
        try:
            sp = subprocess.Popen(
                cmdline,
                cwd=args['W_AFL_HOME'] + f'bin{args["ARCH"]}\\'
            )
            sp.wait()
        except:
            print(f'[-] fuzzer_{worker} died! Restarting instance!')

        cmdline[cmdline.index('-i') + 1] = '-'
        print(f'Restarting fuzzer with new cmdline: {" ".join(cmdline)}')

        time.sleep(2)
        
def main():
    if len(sys.argv) > 2:
        worker = int(sys.argv[1])
        threading.Timer(0.0, spawn_fuzzer, args=[worker, True if worker == 0 else False, load_config(sys.argv[2])]).start()
    else:
        print(f'Usage: {sys.argv[0]} <fuzzer_id> <config.json>')

if __name__ == "__main__":
    main()