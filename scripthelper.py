import json
import subprocess
import os
import zipfile
import socket
import string
import random
import shutil

class System:

    @staticmethod
    def local_ip_addresses():
        return list(set(socket.gethostbyname_ex(socket.gethostname())[2]))

    @staticmethod
    def hostname():
        return socket.gethostname()

    @staticmethod
    def run(cmd, dry_run=False):
        if dry_run:
            print("[dry>] " + cmd)
            return

        print(f"[>] {cmd}")

        os.system(cmd)

    @staticmethod
    def run_get_output(cmd, dry_run=False):
        if dry_run:
            print("[dry>] " + cmd)
            return "DRY_RUN_OUTPUT"

        print(f"[>] {cmd}")

        return subprocess.check_output(cmd.split()).decode()


class Random:

    @staticmethod
    def string(length, src_dataset=string.ascii_letters):
        return ''.join(random.choices(src_dataset, k=length))


class File:

    @staticmethod
    def read(file_path: str):
        with open(file_path, "r") as f:
            content = f.read()

            if isinstance(content, bytes):
                return content.decode()

            return content

    @staticmethod
    def write(file_path: str, data: str):
        with open(file_path, "w") as f:
            f.write(data)

    @staticmethod
    def regex_replace(file_path: str, regex_replacements: dict):
        replaced_file = File.read(file_path)

        for old, new in regex_replacements.items():
            replaced = re.sub(old, new, replaced_file)

            if replaced == "":
                print(f"[!] Could not replace '{old}' in file '{file_path}'")
                continue

            replaced_file = replaced

        return replaced_file

    @staticmethod
    def unzip(zip_file_path: str, output_dir: str):
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(output_dir)

    @staticmethod
    def rm(file_path):
        #shutil.rmtree(file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            print(f"The file '{file_path}' does not exist")

    @staticmethod
    def copy(src_file, dst_file):
        shutil.copy2(src_file, dst_file)

    @staticmethod
    def cp(src_file, dst_file):
        File.copy(src_file, dst_file)

    @staticmethod
    def mv(src_file, dst_file):
        shutil.move(src_file, dst_file)

class Dir:

    @staticmethod
    def rm(file_path):
        shutil.rmtree(file_path)

    def mk(path):
        if not os.path.exists(path):
            os.makedirs(path)

    def assure_trailing_sep(string):
        if not string.endswith(os.sep):
            return string + os.sep


class FileBackup:

    @staticmethod
    def backup_files_into_timestamp_dir(file_paths_to_backup: list, backup_path: str):
        now = datetime.datetime.now().isoformat().replace(":", "-")
        backup_dir = f"{backup_path}/{now}/"

        osrun(f"mkdir -p {backup_dir}", DRY_RUN)

        for file_path in file_paths_to_backup:
            osrun(f"cp -r {file_path} {backup_dir}", DRY_RUN)


