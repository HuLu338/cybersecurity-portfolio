"""Build the plain-HTML portfolio using only Python's standard library."""
from pathlib import Path
import html
import json
import re
import csv

ROOT=Path(__file__).resolve().parents[1]
profile=json.loads((ROOT/'content/profile.json').read_text(encoding='utf-8'))
journey=(ROOT/'content/learning-journey.md').read_text(encoding='utf-8').strip()
E=html.escape
def words(s):return len(re.findall(r"\b[\w]+(?:[-'][\w]+)*\b",s))
counts={'about':words(' '.join(profile['about'])),'learning':words(journey),'career':words(' '.join(profile['career']))}
assert 100<=counts['about']<=200,counts
assert 400<=counts['learning']<=600,counts
assert 100<=counts['career']<=200,counts

def inline(s):
    tokens=[]
    def reserve(value):tokens.append(value);return f'ZXQTOKEN{len(tokens)-1}QXZ'
    s=re.sub(r'`([^`]+)`',lambda m:reserve('<code>'+E(m.group(1))+'</code>'),s)
    s=re.sub(r'\[([^]]+)\]\(([^)]+)\)',lambda m:reserve(f'<a href="{E(m.group(2),quote=True)}"'+(' rel="noopener noreferrer"' if m.group(2).startswith('http') else '')+'>'+E(m.group(1))+'</a>'),s)
    s=E(s)
    s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s)
    for i,token in enumerate(tokens):s=s.replace(f'ZXQTOKEN{i}QXZ',token)
    return s
def slug(s):return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
def markdown(text,skip_h1=False):
    out=[];toc=[]
    for block in re.split(r'\n\s*\n',text.strip()):
        if block.startswith('```'):
            lines=block.splitlines();out.append('<pre><code>'+E('\n'.join(lines[1:-1]))+'</code></pre>');continue
        image=re.fullmatch(r'!\[([^]]*)\]\(([^)]+)\)',block)
        if image:
            alt,path=image.groups();out.append(f'<figure><a href="{E(path)}"><img src="{E(path)}" alt="{E(alt)}" loading="lazy"></a><figcaption>{E(alt)}</figcaption></figure>');continue
        h=re.fullmatch(r'(#{1,3}) (.+)',block)
        if h:
            n=len(h.group(1));title=h.group(2)
            if n==1 and skip_h1:continue
            ident=slug(title);out.append(f'<h{n} id="{ident}">{inline(title)}</h{n}>')
            if n==2:toc.append((ident,title))
            continue
        if block.startswith('|'):
            rows=[[c.strip() for c in line.strip('|').split('|')] for line in block.splitlines() if not re.fullmatch(r'[| :\-]+',line)]
            out.append('<div class="table-scroll"><table><thead><tr>'+''.join('<th scope="col">'+inline(c)+'</th>' for c in rows[0])+'</tr></thead><tbody>')
            out.extend('<tr>'+''.join('<td>'+inline(c)+'</td>' for c in row)+'</tr>' for row in rows[1:]);out.append('</tbody></table></div>');continue
        if all(re.match(r'^\d+\. ',line) for line in block.splitlines()):
            out.append('<ol>'+''.join('<li>'+inline(re.sub(r'^\d+\. ','',line))+'</li>' for line in block.splitlines())+'</ol>');continue
        if all(line.startswith('- ') for line in block.splitlines()):
            out.append('<ul>'+''.join('<li>'+inline(line[2:])+'</li>' for line in block.splitlines())+'</ul>');continue
        out.append('<p>'+inline(block).replace('  \n','<br>').replace('\n',' ')+'</p>')
    return '\n'.join(out),toc
def paras(items):return ''.join('<p>'+inline(p)+'</p>' for p in items)
from site_templates import build
build(ROOT, profile, journey, counts, inline, markdown)
