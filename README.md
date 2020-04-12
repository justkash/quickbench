# quickbench
Quickbench is a commandline utility to quickly measure the memory usage and execution time for a given program process. It makes use of the python [resource](https://docs.python.org/3/library/resource.html) package which is itself a wrapper for the operating system's [c api](https://manpages.debian.org/buster/manpages-dev/getrusage.2.en.html).

## Installation
```
$ sudo python3 setup.py install
```

## Usage
A quick overview of the available commands can be viewed using the `-h` commandline flag as shown in the following example.
```
$ quickbench -h
```
Furthermore, passing the `-v` or `--verbose` flag will also output the following descriptions for the tracked parameters.
```
     Elapsed Time (ms)  Wall clock time taken from start to finish of the process execution.
        User Time (ms)  The amount of CPU time spent in user-mode (outside the kernel) for the process execution.
         Sys Time (ms)  The amount of CPU time spend in kernel-mode within system calls, as opposed to library code.
Peak Memory Usage (kB)  The resident set size (peak memory usage) of the largest of the spawned processes.
# of Minor Page Faults  The number of page faults serviced without any I/O activity.
# of Major Page Faults  The number of page faults serviced that required I/O activity.
```

### Basic
To quickly get an overview of execution time and memory usage, the utility can be invoked as shown in the following example.
```
$ quickbench "ls -lh" -v
total 8
-rw-r--r--  1 akash  staff    33B 11 Apr 23:54 source.c
-rw-r--r--  1 akash  staff     0B 11 Apr 23:53 test_file.txt

Results from one iteration for command 'ls -lh':
     Elapsed Time (ms)  8.087   
        User Time (ms)  1.791   
         Sys Time (ms)  3.086   
Peak Memory Usage (kB)  847872  
# of Minor Page Faults  797     
# of Major Page Faults  0
```

### Advanced
By passing the `-i <integer>` flag, it is possible to execute the command a given number of times to average out the results. Also note, that it is very useful to also pass the `-s` flag along with the `-i` flag to supress the output from the command executions. An example of this is shown below.
```
$ quickbench "./a.out < test_file.txt" -i10 -s
Results from 10 iterations for command './a.out < test_file.txt':
                        Min        Mean        Median        Max        Std Dev        
                        ---        ----        ------        ---        -------        
     Elapsed Time (ms)  10.336     44.552      11.482        342.014    104.519        
        User Time (ms)  1.869      12.579      12.380        23.090     7.050          
         Sys Time (ms)  2.959      20.187      20.160        36.503     11.174         
Peak Memory Usage (kB)  1044480    1044480     1044480       1044480    0.000          
# of Minor Page Faults  941        5177.200    5185          9391       2845.968       
# of Major Page Faults  0          0           0             0          0.000
```
