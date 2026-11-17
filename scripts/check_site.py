"""Check links, required sections, word limits and evidence integrity offline."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import hashlib
import json
import re

ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.ids=set();self.links=[];self.images=[];self.feed(text)
    def handle_starttag(self,tag,attributes):
        attrs=dict(attributes)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids,('duplicate id',attrs['id'])
            self.ids.add(attrs['id'])
        for key in ['href','src']:
            if key in attrs:self.links.append(attrs[key])
        if tag=='img':assert attrs.get('alt'),('missing image alternative',attrs)

pages={p:Page(p.read_text(encoding='utf-8')) for p in ROOT.rglob('*.html')}
assert set(['about','skills','training','projects','learning','career','contact'])<=pages[ROOT/'index.html'].ids
errors=[];checked=0
for path,page in pages.items():
    for href in page.links:
        parsed=urlsplit(href)
        if parsed.scheme in ['https','http','mailto']:continue
        rel=unquote(parsed.path)
        if rel.startswith('/cybersecurity-portfolio/'):
            target=ROOT/rel[len('/cybersecurity-portfolio/'):]
        elif rel.startswith('/'):
            errors.append((str(path.relative_to(ROOT)),href,'wrong project root'));continue
        elif rel:target=(path.parent/rel).resolve()
        else:target=path
        if target.is_dir():target=target/'index.html'
        if not target.is_file():errors.append((str(path.relative_to(ROOT)),href,'missing file'));continue
        if parsed.fragment and target.suffix=='.html' and parsed.fragment not in pages[target].ids:
            errors.append((str(path.relative_to(ROOT)),href,'missing anchor'))
        checked+=1
assert not errors,errors

profile=json.loads((ROOT/'content/profile.json').read_text(encoding='utf-8'))
word=lambda s:len(re.findall(r"\b[\w]+(?:[-'][\w]+)*\b",s))
counts=dict(about=word(' '.join(profile['about'])),learning=word((ROOT/'content/learning-journey.md').read_text(encoding='utf-8')),career=word(' '.join(profile['career'])))
assert 100<=counts['about']<=200 and 400<=counts['learning']<=600 and 100<=counts['career']<=200,counts
assert profile['linkedin']=='https://www.linkedin.com/in/bingyan0712/'
assert profile['email']=='g504817771@gmail.com'

evidence_files=0
for manifest in ROOT.glob('projects/*/evidence/manifest.json'):
    data=json.loads(manifest.read_text(encoding='utf-8'))
    for item in data['files']:
        p=manifest.parent/item['file']
        assert hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256'],p
        evidence_files+=1
summary=json.loads((ROOT/'projects/nmap-service-scan/evidence/scan-summary.json').read_text(encoding='utf-8'))
assert (summary['open'],summary['closed'],summary['seconds'])==(23,977,11.55)
assert len(summary['ports'])==23 and not summary['exploitation_performed']

# Public-repository guard: sensitive local artifacts must never become site files.
for p in ROOT.rglob('*'):
    if not p.is_file() or '.git' in p.parts:continue
    assert p.suffix.lower() not in ['.pdf','.docx','.vmx','.vmdk','.pem','.key'],p
    if p.suffix.lower() in ['.html','.md','.json','.js','.css','.py','.yml','.nmap','.csv','.svg']:
        text=p.read_text(encoding='utf-8')
        for pattern in [r'gh[pousr]_[A-Za-z0-9]{20,}',r'-----BEGIN [A-Z ]*PRIVATE KEY-----',r'[A-Z]:\\Users\\',r'\b(?:matric(?:\s+number)?|student[\s_-]*id)\s*[:=]\s*\d{6,}\b']:
            assert not re.search(pattern,text),(p,'private artifact or secret pattern')
print(json.dumps(dict(html_pages=len(pages),internal_links_checked=checked,word_counts=counts,evidence_hashes_verified=evidence_files,scan_summary='passed',public_artifact_guard='passed'),indent=2))
