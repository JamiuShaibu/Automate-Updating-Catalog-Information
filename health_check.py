#!/usr/bin/env python3

import os
import shutil
import psutil
import socket
import emails


def check_cpu_usage():
    """Verifies that there's enough unused CPU"""
    usage = psutil.cpu_percent(1)
    return usage > 80


def check_disk_usage(disk):
    """Verifies that there's enough free space on disk"""
    du = shutil.disk_usage(disk)
    free = du.free / du.total * 100
    return free > 20


def check_available_memory():
    """Available memory in linux-instance, in byte"""
    available_memory = psutil.virtual_memory().available / (1024 * 1024)
    return available_memory > 500


def check_localhost():
    """Check localhost is correctly configured on 127.0.0.1"""
    localhost = socket.gethostbyname('localhost')
    return localhost == '127.0.0.1'


def send_alert(alert):
    """Send email if any error is reported"""
    # Replace <student> with username
    message_content = emails.generate_email("automation@example.com", "<student>@example.com", alert,
                                            "Please check your system and resolve the issue as soon as possible.", "")
    emails.send_email(message_content)
    exit("Alert email successfully sent!")


def main():
    # Check system resources:
    print("Checking system resources...")
    alert = None
    if check_cpu_usage():
        alert = "Error - CPU usage is over 80%"
        send_alert(alert)
    elif not check_disk_usage('/'):
        alert = "Error - Available disk space is less than 20%"
        send_alert(alert)
    elif not check_available_memory():
        alert = "Error - Available memory is less than 500MB"
        send_alert(alert)
    elif not check_localhost():
        alert = "Error - localhost cannot be resolved to 127.0.0.1"
        send_alert(alert)

    else:
        print("system ok")


if __name__ == "__main__":
    main()
