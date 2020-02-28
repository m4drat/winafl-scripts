from config_loader import load_config

import subprocess
import sys

def run_cmin(args : dict):
    cmdline = [
        'py',
        '-2',
        args['W_AFL_HOME'] + 'winafl-cmin.py',
        '-D',
        args['D_RIO_HOME'] + f'bin{args["ARCH"]}\\',
        '-i',
        args['AFL_CMIN']['INP_DIR'],
        '-o',
        args['AFL_CMIN']['MIN_DIR'],
        '-t',
        args['AFL_CMIN']['TIMEOUT'],
        '-target_module',
        args['AFL_CMIN']['TARGET_MODULE'],
        '-coverage_module',
        args['AFL_CMIN']['COVERAGE_MODULE'],
        '-target_offset',
        hex(int(args['AFL_CMIN']['TARGET_OFFSET'], 16)),
        '-nargs',
        args['AFL_CMIN']['NARGS'],
        '-call_convention',
        args['AFL_CMIN']['CALL_CONVENTION'],
        '-covtype',
        args['AFL_CMIN']['COVTYPE'],
        '--',
        ' '.join(args['FUZZ']['TARGET_CMD'])
    ]

    print(' '.join(cmdline))

    subprocess.run(
        cmdline,
        cwd=args['W_AFL_HOME'] + f'bin{args["ARCH"]}'
    )

def main():
    if len(sys.argv) > 1:
        args = load_config(sys.argv[1])

        if args == None:
            exit(1)

        run_cmin(args)
    else:
        print(f'Usage: {sys.argv[0]} <config_file>')

if __name__ == "__main__":
    main()