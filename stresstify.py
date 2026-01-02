import psutil
import time
import numpy as np
import os
import multiprocessing
import cpuinfo
import gc
import plotext as plt
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as mplt
from threading import Thread


def plot(x: list[float], y: list[float], x_label, y_label, title, plot_type):
    valid_types = ['console', 'window']

    if plot_type not in valid_types:
        raise ValueError(f"Invalid type '{plot_type}'. Possible types: {', '.join(valid_types)}")

    if plot_type == "console":
        plt.plot(x, y, marker='*', color='red')

        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)

        plt.show()
    elif plot_type == 'window':
        mplt.plot(x, y, color='blue')
        mplt.xlabel(x_label)
        mplt.ylabel(y_label)
        mplt.title(title)

        mplt.show()


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


def cpu_calculation(i, size=5000, max_retries=3):
    for _ in range(max_retries):
        try:
            start_time = time.time()
            a = np.random.rand(size, size)
            b = np.random.rand(size, size)

            cpu_load_samples = []
            cpu_freq_samples = []

            result_holder = {}

            def do_multiplication():
                result_holder["result"] = np.dot(a, b)

            t = Thread(target=do_multiplication)
            t.start()

            while t.is_alive():
                cpu_load_samples.append(psutil.cpu_percent(interval=1))
                cpu_freq_samples.append(psutil.cpu_freq().current)

            t.join()
            elapsed_time = round(time.time() - start_time, 2)

            del result_holder["result"]
            gc.collect()

            return i, elapsed_time, cpu_load_samples, cpu_freq_samples
        except MemoryError:
            time.sleep(0.5)
            continue
    return i, None, None, None


class StressTest:
    def ram_test(self, size_mb=8, duration_sec=30, debug=False):
        num_elements = size_mb * 1024 * 1024 // 4
        blocks = []
        ram_stats = {}

        start_time = time.time()
        last_check = start_time

        try:
            while time.time() - start_time < duration_sec:
                block = np.ones(num_elements, dtype=np.float32)
                blocks.append(block)

                block[:1000] *= 2

                if debug:
                    current_time = time.time()
                    if current_time - last_check >= 1.0:
                        used_percent = psutil.virtual_memory().percent
                        ram_stats[round(current_time - start_time, 2)] = f'{used_percent:.2f}%'
                        last_check = current_time

                time.sleep(0.01)

        except MemoryError:
            print("MemoryError.")

        finally:
            del blocks

        if debug:
            elapsed_time = round(time.time() - start_time, 2)
            return {'elapsed_time': elapsed_time, 'ram_used': ram_stats}

        return {'elapsed_time': round(time.time() - start_time, 2), 'ram_used': None}

    def memory_test(self, debug=False, size=128 * 1024 ** 2):
        filename = 'testfile.bin'

        write_time_dict = {}
        read_time_dict = {}
        write_dict = {}
        read_dict = {}

        data = os.urandom(size)

        for i in range(1, 11):
            start_time = time.time()
            with open(filename, 'wb') as file:
                file.write(data)
            elapsed_time = round(time.time() - start_time, 2)

            start_time = time.time()
            with open(filename, 'rb') as file:
                read_data = file.read()

            for _ in range(5):
                try:
                    os.remove(filename)
                    break
                except PermissionError:
                    time.sleep(0.1)

            elapsed_time2 = round(time.time() - start_time, 2)

            write_speed_mb = round((size / (1024 * 1024)) / elapsed_time, 2)  # MB/s
            read_speed_mb = round((size / (1024 * 1024)) / elapsed_time2, 2)  # MB/s

            if debug:
                write_time_dict[i] = elapsed_time
                read_time_dict[i] = elapsed_time2
                write_dict[i] = write_speed_mb
                read_dict[i] = read_speed_mb
            else:
                return write_speed_mb, read_speed_mb, elapsed_time

        if debug:
            average_write_speed = round(sum(write_dict.values()) / len(write_dict), 2)
            write_average_time = round(sum(write_time_dict.values()) / len(write_time_dict), 2)
            average_read_speed = round(sum(read_dict.values()) / len(read_dict), 2)
            read_average_time = round(sum(read_time_dict.values()) / len(read_time_dict), 2)

            full_dict = {
                'average_write_speed_mb': average_write_speed,
                'average_write_time_s': write_average_time,
                'average_read_speed_mb': average_read_speed,
                'read_average_time_s': read_average_time
            }
            return full_dict

    def cpu_test(self, size=11585, iterations=11, debug=False, visualize=False, x_label='',
                 y_label='', title='', plot_type=''):
        start_cpu_load = psutil.cpu_percent(interval=1)
        start_cpu_freq = psutil.cpu_freq().current

        cpu_load_dict = {'start': start_cpu_load}
        cpu_freq_dict = {'start': start_cpu_freq}
        time_dict = {}

        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            results = pool.starmap(cpu_calculation, [(i, size) for i in range(1, iterations + 1)])

        for i, elapsed_time, cpu_load_list, cpu_freq_list in results:
            if cpu_load_list is None or cpu_freq_list is None:
                i, elapsed_time, cpu_load_list, cpu_freq_list = cpu_calculation(i, size)
            if cpu_load_list is not None:
                cpu_load_dict[i] = cpu_load_list
            if cpu_freq_list is not None:
                cpu_freq_dict[i] = cpu_freq_list
            if elapsed_time is not None:
                time_dict[i] = elapsed_time

        if debug:
            valid_cpu_loads = [sum(loads)/len(loads) for loads in cpu_load_dict.values() if isinstance(loads, list)]
            valid_cpu_freqs = [sum(freqs)/len(freqs) for freqs in cpu_freq_dict.values() if isinstance(freqs, list)]
            valid_times = [t for t in time_dict.values() if t is not None]

            average_cpu_load = round(sum(valid_cpu_loads) / len(valid_cpu_loads), 2) if valid_cpu_loads else 0
            average_cpu_freq = round(sum(valid_cpu_freqs) / len(valid_cpu_freqs), 2) if valid_cpu_freqs else 0
            average_time = round(sum(valid_times) / len(valid_times), 2) if valid_times else 0

            cpu_full_dict = {
                'average_cpu_load': average_cpu_load,
                'average_cpu_freq': average_cpu_freq,
                'average_time': average_time,
                'cpu_load_dict': cpu_load_dict,
                'cpu_freq_dict': cpu_freq_dict,
                'time_dict': time_dict
            }
            if visualize:
                # строим по первой итерации для примера
                x = list(range(1, len(cpu_load_dict[1]) + 1))
                y = cpu_load_dict[1]
                plot(x, y, title=title, x_label=x_label, y_label=y_label, plot_type=plot_type)

            return cpu_full_dict
        else:
            return results[0][1] if results and results[0][1] is not None else 0
