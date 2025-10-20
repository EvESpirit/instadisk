import ctypes
import os
import re
import shutil
import subprocess
import sys

# !!!!!!!!!! CONFIG !!!!!!!!!!
# Set the desired size of the RAM disk in Gigabytes.
ramdiskSizeGb = 8.0

# Set the filesystem for the RAMDisk.
# Supported formats: ntfs, fat, fat32, exfat, refs
ramdiskFilesystem = "ntfs"
# !!!!!!!!!! CONFIG !!!!!!!!!!


def isAdmin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def findImdiskExecutable():
    imdiskPath = shutil.which("imdisk.exe")
    if imdiskPath:
        return imdiskPath

    programFilesPath = os.environ.get("ProgramFiles", "C:\\Program Files")
    fallbackPath = os.path.join(programFilesPath, "ImDisk", "imdisk.exe")
    if os.path.exists(fallbackPath):
        return fallbackPath

    errorMessage = (
        "ERROR: Could not find 'imdisk.exe'.\n\n"
        "Please ensure the ImDisk Toolkit is installed correctly and that\n"
        "'imdisk.exe' is available in your system's PATH environment variable."
    )
    raise FileNotFoundError(errorMessage)


def createRamdisk(sizeGb: float, filesystem: str, imdiskExePath: str):
    sizeMb = int(sizeGb * 1024)
    sizeParameter = f"{sizeMb}m"
    formatParameters = f"/fs:{filesystem} /q /y"

    command = [
        imdiskExePath,
        "-a",
        "-s", sizeParameter,
        "-m", "#:",
        "-p", formatParameters,
    ]

    print(f"Attempting to create a {sizeGb} GB {filesystem.upper()} RAM disk...")
    print(f"Executing: {' '.join(command)}")

    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )

        output = result.stdout
        driveLetterPattern = re.compile(r"mounted as ([A-Z]):", re.IGNORECASE)
        match = driveLetterPattern.search(output)

        if match:
            driveLetter = match.group(1)
            print(f"\nSUCCESS: RAM disk created and mounted as drive {driveLetter}:")
            return driveLetter
        else:
            print("\nSUCCESS: RAM disk created, but the drive letter could not be determined.")
            return None

    except subprocess.CalledProcessError as e:
        print("\nERROR: Failed to create the RAM disk.")
        print(f"ImDisk process returned a non-zero exit code: {e.returncode}")

        errorOutput = e.stderr.strip() or e.stdout.strip()
        if errorOutput:
            print("\nImDisk ERROR:")
            print(errorOutput)
        else:
            print("ImDisk provided no additional error information.")

        raise


def relaunchWithAdminPrivileges():
    print("Administrator privileges are required. Attempting to re-launch...")

    shellExecuteFailureCode = 32
    try:
        returnCode = ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            sys.executable,
            subprocess.list2cmdline(sys.argv),
            None,
            1
        )

        if returnCode <= shellExecuteFailureCode:
            print(f"Failed to elevate permissions (Error code: {returnCode}).")
            input("Press Enter to exit.")

    except Exception as e:
        print(f"An unexpected error occurred during elevation attempt: {e}")
        input("Press Enter to exit.")

    finally:
        sys.exit(0)


def main():
    if not isAdmin():
        relaunchWithAdminPrivileges()

    try:
        imdiskExe = findImdiskExecutable()
        createRamdisk(
            sizeGb=ramdiskSizeGb,
            filesystem=ramdiskFilesystem,
            imdiskExePath=imdiskExe
        )
        sys.exit(0)

    except FileNotFoundError as e:
        print(f"\n{e}")
        input("\nPlease check your installation and try again. Press Enter to exit.")
        sys.exit(1)

    except subprocess.CalledProcessError:
        input("\nOperation failed. Press Enter to exit.")
        sys.exit(1)

    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        input("Press Enter to exit.")
        sys.exit(1)


if __name__ == "__main__":
    main()
