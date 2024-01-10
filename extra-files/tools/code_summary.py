"""CodeSummary class"""
import os
import re
import subprocess
from datetime import datetime
from zoneinfo import ZoneInfo


class CodeSummary:
    """Get some information about code and make a simple summary"""

    code_from: str
    code_branch: list
    code_tag: list
    code_commit_hash: str
    code_commit_date: str
    build_date: str
    login_ip: str
    login_user: str
    login_pwd: str

    def __init__(self, codedir):
        self.codedir = codedir
        self.config = '.config'
        self.generate = 'package/base-files/files/bin/config_generate'
        self.rpcd = 'package/system/rpcd/files/rpcd.config'
        self.shadow = 'package/base-files/files/etc/shadow'

    @property
    def summary_dict(self):
        last_log = self.get_last_log()
        build_date = self.get_build_date()
        login_info = self.get_login_info()
        profiles = self.get_profiles()
        return {
            'code_from': last_log[0],
            'code_branch': last_log[1],
            'code_tag': last_log[2],
            'code_commit_hash': last_log[3],
            'code_commit_date': last_log[4],
            'build_date': build_date,
            'login_ip': login_info[0],
            'login_user': login_info[1],
            'login_pwd': login_info[2],
            'board': profiles[0],
            'subtarget': profiles[1],
            'arch_packages': profiles[2],
            'profile': profiles[3]
        }

    def get_profiles(self):
        """Get some configuration values from the .config file
        Example:
        CONFIG_TARGET_BOARD="ramips"
        CONFIG_TARGET_SUBTARGET="mt7621"
        CONFIG_TARGET_ARCH_PACKAGES="mipsel_24kc"
        CONFIG_TARGET_DEVICE_ramips_mt7621_DEVICE_xiaomi_mi-router-ac2100=y
        """

        file = self.config
        board, subtarget, arch_packages, profile = '', '', '', []
        with open(file, encoding='utf-8') as f:
            for line in f:
                if line.startswith('CONFIG_TARGET_BOARD='):
                    board = line.split('=')[1].strip().strip('"')
                elif line.startswith('CONFIG_TARGET_SUBTARGET='):
                    subtarget = line.split('=')[1].strip().strip('"')
                elif line.startswith('CONFIG_TARGET_DEVICE_') and line.endswith('=y\n'):
                    profile.append(line.strip().split("_DEVICE_")[-1].split("=")[0])
                elif line.startswith('CONFIG_TARGET_ARCH_PACKAGES='):
                    arch_packages = line.split('=')[1].strip().strip('"')

                if all([board, subtarget, arch_packages, profile]):
                    break
        return board, subtarget, arch_packages, profile

    def get_last_log(self):
        prev_dir = os.getcwd()
        os.chdir(self.codedir)
        code_url = subprocess.run(
            'git remote get-url origin',
            shell=True,
            capture_output=True,
            text=True).stdout.strip()

        code_name_table = {
            ('coolsnowwolf', 'lede'): 'lede'
        }
        code_ = tuple(code_url.rstrip('/').removesuffix('.git').split('/')[-2:])
        try:
            code_from = code_name_table[code_]
        except KeyError:
            if code_[0] == code_[1]:
                code_from = code_[0]
            else:
                code_from = code_[0] + '/' + code_[1]

        code_commit_log = subprocess.run(
            'git log -1 --pretty=format:%cI%n%h%n%D',
            shell=True,
            capture_output=True,
            text=True).stdout.strip().split('\n')
        code_commit_date = datetime.fromisoformat(
            code_commit_log[0]).astimezone(ZoneInfo('Asia/Shanghai')).isoformat()
        code_commit_hash = code_commit_log[1][:7]
        code_ref = code_commit_log[2].replace(' ', '').split(',')

        code_branch = []
        code_tag = []
        for r in code_ref:
            if r.startswith('HEAD->'):
                code_branch.append(r[6:])
            elif r.startswith('tag:'):
                code_tag.append(r[4:])
            elif '/' in r or r == 'HEAD' or r == 'grafted':
                pass
            else:
                code_branch.append(r)

        if not code_branch:
            tag_belong_to = subprocess.run(
                'git branch --contains HEAD',
                shell=True,
                capture_output=True,
                text=True).stdout.strip().split('\n')
            for tb in tag_belong_to:
                if not tb.startswith('* (HEAD detached'):
                    code_branch.append(tb.strip())
        if not code_tag:
            code_tag.append('snapshot')

        for i, cb in enumerate(code_branch.copy()):
            code_branch[i] = cb.removeprefix('openwrt-')
        for i, ct in enumerate(code_tag.copy()):
            code_tag[i] = ct.removeprefix('v')

        os.chdir(prev_dir)

        return (
            code_from,
            code_branch,
            code_tag,
            code_commit_hash,
            code_commit_date
        )

    def get_build_date(self):
        return datetime.now(ZoneInfo('Asia/Shanghai')).replace(microsecond=0).isoformat()

    def get_login_info(self):
        username, password_id = self.__login_user()
        return (
            self.__login_ip(),
            username,
            self.__login_pwd(password_id)
        )

    def __login_ip(self):
        """Read the ip address from the config_generate file
        The example string 'lan) ipad=${ipaddr:-"192.168.15.1"} ;;'
        """

        file = self.generate
        with open(file, encoding='utf-8') as f:
            for line in f:
                if 'lan) ipad=' in line:
                    ip_regex = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
                    match = re.search(ip_regex, line)
                    if match:
                        return match.group()
                    return ''

    def __login_user(self):
        """Locate the 'config login' line from rpcd.config
        Then read the next few lines
        Get the username from the example string 'option username 'root '
        Get the password id from the example string 'option password '$p$root'
        """

        username = 'not set'
        password_id = 'not set'
        file = self.rpcd
        with open(file, encoding='utf-8') as f:
            for line in f:
                if 'config login' in line:
                    break
            for line in f:
                if 'option username' in line:
                    username = line.split()[-1].strip("'")
                elif 'option password' in line:
                    password_id = line.split()[-1].strip("'")[3:]
                    break
        return username, password_id

    def __login_pwd(self, password_id):
        """Read the line starting with the example string 'root' from the 'shadow' file
        Truncate the part after the first ':' in the example string 'root:: 0:99999:7:::'
        """

        file = self.shadow
        with open(file, encoding='utf-8') as f:
            for line in f:
                if line.startswith(password_id):
                    pwd_value = line.strip().split(':', 1)[-1]
                    if pwd_value == '::0:99999:7:::':
                        return 'blank'
                    return 'customized by you'
        return 'not set'
