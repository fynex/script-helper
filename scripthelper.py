import json
import subprocess
import os
import re
import zipfile
import socket
import string
import random
import shutil
import platform
from collections.abc import Iterable

VERBOSE = False

class System:

    @staticmethod
    def os_name():
        return platform.system()

    @staticmethod
    def local_ip_addresses():
        return list(set(socket.gethostbyname_ex(socket.gethostname())[2]))

    @staticmethod
    def hostname():
        return socket.gethostname()

    @staticmethod
    def run_without_output(cmd, dry_run=False, print_cmd=True):
        if dry_run:
            print("[dry>] " + cmd)
            return

        if print_cmd:
            print(f"[>] {cmd}")

        os.system(cmd)

    @staticmethod
    def run(cmd, dry_run=False, print_cmd=False):
        if dry_run:
            print("[dry>] " + cmd)
            return "DRY_RUN_OUTPUT"

        if print_cmd:
            print(f"[>] {cmd}")

        if System.os_name() == "Windows":
            return subprocess.check_output(cmd.split(), shell=True).decode("cp437")

        return subprocess.check_output(cmd.split(), shell=True).decode()


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
    def read_json(file_path: str):
        return json.loads(File.read(file_path))

    @staticmethod
    def write(file_path: str, data: str):
        with open(file_path, "w") as f:
            f.write(data)

    @staticmethod
    def write_json(file_path: str, data: dict):
        return File.write(file_path, json.dumps(data))

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

    @staticmethod
    def mk(path):
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def copy(src, dst):
        shutil.copytree(src, dst, dirs_exist_ok=True)

    @staticmethod
    def cp(src, dst):
        Dir.copy(src, dst)

    @staticmethod
    def exists(path):
        return os.path.exists(path)

    @staticmethod
    def assure_trailing_sep(string):
        if not string.endswith(os.sep):
            return string + os.sep
        return string


class FileBackup:

    @staticmethod
    def backup_files_into_timestamp_dir(file_paths_to_backup: list, backup_path: str):
        now = datetime.datetime.now().isoformat().replace(":", "-")
        backup_dir = f"{backup_path}/{now}/"

        osrun(f"mkdir -p {backup_dir}", DRY_RUN)

        for file_path in file_paths_to_backup:
            osrun(f"cp -r {file_path} {backup_dir}", DRY_RUN)


class DNS:

    @staticmethod
    def get_ip_by_name(hostname):
        try:
            ip_list = socket.gethostbyname_ex(hostname.strip())[2]

            return ip_list
        except:
            if VERBOSE:
                print(f"[*] Error for '{hostname}'")
            return []

    @staticmethod
    def multiline_get_ip_by_name(hostnames: str):
        ips = []

        for hostname in hostnames.split("\n"):
            if hostname:
                ips += DNS.get_ip_by_name(hostname)

        return ips

class PP:

    @staticmethod
    def p(data):
        if isinstance(data, Iterable):
            for e in data:
                print(e)

    def comma_sep(l: list):
        return ", ".join(l)


class Extract:

    @staticmethod
    def ipv4(data: str):
        pat=re.compile(r'''\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.
        (25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.
        (25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.
        (25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))\b''', re.X)

        ips = []
        for ip_match_tuple in re.findall(pat, data):
            if ip_match_tuple:
                ip = ip_match_tuple[0]
                ips.append(ip)

        return sorted(set(ips))

    @staticmethod
    def multiline(pattern, string):
        try:
            found = re.search(pattern, string, re.S)

            if found:
                return found.group()

            return ""
        except AttributeError:
            print("[!] Pattern not found")

            return ""

    @staticmethod
    def singleline(pattern, string):
        try:
            found = re.search(pattern, string)

            if found:
                return found.group()

            return ""
        except AttributeError:
            print("[!] Pattern not found")

            return ""


