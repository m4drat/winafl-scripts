from config_loader import load_config

import argparse
import pathlib
import shutil
import sys

def main():
    if len(sys.argv) > 1:
        args = load_config(sys.argv[1])

        if args == None:
            exit(1)

        sync_path = pathlib.Path(args['COLLECT']['FUZZER_SYNC_DIR'])
        out_dir_path = pathlib.Path(args['COLLECT']['OUT_DIR'])

        crashes_dir = out_dir_path / 'crashes'
        hangs_dir = out_dir_path / 'hangs'

        if not crashes_dir.exists() or not hangs_dir.exists():
            print('Out directory doesnt exist! Creating new one.')
            crashes_dir.mkdir(parents=True, exist_ok=True)
            hangs_dir.mkdir(parents=True, exist_ok=True)
        
        crashes = 0
        hangs   = 0
        per_fuzzer_stats = {} # {'fuzzer0':(crashes, hangs)}
        for fuzzer_path in sync_path.iterdir():
            if fuzzer_path.is_dir():
                for fuzzer_data in fuzzer_path.iterdir():
                    if 'crashes' in fuzzer_data.name and fuzzer_data.is_dir():
                        for crash_path in fuzzer_data.iterdir():
                            if not 'README' in crash_path.name:
                                copy_from = crash_path.as_posix()
                                copy_to   = (crashes_dir).as_posix() + '/' + crash_path.name + '_' + str(crashes)
                                if args['COLLECT']['VERBOSITY']:
                                    print('Crash path:   ' + copy_from)
                                    print('Copy to path: ' + copy_to)
                                if not args['COLLECT']['JUST_GET_STATS']:
                                    shutil.copy(copy_from, copy_to)
                                crashes += 1
                                if not fuzzer_path.name in per_fuzzer_stats.keys():
                                    per_fuzzer_stats[fuzzer_path.name] = [0, 0]
                                else:
                                    per_fuzzer_stats[fuzzer_path.name][0] += 1
                    if 'hangs' in fuzzer_data.name and fuzzer_data.is_dir():
                        for hangs_path in fuzzer_data.iterdir():
                            if not 'README' in hangs_path.name: 
                                copy_from = hangs_path.as_posix()
                                copy_to   = (hangs_dir).as_posix() + '/' + hangs_path.name + '_' + str(hangs)
                                if args['COLLECT']['VERBOSITY']:
                                    print('Crash path:   ' + copy_from)
                                    print('Copy to path: ' + copy_to)
                                if not args['COLLECT']['JUST_GET_STATS']:
                                    shutil.copy(copy_from, copy_to)
                                hangs += 1
                                if not fuzzer_path.name in per_fuzzer_stats.keys():
                                    per_fuzzer_stats[fuzzer_path.name] = [0, 0]
                                else:
                                    per_fuzzer_stats[fuzzer_path.name][1] += 1
        
        print(f'Total collected:')
        print(f'\tCrashes: {crashes}')
        print(f'\tHangs:   {hangs}')
        print(f'Per-fuzzer stats:')
        for k, v in per_fuzzer_stats.items():
            print(f'\tFuzzer: {k}. Crashes: {v[0]}. Hangs: {v[1]}.')
    else:
        print(f'Usage: {sys.argv[0]} <config_file>')

if __name__ == "__main__":
    main()