import argparse
import subprocess
import time
import resource
import sys
from statistics import fmean, stdev, variance

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Utility to quickly measure the memory usage and execution time for a given program process.")

        parser.add_argument("command", help="command to run and measure the execution of")
        parser.add_argument("-s", "--supress_output", action="store_true", default=False, help="supress all output from the running process")
        parser.add_argument("-v", "--verbose", action="store_true", default=False, help="include addtional metrics in the output")
        parser.add_argument("-i", "--iterations", type=int, default=1, help="number of iterations to run")
        parser.add_argument("-t", "--timeout", type=int, default=1000, help="amount of time in milliseconds to wait before terminating the running process")
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
                stdout=(None if args.supress_output else subprocess.PIPE),
                stderr=(None if args.supress_output else subprocess.STDOUT),
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

        if args.iterations > 1:
            #                          Average     Min     Max     Standard Deviation     Variance     Description
            #                          =======     ===     ===     ==================     ========     ===========
            # Elapsed Time (ms)      |
            # User Time (ms)         |
            # Sys Time (ms)          |
            # Peak RAM Usage (kB)    |
            # # of Minor Page Faults |
            # # of Major Page Faults |
            pass

            colheaders = ["Average", "Min", "Max", "Standard Deviation", "Variance"]
            rowheaders = ["Elapsed Time (ms)",  "User Time (ms)", "Sys Time (ms)", "Peak Memory Usage (kB)", "# of Minor Page Faults", "# of Major Page Faults"]
            elapsed_time_table_vals = [fmean(elapsed_times), min(elapsed_times), max(elapsed_times), stdev(elapsed_times), variance(elapsed_times)]
            user_time_table_vals = [fmean(user_times), min(user_times), max(user_times), stdev(user_times), variance(user_times)]
            sys_time_table_vals = [fmean(sys_times), min(sys_times), max(sys_times), stdev(sys_times), variance(sys_times)]
            ram_usage_table_vals = [fmean(ram_usages), min(ram_usages), max(ram_usages), stdev(ram_usages), variance(ram_usages)]
            min_flts_table_vals = [fmean(min_flts), min(min_flts), max(min_flts), stdev(min_flts), variance(min_flts)]
            maj_flts_table_vals = [fmean(maj_flts), min(maj_flts), max(maj_flts), stdev(maj_flts), variance(maj_flts)]

            if args.verbose:
                colheaders.append("Description")
                elapsed_time_table_vals.append("Wall clock time taken from start to finish of the process execution.")
                user_time_table_vals.append("The amount of CPU time spent in user-mode (outside the kernel) for the process execution.")
                sys_time_table_vals.append("The amount of CPU time spend in kernel-mode within system calls, as opposed to library code.")
                ram_usage_table_vals.append("The maximum resident set size (peak memory) used. Note that this is the resident set size of the largest of all spawned processes rather than the maximum resident set size of the process tree.")
                min_flts_table_vals.append("The number of page faults serviced without any I/O activity.")
                maj_flts_table_vals.append("The number of page faults serviced that required I/O activity.")

        elif args.iterations == 1:
            pass
        else
            print("The command was successfully executed zero times; the elasped time is 0ms and took 0kB of memory. This is as fast and optimized as it gets.")

    except TimeoutExpired as timeoutErr:
        sys.stderr.write("Time limit set for {}ms expired before process completion with output: {}.", args.timeout, timeoutErr.output)
    except CalledProcessError as processErr:
        sys.stderr.write("Process exited with non-zero exitcode {} and output: {}.", processErr.returncode, processErr.output)
    except:
        sys.stderr.write("An unexcepted error has occurred with sys info: {}.", sys.exc_info()[0])

