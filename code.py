import subprocess
import re
from process import Process
from file import File


def psaux_run():
    execution_results = subprocess.Popen(
        "ps aux", shell=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    info = execution_results.stdout.read().decode('cp866')

    lines = info.splitlines()
    del lines[0]

    all_processes_data = []
    users = []
    pids = []
    for line in lines:
        process = create_process(parse(line))
        all_processes_data.append(process)
        users.append(process.user)
        pids.append(process.pid)
    unique_users = set(users)
    processes_amount = len(set(pids))

    dict_user_pids_amount = {}
    for user in unique_users:
        pids_counter = 0
        for process in all_processes_data:
            if process.user == user:
                pids_counter += 1
        dict_user_pids_amount[user] = pids_counter

    memory_sum = 0.0
    cpu_sum = 0.0
    for process in all_processes_data:
        memory_sum += float(process.mem)
        cpu_sum += float(process.cpu)

    biggest_memory = float(all_processes_data[0].mem)
    name_of_biggest_memory_process = all_processes_data[0].command
    biggest_cpu = float(all_processes_data[0].cpu)
    name_of_biggest_cpu_process = all_processes_data[0].command
    for process in all_processes_data:
        if float(process.mem) > float(biggest_memory):
            biggest_memory = process.mem
            name_of_biggest_memory_process = process.command
        if float(process.cpu) > float(biggest_cpu):
            biggest_cpu = process.cpu
            name_of_biggest_cpu_process = process.command

    print_to_console(unique_users, processes_amount,
                     dict_user_pids_amount, memory_sum,
                     cpu_sum, name_of_biggest_memory_process,
                     name_of_biggest_cpu_process)
    make_report(unique_users, processes_amount,
                dict_user_pids_amount, memory_sum,
                cpu_sum, name_of_biggest_memory_process,
                name_of_biggest_cpu_process)


def parse(line):
    process_data = []

    re_user = re.search(r'[a-z]+[\S^\d]+', line)
    user = re_user.group()
    process_data.append(user)
    line = cut_parsed_field(line, user)

    re_pid = re.search(r'\d+', line)
    pid = re_pid.group()
    process_data.append(pid)
    line = cut_parsed_field(line, pid)

    re_cpu = re.search(r'\d{,2}[.]\d+', line)
    cpu = re_cpu.group()
    process_data.append(cpu)
    line = cut_parsed_field(line, cpu)

    re_mem = re.search(r'\d{,2}[.]\d+', line)
    mem = re_mem.group()
    process_data.append(mem)
    line = cut_parsed_field(line, mem)

    re_vsz = re.search(r'\d+', line)
    vsz = re_vsz.group()
    process_data.append(vsz)
    line = cut_parsed_field(line, vsz)

    re_rss = re.search(r'\d+', line)
    rss = re_rss.group()
    process_data.append(rss)
    line = cut_parsed_field(line, rss)

    re_tty = re.search(r'\S+', line)
    tty = re_tty.group()
    process_data.append(tty)
    line = cut_parsed_field(line, tty)

    re_stat = re.search(r'\S[^\d]+', line)
    stat = re_stat.group()
    process_data.append(stat)
    line = cut_parsed_field(line, stat)

    re_start = re.search(r'\d{2}[:]\d{2}', line)
    start = re_start.group()
    process_data.append(start)
    line = cut_parsed_field(line, start)

    re_time = re.search(r'\d{,2}[:]\d{2}', line)
    time = re_time.group()
    process_data.append(time)
    command = cut_parsed_field(line, time)[:20]
    process_data.append(command)

    return process_data


def cut_parsed_field(line, field):
    line = line[len(field):].lstrip()
    return line


def create_process(list):
    process = Process(list)
    return process


def print_to_console(unique_users, processes_amount,
                     dict_user_pids_amount, memory_sum,
                     cpu_sum, name_of_biggest_memory_process,
                     name_of_biggest_cpu_process):
    print("Отчет о состоянии системы:")
    print("Пользователи системы: ", unique_users)
    print("Процессов запущено: ", processes_amount)
    print("Пользовательских процессов: ", dict_user_pids_amount)
    print("Всего памяти используется: ", memory_sum, '%')
    print("Всего CPU используется: ", cpu_sum, '%')
    print("Больше всего памяти использует: ", name_of_biggest_memory_process)
    print("Больше всего CPU использует: ", name_of_biggest_cpu_process)


def make_report(unique_users,
                processes_amount, dict_user_pids_amount,
                memory_sum, cpu_sum, name_of_biggest_memory_process,
                name_of_biggest_cpu_process):
    scan_report = File()
    scan_report.write("Отчет о состоянии системы:")
    scan_report.write("Пользователи системы: ")
    scan_report.write_list(unique_users)
    scan_report.write("\nПроцессов запущено: " + str(processes_amount))
    scan_report.write("Пользовательских процессов: ")
    scan_report.write_dict(dict_user_pids_amount)
    scan_report.write("Всего памяти используется: " + str(memory_sum) + "%")
    scan_report.write("Всего CPU используется: " + str(cpu_sum) + "%")
    scan_report.write("Больше всего памяти использует: " +
                      name_of_biggest_memory_process)
    scan_report.write("Больше всего CPU использует: "
                      + name_of_biggest_cpu_process)
    scan_report.close()


if __name__ == '__main__':
    psaux_run()
