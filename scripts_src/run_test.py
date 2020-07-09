from config_loader import load_config

import subprocess
import threading
import time
import sys

def run_dbg(args):
    cmdline = [
        args['D_RIO_HOME'] + f'bin{args["ARCH"]}\\drrun.exe',
        '-c',
        args['W_AFL_HOME'] + f'bin{args["ARCH"]}\\winafl.dll',
        '-debug',
        *args['RUN_TEST']['D_RIO_OPTIONS'],
        '--',
        *args['RUN_TEST']['TARGET_CMD'],
    ]

    print('Cmdline: ' + ' '.join(cmdline))

    sp = subprocess.Popen(
        cmdline,
        # stdout=subprocess.PIPE, 
        # stderr=subprocess.PIPE,
        cwd=args['RUN_TEST']['OUT_DIR']
    )
    sp.wait()
        
def main():
    if len(sys.argv) > 1:
        args = load_config(sys.argv[1])

        if args == None:
            exit(1)

        run_dbg(args)
    else:
        print(f'Usage: {sys.argv[0]} <config_file>')

if __name__ == "__main__":
    main()