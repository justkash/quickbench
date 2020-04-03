import argparse
import subprocess
import time
import resource
import sys
from statistics import mean, median, stdev
from print_utils import print_2D_table, print_table

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Utility to quickly measure the memory usage and execution time for a given program process.")

        parser.add_argument("command", help="command to execute for measurement")
        parser.add_argument("-s", "--supress_output", action="store_true", default=False, help="supress all output from the running process")
        parser.add_argument("-v", "--verbose", action="store_true", default=False, help="include a description with results")
        parser.add_argument("-i", "--iterations", type=int, default=1, help="number of iterations to run (default is one)")
        parser.add_argument("-t", "--timeout", type=int, default=1000, help="amount of time in milliseconds to wait before terminating the running process (default is 1s)")
        args = parser.parse_args()

        elapsed_times = [None]*args.iterations
        user_times = [None]*args.iterations
        sys_times = [None]*args.iterations
        ram_usages = [None]*args.iterations
        min_flts = [None]*args.iterations
        maj_flts =[None]*args.iterations

        for i in range(args.iterations):
            start_time = time.time()
            run_info = subprocess.run(
                args.command.split(),
                stdin=None,
                input=None,
                stdout=(subprocess.DEVNULL if args.supress_output else subprocess.PIPE),
                stderr=subprocess.STDOUT,
                capture_output=False,
                shell=False,
                cwd=None,
                timeout=args.timeout,
                check=False,
                encoding=None,
                errors=None,
                text=True,
                env=None,
                universal_newlines=None
            )
            elapsed_time_ms = (time.time() - start_time)*1000.0

            res_usage_info = resource.getrusage(resource.RUSAGE_CHILDREN)

            elapsed_times[i] = elapsed_time_ms
            user_times[i] = res_usage_info.ru_utime*1000.0
            sys_times[i] = res_usage_info.ru_stime*1000.0
            ram_usages[i] = res_usage_info.ru_maxrss
            min_flts[i] = res_usage_info.ru_minflt
            maj_flts[i] = res_usage_info.ru_majflt

            if not args.supress_output:
                print(run_info.stdout)

        # Print results
        rowheaders = ["Elapsed Time (ms)",  "User Time (ms)", "Sys Time (ms)", "Peak Memory Usage (kB)", "# of Minor Page Faults", "# of Major Page Faults"]
        colheaders = ["Min", "Mean", "Median", "Max", "Std Dev"]

        elapsed_time_table_vals = user_time_table_vals = sys_time_table_vals = ram_usage_table_vals = min_flts_table_vals = maj_flts_table_vals  = []
        if args.iterations > 1:
            elapsed_time_table_vals = [min(elapsed_times), mean(elapsed_times), median(elapsed_times), max(elapsed_times), stdev(elapsed_times)]
            user_time_table_vals = [min(user_times), mean(user_times), median(user_times), max(user_times), stdev(user_times)]
            sys_time_table_vals = [min(sys_times), mean(sys_times), median(sys_times), max(sys_times), stdev(sys_times)]
            ram_usage_table_vals = [min(ram_usages), int(mean(ram_usages)), int(median(ram_usages)), max(ram_usages), stdev(ram_usages)]
            min_flts_table_vals = [min(min_flts), mean(min_flts), int(median(min_flts)), max(min_flts), stdev(min_flts)]
            maj_flts_table_vals = [min(maj_flts), mean(maj_flts), int(median(maj_flts)), max(maj_flts), stdev(maj_flts)]
        else:
            elapsed_time_table_vals = elapsed_times
            user_time_table_vals = user_times
            sys_time_table_vals = sys_times
            ram_usage_table_vals = ram_usages
            min_flts_table_vals = min_flts
            maj_flts_table_vals = maj_flts

        if args.verbose:
            colheaders.append("Description")
            elapsed_time_table_vals.append("Wall clock time taken from start to finish of the process execution.")
            user_time_table_vals.append("The amount of CPU time spent in user-mode (outside the kernel) for the process execution.")
            sys_time_table_vals.append("The amount of CPU time spend in kernel-mode within system calls, as opposed to library code.")
            ram_usage_table_vals.append("The resident set size (peak memory usage) of the largest of the spawned processes.")
            min_flts_table_vals.append("The number of page faults serviced without any I/O activity.")
            maj_flts_table_vals.append("The number of page faults serviced that required I/O activity.")

        if args.iterations > 1:
            print(f"Results from {args.iterations} iterations for command '{args.command}':")
            print_2D_table(
                    rowheaders, colheaders,
                    elapsed_time_table_vals,
                    user_time_table_vals,
                    sys_time_table_vals,
                    ram_usage_table_vals,
                    min_flts_table_vals,
                    maj_flts_table_vals
            )
        elif args.iterations == 1:
            print(f"Results from one iteration for command '{args.command}':")
            print_table(
                    rowheaders,
                    elapsed_time_table_vals,
                    user_time_table_vals,
                    sys_time_table_vals,
                    ram_usage_table_vals,
                    min_flts_table_vals,
                    maj_flts_table_vals
            )
        else:
            print("The command was successfully executed zero times; the elasped time is 0ms and took 0kB of memory. This is as fast and optimized as it gets.")

    except subprocess.TimeoutExpired as timeoutErr:
        sys.stderr.write("Time limit set for {}ms expired before process completion with output: {}.".format(args.timeout, timeoutErr.output))
    except subprocess.CalledProcessError as processErr:
        sys.stderr.write("Process exited with non-zero exitcode {} and output: {}.".format(processErr.returncode, processErr.output))
    except TypeError as typeErr:
        sys.stderr.write(str(typeErr))
    #except:
        #sys.stderr.write("An unexcepted error has occurred with sys info: {}.".format(sys.exc_info()[0]))
