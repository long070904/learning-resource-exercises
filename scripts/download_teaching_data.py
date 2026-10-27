"""Download optional teaching fixtures; large inputs stay outside Git history."""
from pathlib import Path
import argparse,hashlib,json,os,tempfile,urllib.request

ROOT=Path(__file__).resolve().parents[1]
FILES=json.loads((Path(__file__).with_name('teaching_data_manifest.json')).read_text(encoding='utf-8'))['files']
def fingerprint(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
def ensure(item):
    target=(ROOT/item['path']).resolve()
    if not target.is_relative_to(ROOT.resolve()):raise ValueError('Data target leaves repository')
    if target.is_file() and fingerprint(target)==item['sha256']:
        print('Verified existing:',item['path']);return
    target.parent.mkdir(parents=True,exist_ok=True)
    fd,name=tempfile.mkstemp(prefix='teaching-download-',suffix='.part',dir=target.parent)
    part=Path(name)
    try:
        with os.fdopen(fd,'wb') as output,urllib.request.urlopen(item['url'],timeout=90) as response:
            for block in iter(lambda:response.read(1024*1024),b''):output.write(block)
        if part.stat().st_size!=item['bytes'] or fingerprint(part)!=item['sha256']:
            raise ValueError('Downloaded bytes differ from recorded teaching input: '+item['path'])
        part.replace(target);print('Downloaded and verified:',item['path'])
    finally:
        if part.exists():part.unlink()
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--all',action='store_true',help='Download all five optional teaching inputs')
    parser.add_argument('--name',help='Download one filename, for example mnist.npz')
    parser.add_argument('--list',action='store_true',help='List inputs without downloading')
    args=parser.parse_args()
    if not(args.all or args.name):
        for item in FILES:print(item['path'],item['bytes'],'bytes')
        return
    chosen=FILES if args.all else [f for f in FILES if Path(f['path']).name==args.name]
    if not chosen:parser.error('Unknown teaching input')
    for item in chosen:ensure(item)
if __name__=='__main__':main()
