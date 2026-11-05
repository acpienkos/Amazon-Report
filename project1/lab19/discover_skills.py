"""Ask the actual Codex app-server to discover repo skills; no model turn or credentials."""
from pathlib import Path
import sys, tempfile, os, subprocess, threading, queue, json, time

ROOT = Path(__file__).resolve().parent

def main():
    codex = Path(os.environ['APPDATA'])/'npm/codex.cmd'
    with tempfile.TemporaryDirectory(prefix='lab19-discovery-') as temporary:
        env = dict(os.environ, CODEX_HOME=temporary)
        process = subprocess.Popen([str(codex),'app-server','--stdio'], stdin=subprocess.PIPE,stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,text=True,encoding='utf-8',env=env,creationflags=subprocess.CREATE_NO_WINDOW)
        messages=queue.Queue()
        def read():
            for line in process.stdout:
                try: messages.put(json.loads(line))
                except json.JSONDecodeError: pass
        threading.Thread(target=read,daemon=True).start()
        def send(message):
            process.stdin.write(json.dumps(message)+'\n')
            process.stdin.flush()
        def response(identifier):
            limit=time.monotonic()+30
            while time.monotonic()<limit:
                try: item=messages.get(timeout=1)
                except queue.Empty: continue
                if item.get('id')==identifier:
                    return item
            raise TimeoutError('No app-server response')
        try:
            send({'id':1,'method':'initialize','params':{'clientInfo':{'name':'lab19_validation','version':'1.0.0'},'capabilities':{'experimentalApi':True}}})
            initialized=response(1)
            if 'error' in initialized: raise RuntimeError(initialized['error'])
            send({'method':'initialized','params':{}})
            send({'id':2,'method':'skills/list','params':{'cwds':[str(ROOT)],'forceReload':True}})
            result=response(2)
            if 'error' in result: raise RuntimeError(result['error'])
            # Store only repo skill metadata, not unrelated home skill contents.
            entries=result['result']['data']
            skills=[s for entry in entries for s in entry.get('skills',[]) if s.get('name') in ('buffett-panel','cathie-wood-panel','burry-panel')]
            evidence={'method':'skills/list','cwd':str(ROOT),'skills':skills,'errors':[e for entry in entries for e in entry.get('errors',[])]}
            (ROOT/'evidence/codex_discovery.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
            assert len(skills)==3,evidence
            print('Actual Codex skills/list discovered:',', '.join(s['name'] for s in skills))
        finally:
            process.terminate()
            process.communicate(timeout=10)

if __name__=='__main__':
    main()
