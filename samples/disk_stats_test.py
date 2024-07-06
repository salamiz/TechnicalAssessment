import subprocess
import re
import os
from time import sleep
import platform


class Disk:
    def __init__(self, disk_name="sda"):
        self.disk_name = disk_name
        self.status = 0
        self.nvdimm = "pmem"

    def check_proc_partitions(self):
        """
        Checks if the disk is found in /proc/partitions.

        Raises:
            RuntimeError: If the disk is not found.
        """
        if platform.system() == "Windows":
            print("Info: Skipping /proc/partitions check on Windows")
            return
        elif platform.system() == "Darwin":
            print("Info: Skipping /proc/partitions check on macOS")
            return

        output = subprocess.check_output(["cat", "/proc/partitions"]).decode()
        if not re.search(rf"\b{self.disk_name}\b", output):
            raise RuntimeError(f"Error: Disk {self.disk_name} not found in /proc/partitions")

    def check_proc_diskstats(self):
        """
        Checks if the disk is found in /proc/diskstats.

        Raises:
            RuntimeError: If the disk is not found.
        """
        if platform.system() == "Windows":
            print("Info: Skipping /proc/diskstats check on Windows")
            return
        elif platform.system() == "Darwin":
            print("Info: Skipping /proc/diskstats check on macOS")
            return

        output = subprocess.check_output(["cat", "/proc/diskstats"]).decode()
        if not re.search(rf"\b{self.disk_name}\b", output):
            raise RuntimeError(f"Error: Disk {self.disk_name} not found in /proc/diskstats")

    def check_sys_block(self):
        """
        Checks if the disk directory exists in /sys/block.

        Raises:
            RuntimeError: If the disk directory is not found.
        """
        if platform.system() == "Windows":
            print("Info: Skipping /sys/block check on Windows")
            return
        elif platform.system() == "Darwin":
            print("Info: Skipping /sys/block check on macOS")
            return

        cmd = ["ls", "/sys/block/*", f"{self.disk_name}*"]
        result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode != 0:
            raise RuntimeError(f"Error: Disk {self.disk_name} not found in /sys/block")

    def check_sys_block_stat(self):
        """
        Checks if the stat file exists and is not empty in /sys/block/$DISK/.

        Raises:
            RuntimeError: If the stat file is empty or non-existent.
        """
        if platform.system() == "Windows":
            print("Info: Skipping /sys/block/$DISK/stat check on Windows")
            return
        elif platform.system() == "Darwin":
            print("Info: Skipping /sys/block/$DISK/stat check on macOS")
            return

        cmd = ["stat", "-c", "%s", f"/sys/block/{self.disk_name}/stat"]
        result = subprocess.run(cmd)
        if result.returncode != 0:
            raise RuntimeError(
                f"Error: stat is either empty or non-existent in /sys/block/{self.disk_name}/"
            )

    def get_baseline_stats(self):
        """
        Gets the baseline statistics from /proc/diskstats and /sys/block/$DISK/stat.

        Returns:
            tuple: A tuple containing the baseline statistics from /proc/diskstats 
                   and /sys/block/$DISK/stat.
        """
        if platform.system() == "Windows":
            print("Info: Skipping baseline stats collection on Windows")
            self.proc_stat_begin, self.sys_stat_begin = None, None
            return self.proc_stat_begin, self.sys_stat_begin
        elif platform.system() == "Darwin":
            print("Info: Skipping baseline stats collection on macOS")
            self.proc_stat_begin, self.sys_stat_begin = None, None
            return self.proc_stat_begin, self.sys_stat_begin

        cmd = ["grep", "-w", "-m", "1", self.disk_name, "/proc/diskstats"]
        self.proc_stat_begin = subprocess.check_output(cmd).decode()
        cmd = ["cat", f"/sys/block/{self.disk_name}/stat"]
        self.sys_stat_begin = subprocess.check_output(cmd).decode()
        return self.proc_stat_begin, self.sys_stat_begin

    def generate_disk_activity(self):
        """
        Generates some disk activity using hdparm.
        """
        if platform.system() == "Windows":
            print("Info: Skipping disk activity generation on Windows")
            return
        elif platform.system() == "Darwin":
            print("Info: Skipping disk activity generation on macOS")
            return

        cmd = ["hdparm", "-t", f"/dev/{self.disk_name}"]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def verify_stat_changes(self):
        """
        Verifies if the statistics in /proc/diskstats and /sys/block/$DISK/stat 
        have changed.

        Raises:
            RuntimeError: If the statistics haven't changed.
        """
        if platform.system() == "Windows":
            print("Info: Skipping stat change verification on Windows")
            return
        elif platform.system() == "Darwin":
            print("Info: Skipping stat change verification on macOS")
            return

        cmd = ["grep", "-w", "-m", "1", self.disk_name, "/proc/diskstats"]
        self.proc_stat_end = subprocess.check_output(cmd).decode()
        cmd = ["cat", f"/sys/block/{self.disk_name}/stat"]
        self.sys_stat_end = subprocess.check_output(cmd).decode()

        if self.proc_stat_begin == self.proc_stat_end:
            raise RuntimeError(
                f"Error: Stats in /proc/diskstats did not change\n{self.proc_stat_begin}\n"
                f"{self.proc_stat_end}"
            )

        if self.sys_stat_begin == self.sys_stat_end:
            raise RuntimeError(
                f"Error: Stats in /sys/block/{self.disk_name}/stat did not change\n"
                f"{self.sys_stat_begin}\n{self.sys_stat_end}"
            )

    def run_test(self):
        """
        Runs the entire disk verification test.

        Raises:
            RuntimeError: If any of the checks fail.
        """
        # Check if the disk appears to be an NVDIMM and skip if so
        if self.disk_name.endswith(self.nvdimm):
            print(f"Info: Disk {self.disk_name} appears to be an NVDIMM, skipping")
            return

        # Perform all the checks
        try:
            self.check_proc_partitions()
            self.check_proc_diskstats()
            self.check_sys_block()
            self.check_sys_block_stat()
        except RuntimeError as e:
            print(f"Error: {e}")
            self.status = 1

        # Get baseline stats and generate disk activity
        self.get_baseline_stats()
        self.generate_disk_activity()

        # Wait for stats to update and verify changes
        sleep(5)
        self.verify_stat_changes()

        # If no errors, print success message
        if self.status == 0:
            print(f"PASS: Finished testing stats for {self.disk_name}")


# Example usage
if __name__ == "__main__":
    disk = Disk()  # Create a Disk object with default settings
    disk.run_test()
    exit(disk.status)
