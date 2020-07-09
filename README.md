# Winafl-scripts

Python scripts, that wraps common utilities like cmin, tmin, etc.

## cmin

config entry: `AFL_CMIN`

- `INP_DIR` - string, path to testcases
- `MIN_DIR` - string, path to directory with minimised samples
- `TIMEOUT` - int, timeout value
- `ADDITIONAL_CMD` - array of strings, additional parameters
- `TARGET_CMD` - arguments for app

## collect

config entry: `COLLECT`

- `FUZZER_SYNC_DIR` - string, path to fuzzers sync directory
- `OUT_DIR` - string, path to directory, where to write all aoutput results
- `JUST_GET_STATS` - bool, if false, will calculate stats, without copying
- `VERBOSITY` - bool, if true, verbosity level is maximum

## coverage

config entry: `COVERAGE`

- `WORKERS` - int, number of threads
- `INP_DIR` - string, path to samples directory
- `OUT_DIR` - string, path to directory with generated coverage files
- `TARGET_APP` - string, path to app

## crash_analyzer

config entry: `CRASH_ANALYZER`

- `WORKERS` - int, amount of threads
- `BUGID_DIR` - string, path to directory with BugId
- `INP_DIR` - string, path to directory with results of fuzzing
- `REPORTS_DIR` - string, path to directory with generated reports
- `DELETE_NON_CRASHING` - bool, delete samples, if they aren't cause crashes
- `ADDITIONAL_CMD` - array of strings, additional parameters
- `TARGET_APP` - string, path to target app

## fuzz

config entry: `FUZZ`

- `INP_DIR` - string, path to directory with samples
- `OUT_DIR` - string, directory, where to write fuzzed samples
- `TIMEOUT` - string, timeout value
- `D_RIO_OPTIONS` - array of strings, options for dynamorio
- `TARGET_CMD` - array of strings, target app command line

## run_test

config entry: `RUN_TEST`

- `OUT_DIR` - string, path to directory with samples to test on
- `D_RIO_OPTIONS` - array of strings, options for dynamorio
- `TARGET_CMD` - array of strings, command line for target app

## tmin

config entry: `AFL_TMIN`

- `WORKERS` - int, number of threads
- `INP_DIR` - string, path to directory with files to minimise
- `MIN_DIR` - string, path to directory, where to write minimised samples
- `TIMEOUT`  - string, timeout value
- `D_RIO_OPTIONS` - array of strings, dynamorio options
- `TARGET_CMD` - array of strings, command line for target app
- `EXCLUDE` - array of strings, files to exclude
