from test import video_stream_with_trackbars
import multiprocessing 
import time

def main_multiprocess(n_processes=None):
    if not n_processes:
        n_processes = int(input('n_processes = '))

    processes = []

    for idx in range(n_processes):
        processes.append(multiprocessing.Process(target=video_stream_with_trackbars))

    print('------ RUN PROCESSES ------\n')
    for idx, proc in enumerate(processes, start=1):
        proc.start()
        print(f'{idx}) PID: {proc.pid} has been started!')

    input('\n\n\nPress Enter to terminate\n\n\n')

    for proc in processes:
        start = time.perf_counter()
        proc_id = proc.pid
        while proc.is_alive():
            proc.terminate()
        print(f'took {round(time.perf_counter() - start, 2)} sec. to terminate process {proc_id}')

if __name__ == '__main__':
    main_multiprocess()
