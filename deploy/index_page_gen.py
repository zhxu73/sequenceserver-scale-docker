#!/usr/bin/env python

import progress_reporter
import time
import subprocess


def main():
    db_dir = "/scratch/"

    time.sleep(5)
    while(True):
        output = subprocess.check_output(["bash", "-c", "du -h " + db_dir + " | tail -n 1 | awk '{$1=$1};1' | cut -d' ' -f 1"]).decode("utf-8").strip("\n")
        output = "downloaded: " + output
        print(output)
        html = progress_reporter.read_index_page()
        progress_reporter.append_detail(html, output)

        output = subprocess.check_output(["sudo", "docker", "ps"]).decode("utf-8").strip("\n")
        if len(output.split("\n")) == 1:
            break
        time.sleep(10)


if __name__== "__main__":
    main()

