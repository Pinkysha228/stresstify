import psutil
import time
import numpy as np
import os
import multiprocessing
import cpuinfo


def cpu_info():
    info = {}
    cpu_name = cpuinfo.get_cpu_info()
    info['cpu_name'] = cpu_name['brand_raw']
    info["physical_cores"] = psutil.cpu_count(logical=False)
    info["logical_cores"] = psutil.cpu_count(logical=True)
    freq = psutil.cpu_freq()
    info["max_frequency"] = freq.max
    info["min_frequency"] = freq.min
    info["current_frequency"] = freq.current
    info["cpu_percent"] = psutil.cpu_percent(interval=1, percpu=True)

    return info


def memory_info():
    info = {'Total_GB': psutil.virtual_memory().total / (1024 ** 3),
            'Used_GB': psutil.virtual_memory().used / (1024 ** 3),
            'Free_GB': psutil.virtual_memory().free / (1024 ** 3), 'Percent': psutil.virtual_memory().percent}
    return info


def disk_info():
    disk_info_dict = {}
    disk_partitions = psutil.disk_partitions()
    for partition in disk_partitions:
        partition_info = {}
        usage = psutil.disk_usage(partition.mountpoint)
        partition_info['mountpoint'] = partition.mountpoint
        partition_info['total_size_GB'] = round(usage.total / (1024 ** 3), 2)
        partition_info['used_size_GB'] = round(usage.used / (1024 ** 3), 2)
        partition_info['free_size_GB'] = round(usage.free / (1024 ** 3), 2)
        partition_info['usage_percent'] = usage.percent
        disk_info_dict[partition.device] = partition_info
    return disk_info_dict


def cpu_calculation(number_a, i, size=10000000):
    start_time = time.time()
    number_a ** size
    elapsed_time = round(time.time() - start_time, 2)
    cpu_load = psutil.cpu_percent(interval=1)
    cpu_freq = psutil.cpu_freq().current
    return i, elapsed_time, cpu_load, cpu_freq


class StressTest:
    def __init__(self, debug=False):
        self.debug = debug

    def ram_test(self):
        num_elements = 8 * 1024 * 1024 // 4  # 8 MB
        elements = []
        start_time = time.time()
        ram_used = {}
        while True:
            try:
                memory = np.ones(num_elements, dtype=np.float32)
                elements.append(memory)

                if self.debug:
                    used_percent = psutil.virtual_memory().percent
                    ram_used[round(time.time() - start_time, 2)] = f'{used_percent:.2f}%'
            except MemoryError:
                elements.clear()
                break

        if self.debug:
            elapsed_time = round(time.time() - start_time)
            full_dict = {'elapsed_time': elapsed_time,
                         'ram_used': ram_used}
            return full_dict

    def memory_test(self):
        filename = 'testfile.bin'
        file_size = 1 * 1024 * 1024 * 1024  # 1 ГБ

        write_time_dict = {}
        read_time_dict = {}
        write_dict = {}
        read_dict = {}

        data = os.urandom(file_size)  # сразу создаём 1 ГБ в памяти

        for i in range(1, 11):
            # замеряем время записи
            start_time = time.time()
            with open(filename, 'wb') as file:
                file.write(data)
            elapsed_time = round(time.time() - start_time, 2)

            # замеряем время чтения
            start_time = time.time()
            with open(filename, 'rb') as file:
                data = file.read()
            elapsed_time2 = round(time.time() - start_time, 2)

            write_speed = round((file_size / (1024 * 1024)) / elapsed_time, 2)  # MB/s
            read_speed = round((file_size / (1024 * 1024)) / elapsed_time2, 2)  # MB/s

            if self.debug:
                write_time_dict[i] = elapsed_time
                read_time_dict[i] = elapsed_time2
                write_dict[i] = write_speed
                read_dict[i] = read_speed
            else:
                return write_speed, read_speed, elapsed_time

        if self.debug:
            average_write_speed = round(sum(write_dict.values()) / len(write_dict), 2)
            write_average_time = round(sum(write_time_dict.values()) / len(write_time_dict), 2)
            average_read_speed = round(sum(read_dict.values()) / len(read_dict), 2)
            read_average_time = round(sum(read_time_dict.values()) / len(read_time_dict), 2)

            full_dict = {
                'average_write_speed': average_write_speed,
                'average_write_time': write_average_time,
                'average_read_speed': average_read_speed,
                'read_average_time': read_average_time
            }
            return full_dict

    def cpu_test(self, size=10000000):
        number_a = 2 ** 256

        start_cpu_load = psutil.cpu_percent(interval=1)
        start_cpu_freq = psutil.cpu_freq().current

        cpu_load_dict = {'start': start_cpu_load}
        cpu_freq_dict = {'start': start_cpu_freq}
        time_dict = {}

        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            results = pool.starmap(cpu_calculation, [(number_a, i, size) for i in range(1, 11)])

        if self.debug:
            for i, elapsed_time, cpu_load, cpu_freq in results:
                cpu_load_dict[i] = cpu_load
                cpu_freq_dict[i] = cpu_freq
                time_dict[i] = elapsed_time

            average_cpu_load = round(sum(cpu_load_dict.values()) / len(cpu_load_dict), 2)
            average_cpu_freq = round(sum(cpu_freq_dict.values()) / len(cpu_freq_dict), 2)
            average_time = round(sum(time_dict.values()) / len(time_dict), 2)

            cpu_full_dict = {
                'average_cpu_load': average_cpu_load,
                'average_cpu_freq': average_cpu_freq,
                'average_time': average_time,
                'cpu_load_dict': cpu_load_dict,
                'cpu_freq_dict': cpu_freq_dict,
                'time_dict': time_dict
            }

            return cpu_full_dict
        else:
            return results[0][1]