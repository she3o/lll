#!/usr/bin/env python3

import os
import subprocess
from datetime import datetime

COURSES_FILE = "./.courses.txt"
LOG_FILE = "./.log.txt"

def main():
    try:
        with open(COURSES_FILE, 'r') as f:
            courses = f.read().splitlines()
    except Exception as e:
        print(f"Error reading courses file: {e}")
        return

    for course in courses:
        print(f"STARTING: {course}\n\n")

        try:
            os.mkdir(course)
        except FileExistsError:
            print(f"Failed to create directory {course}: Directory already exists")
            continue
        except Exception as e:
            print(f"Failed to create directory {course}: {e}")
            continue

        yt_dlp_command = [
            'yt-dlp',
            '-vcwi',
            '--cookies-from-browser', 'firefox',
            '--sleep-interval', '60',
            '--max-sleep-interval', '110',
            '-o', '%(playlist_index)s - %(title)s.%(ext)s',
            f'https://www.linkedin.com/learning/{course}'
        ]

        log_path = os.path.join(course, 'log.txt')
        with open(log_path, 'w') as logf:
            try:
                subprocess.run(yt_dlp_command, stdout=logf, stderr=logf, cwd=course, check=True)
            except subprocess.CalledProcessError:
                print(f"yt-dlp failed for course {course}")
                continue

        with open(LOG_FILE, 'a') as global_log:
            global_log.write(f"{datetime.now()}\n")
            global_log.write(f"{course} DONE!\n\n")

if __name__ == "__main__":
    main()
