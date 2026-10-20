# headless check: any .sv/.ct whose content overflows, or elements crossing the footer line
import subprocess, os, tempfile, shutil, json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src=open(os.path.join(ROOT,'index.html'),encoding='utf-8').read()
js='''<script>addEventListener('load',()=>setTimeout(()=>{const r=[];document.querySelectorAll('.page').forEach((pg,i)=>{const b=pg.getBoundingClientRect();
const box=pg.querySelector('.sv,.ct');if(!box)return;const lim=b.bottom-(box.classList.contains("sv")?18.5:20)*3.7795;let mx=0;box.querySelectorAll('*').forEach(e=>{const q=e.getBoundingClientRect();if(q.height&&q.bottom>mx&&!e.closest('.vis'))mx=q.bottom});
if(mx>lim+0.5)r.push([i+1,Math.round((mx-lim)/3.7795*10)/10]);
pg.querySelectorAll('.vis').forEach(v=>{const vb=v.getBoundingClientRect();v.querySelectorAll('.win,.node,div[style*="position:absolute"]').forEach(e=>{const q=e.getBoundingClientRect();if(q.bottom>vb.bottom+1||q.right>vb.right+1)r.push([i+1,'vis-clip',e.className||e.textContent.slice(0,20),Math.round((q.bottom-vb.bottom)/3.78)])})})});
document.body.setAttribute('data-r',JSON.stringify(r))},1500))</script>'''
tmp=os.path.join(ROOT,'_ovf.html');open(tmp,'w',encoding='utf-8').write(src.replace('</body>',js+'</body>'))
prof=tempfile.mkdtemp()
o=subprocess.run([r"C:\Program Files\Google\Chrome\Application\chrome.exe","--headless=new",f"--user-data-dir={prof}","--virtual-time-budget=5000","--window-size=1000,1200","--dump-dom","file:///"+tmp.replace(os.sep,'/')],capture_output=True,text=True,encoding='utf-8').stdout
shutil.rmtree(prof,ignore_errors=True);os.remove(tmp)
import re,html
m=re.search(r'data-r="([^"]*)"',o);print(html.unescape(m.group(1)) if m else 'no result')
