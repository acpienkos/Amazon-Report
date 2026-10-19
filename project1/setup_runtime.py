"""Create a fresh Windows embedded Python environment; never edits historical runtimes."""
import argparse,subprocess,urllib.request,zipfile,io,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
def main():
    p=argparse.ArgumentParser();p.add_argument('--destination',default='.runtime');args=p.parse_args()
    dest=(HERE/args.destination).resolve()
    if dest.parent!=HERE or dest.name not in ['.runtime','.cold-runtime','.review-runtime']:raise ValueError('Destination must be an approved runtime name inside project1')
    if (dest/'python.exe').exists():raise ValueError('Refuse to overwrite existing runtime')
    dest.mkdir(exist_ok=True)
    archive=urllib.request.urlopen('https://www.python.org/ftp/python/3.13.7/python-3.13.7-embed-amd64.zip',timeout=60).read()
    zipfile.ZipFile(io.BytesIO(archive)).extractall(dest)
    (dest/'python313._pth').write_text('python313.zip\n.\nLib/site-packages\nimport site\n',encoding='ascii')
    pip=urllib.request.urlopen('https://bootstrap.pypa.io/get-pip.py',timeout=60).read();(dest/'get-pip.py').write_bytes(pip)
    commands=[[str(dest/'python.exe'),str(dest/'get-pip.py'),'--disable-pip-version-check'],
              [str(dest/'python.exe'),'-m','pip','install','-r',str(HERE/'requirements.txt'),'--disable-pip-version-check']]
    with (HERE/'evidence'/f'{dest.name.lstrip(".")}-install.log').open('w',encoding='utf-8') as log:
        for command in commands:
            log.write('COMMAND '+repr(command)+'\n');log.flush()
            subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,check=True)
    print('Fresh runtime ready:',dest)
if __name__=='__main__':main()
