# 执行终端命令，形参为各文件路径
def gen_dot_config(clone: str, config: str):
    import subprocess
    commands = [
        f'chmod +x {clone} && ./{clone}',
        './scripts/feeds update -a && ./scripts/feeds install -a',
        f'mv -f {config} .config && make defconfig',
        f'cp -f .config {config}'
    ]
    for cmd in commands:
        subprocess.run(cmd, shell=True)
