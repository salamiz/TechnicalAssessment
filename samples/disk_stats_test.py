import subprocess
import re
from time import sleep


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
        output = subprocess.check_output("/proc/partitions").decode()
        if not re.search(rf"\b{self.disk_name}\b", output):
            raise RuntimeError(f"Disk {self.disk_name} not found in /proc/partitions")

    def check_proc_diskstats(self):
        """
        Checks if the disk is found in /proc/diskstats.

        Raises:
            RuntimeError: If the disk is not found.
        """
        output = subprocess.check_output("/proc/diskstats").decode()
        if not re.search(rf"\b{self.disk_name}\b", output):
            raise RuntimeError(f"Disk {self.disk_name} not found in /proc/diskstats")

    def check_sys_block(self):
        """
        Checks if the disk directory exists in /sys/block.

        Raises:
            RuntimeError: If the disk directory is not found.
        """
        cmd = ["ls", "/sys/block/*", f"{self.disk_name}*"]
        result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode != 0:
            raise RuntimeError(f"Disk {self.disk_name} not found in /sys/block")

    def check_sys_block_stat(self):
        """
        Checks if the stat file exists and is not empty in /sys/block/$DISK/.

        Raises:
            RuntimeError: If the stat file is empty or non-existent.
        """
        cmd = ["stat", "-c", "%s", f"/sys/block/{self.disk_name}/stat"]
        result = subprocess.run(cmd)
        if result.returncode != 0:
            raise RuntimeError(
                f"stat is either empty or non-existent in /sys/block/{self.disk_name}/"
            )

    def get_baseline_stats(self):
        """
        Gets the baseline statistics from /proc/diskstats and /sys/block/$DISK/stat.

        Returns:
            tuple: A tuple containing the baseline statistics from /proc/diskstats 
                   and /sys/block/$DISK/stat.
        """
        cmd = ["grep", "-w", "-m", "1", self.disk_name, "/proc/diskstats"]
        self.proc_stat_begin = subprocess.check_output(cmd).decode()
        cmd = ["cat", f"/sys/block/{self.disk_name}/stat"]
        self.sys_stat_begin = subprocess.check_output(cmd).decode()
        return self.proc_stat_begin, self.sys_stat_begin

    def generate_disk_activity(self):
        """
        Generates some disk activity using hdparm.
        """
        cmd = ["hdparm", "-t", f"/dev/{self.disk_name}"]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def verify_stat_changes(self):
        """
        Verifies if the statistics in /proc/diskstats and /sys/block/$DISK/stat 
        have changed.

        Raises:
            RuntimeError: If the statistics haven't changed.
        """
        cmd = ["grep", "-w", "-m", "1", self.disk_name, "/proc/diskstats"]
        self.proc_stat_end = subprocess.check_output(cmd).decode()
        cmd = ["cat", f"/sys/block/{self.disk_name}/stat"]
        self.sys_stat_end = subprocess.check_output(cmd).decode()

        if self.proc_stat_begin == self.proc_stat_end:
            raise RuntimeError(
                f"Stats in /proc/diskstats did not change\n{self.proc_stat_begin}\n"
                f"{self.proc_stat_end}"
            )

        if self.sys_stat_begin == self.sys_stat_end:
            raise RuntimeError(
                f"Stats in /sys/block/{self.disk_name}/stat did not change\n"
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
            print(f"Disk {self.disk_name} appears to be an NVDIMM, skipping")
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
