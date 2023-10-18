"""File operations"""
import os
import shutil
import zipfile


def delete_dir(topdir, dirname):
    """Recursively delete a directory within the specified directory"""

    for root, dirs, files in os.walk(topdir):
        for dir in dirs:
            if dir == dirname:
                shutil.rmtree(os.path.join(root, dir))


def copy_files(topdir, targetdir, *, extension=''):
    """Recursively copy all files in the specified directory, 
    and you can set the extension to filter
    """

    for root, dirs, files in os.walk(topdir):
        for file in files:
            if file.endswith(extension):
                shutil.copy(os.path.join(root, file), targetdir)


def zip_files(dirname, zipfilename, *, excludedir='', extension=''):
    """Recursively compress all files in the specified directory, 
    exclude individual directories, 
    and set extensions for filtering
    """

    with zipfile.ZipFile(zipfilename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dirname):
            if excludedir in dirs:
                dirs.remove(excludedir)
            files = filter(lambda f: f.endswith(extension), files)
            for filename in files:
                filepath = os.path.join(root, filename)
                arcname = os.path.relpath(filepath, dirname)
                zipf.write(filepath, arcname)
