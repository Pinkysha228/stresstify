# Stresstify

Stresstify is a Python module created specifically for stress testing of CPU, RAM, and disk. It also provides tools to monitor the state of these components.

The module includes the main `StressTest` class with several methods, as well as additional standalone functions.


The command to install the module is `pip install stresstify`
***

### RAM Test
The `ram_test()` method performs a simple stress test on the system's RAM by loading files of approximately 8 MB into memory. When using `debug=True`, it records the elapsed time and memory usage percentage for each iteration.

``` python
import stresstify
root = StressTest(debug=True)
result = root.ram_test()
print(result)
```
Output:
``` python
{'elapsed_time': 32, 'ram_used': {0.03: '59.80%', 0.05: '60.00%', 0.07: '60.10%', 0.09: '60.30%', 0.10: '100%'}}
```
***
### Memory Test
The memory_test() method checks the disk write and read speeds by creating a temporary 1 GB binary file, which is immediately deleted. With debug=True, it displays the average write speed and average write time; with debug=False, it outputs only the values from the last iteration. Below are the key values in the dictionary and their meanings:
* average_write_time: Average time taken to write the data in seconds.
* average_read_speed: Average read speed in MB/s.
* read_average_time: Average time taken to read the data in seconds.
``` python
import stresstify
root = StressTest(debug=True)
result = root.memory_test()
print(result)
```
Output:
``` python
{'average_speed': 1189.33, 'average_time': 0.86}
```
***
### CPU Test 
The `cpu_test()` method utilizes all available processor cores for intensive computations. It accepts an optional parameter size (default is 10^7). When debug=True, it returns a dictionary containing:
* average_cpu_load: Average CPU load.
* average_cpu_freq: Average CPU frequency.
* cpu_load_dict: A dictionary with the key "start" representing the initial CPU load, followed by the load for each iteration.
* cpu_freq_dict: A dictionary with the key "start" representing the initial CPU frequency, followed by the frequency for each iteration.
* time_dict: The elapsed time for each iteration. (Note: The time values might not strictly increase, as different cores may complete tasks at varying speeds.)
``` python
import stresstify
if __name__ == '__main__':
    root = StressTest(debug=True)
    result = root.cpu_test()
    print(result)
```
Output:
``` python
{'average_cpu_load': 23.37, 'average_cpu_freq': 2409.09, 'average_time': 25.74, 'cpu_load_dict': {'start': 3.1, 1: 23.8, 2: 23.3, 3: 34.6, 4: 33.1, 5: 22.4, 6: 22.5, 7: 27.8, 8: 21.9, 9: 22.2, 10: 22.4}, 'cpu_freq_dict': {'start': 2500.0, 1: 2500.0, 2: 2500.0, 3: 2500.0, 4: 2500.0, 5: 2500.0, 6: 1500.0, 7: 2500.0, 8: 2500.0, 9: 2500.0, 10: 2500.0}, 'time_dict': {1: 25.84, 2: 25.91, 3: 25.44, 4: 25.41, 5: 26.0, 6: 25.82, 7: 25.43, 8: 25.95, 9: 25.88, 10: 25.69}}
```
***
### CPU Info
The standalone function `cpu_info()` provides detailed information about the processor:
* cpu_name: The name of the processor.
* physical_cores: Number of physical cores.
* logical_cores: Number of logical cores.
* max_frequency: Maximum CPU frequency.
* min_frequency: Minimum CPU frequency.
* current_frequency: Current CPU frequency.
* cpu_percent: A list showing the load percentage for each core.
``` python
import stresstify
root = cpu_info()
print(root)
```
Output:
``` python
{'cpu_name': '12th Gen Intel(R) Core(TM) i5-12450H', 'physical_cores': 8, 'logical_cores': 12, 'max_frequency': 2500.0, 'min_frequency': 0.0, 'current_frequency': 1500.0, 'cpu_percent': [9.1, 47.8, 22.2, 13.8, 23.8, 13.6, 25.4, 13.6, 15.2, 15.6, 16.7, 16.4]}
```
***
### RAM Info
The `memory_info()` function retrieves details about the system's RAM:
* Total_GB: Total RAM in gigabytes.
* Used_GB: Amount of RAM currently used (in gigabytes).
* Free_GB: Amount of free RAM (in gigabytes).
* Percent: Percentage of RAM utilization.
``` python
import stresstify
root = memory_info()
print(root)
```
Output:
``` python
{'Total_GB': 15.710990905761719, 'Used_GB': 10.429752349853516, 'Free_GB': 5.280986785888672, 'Percent': 66.4}
```
***
### Disk Info
The `disk_info()` function displays information about each disk partition. For each partition, it provides:
* mountpoint: The path where the partition is mounted (e.g., "C:\", "/mnt/data").
* total_size_GB: Total size of the partition in gigabytes.
* used_size_GB: Used space on the partition in gigabytes.
* free_size_GB: Free space on the partition in gigabytes.
* usage_percent: Percentage of the partition's used space.
``` python
import stresstify
root = disk_info()
print(root)
```
Output:
``` python
{'C:\\': {'mountpoint': 'C:\\', 'total_size_GB': 181.64, 'used_size_GB': 157.15, 'free_size_GB': 24.49, 'usage_percent': 86.5}, 'D:\\': {'mountpoint': 'D:\\', 'total_size_GB': 214.45, 'used_size_GB': 168.92, 'free_size_GB': 45.53, 'usage_percent': 78.8}, 'E:\\': {'mountpoint': 'E:\\', 'total_size_GB': 80.0, 'used_size_GB': 16.71, 'free_size_GB': 63.29, 'usage_percent': 20.9}}
```
***
### [Project Source Code](https://github.com/Pinkysha228/stresstify)
