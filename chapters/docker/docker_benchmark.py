import subprocess
import time

if __name__ == '__main__':
    subprocess.check_output(['docker pull nginx'], shell=True)
    execute_count = 20
    run_command = "docker run -d nginx"
    kill_command = "docker rm -f $(docker ps -a -q)"
    flush_memory_command = "echo 3 > /proc/sys/vm/drop_caches"
    total_time = 0

    for i in xrange(execute_count):
        start = time.time()
        subprocess.check_output([run_command], shell=True)
        end = time.time()
        one_time = end-start
        total_time += one_time
        time.sleep(3)
        subprocess.check_output([kill_command], shell=True)
        subprocess.check_output([flush_memory_command], shell=True)

    print "creating time per container is: %s" % str(total_time/execute_count)
