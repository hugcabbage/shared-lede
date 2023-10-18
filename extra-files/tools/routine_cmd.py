import subprocess


def gen_dot_config(clone: str, config: str):
    """Execute the terminal command,
    the shape parameters are the file path of each file
    """

    commands = [
        f'chmod +x {clone} && ./{clone}',
        './scripts/feeds update -a && ./scripts/feeds install -a',
        f'mv -f {config} .config && make defconfig',
        f'cp -f .config {config}'
    ]
    for cmd in commands:
        subprocess.run(cmd, shell=True)
