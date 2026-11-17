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
def head(title,prefix=''):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{E(title)} — application security learning and documented lab work by Gong Bingyan."><meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self'; script-src 'self'; style-src 'self'; base-uri 'self'; form-action 'none'; object-src 'none'"><meta name="color-scheme" content="light"><title>{E(title)} | Gong Bingyan</title><link rel="icon" href="{prefix}assets/images/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}assets/site.css"><script src="{prefix}assets/site.js" defer></script></head><body><a class="skip-link" href="#main">Skip to content</a>'''
def header(prefix='',home=False):
    target='' if home else prefix+'index.html'
    nav=[('about','About'),('skills','Skills'),('training','Training'),('projects','Projects'),('learning','Learning'),('career','Career'),('contact','Contact')]
    return '<header class="site-header"><div class="wrap header-inner"><a class="brand" href="'+(prefix+'index.html' if not home else '#top')+'" aria-label="Gong Bingyan home"><span class="monogram">GB</span><span class="brand-name">GONG BINGYAN<small>CYBERSECURITY PORTFOLIO</small></span></a><nav class="site-nav" aria-label="Main navigation">'+''.join(f'<a href="{target}#{ident}">{label}</a>' for ident,label in nav)+'</nav></div></header>'
def footer(prefix=''):
    return f'''<footer class="site-footer"><div class="wrap footer-inner"><span>Gong Bingyan · WQE7001 · Universiti Malaya</span><span><a href="https://github.com/{profile['github']}/cybersecurity-portfolio" rel="noopener noreferrer">Source &amp; Git history</a> &nbsp; / &nbsp; <a href="{prefix}SECURITY.md">Evidence &amp; publication notes</a></span></div></footer></body></html>'''
def section_open(ident,n,title,intro=''):
    return f'<section class="section" id="{ident}" aria-labelledby="{ident}-title"><div class="wrap"><div class="section-head"><div><p class="section-number">{n:02d} / {ident.upper()}</p><h2 id="{ident}-title">{title}</h2></div>'+('<p class="section-intro">'+intro+'</p>' if intro else '')+'</div>'
mini_svg='''<svg viewBox="0 0 450 130" aria-hidden="true"><path d="M85 65H365" stroke="#a6b59d" stroke-width="2" stroke-dasharray="5 6"/><rect x="20" y="22" width="142" height="86" rx="12" fill="#fffef9" stroke="#bac9af"/><rect x="288" y="22" width="142" height="86" rx="12" fill="#fffef9" stroke="#bac9af"/><circle cx="225" cy="65" r="19" fill="#244d39"/><path d="m216 65 6 6 12-13" fill="none" stroke="#f4f7ed" stroke-width="2"/><text x="91" y="59" text-anchor="middle" font-family="Arial,sans-serif" font-size="16" fill="#244d39">Kali Linux</text><text x="91" y="81" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" fill="#617064">192.168.77.10</text><text x="359" y="59" text-anchor="middle" font-family="Arial,sans-serif" font-size="16" fill="#244d39">Metasploitable</text><text x="359" y="81" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" fill="#617064">192.168.77.20</text></svg>'''
site=head('Application security portfolio')+header(home=True)
site+='''<main id="main"><div class="wrap hero" id="top"><div class="hero-grid"><div><p class="eyebrow">Application security · Student portfolio</p><h1>Gong Bingyan.<span>Learning to build<br>safer software.</span></h1><p class="hero-copy">Master of Cyber Security student at Universiti Malaya. I connect software development with practical security checks, clear evidence and verified repairs.</p><div class="actions"><a class="button" href="#projects">Explore my projects <span aria-hidden="true">↗</span></a><a class="button secondary" href="#contact">Get in touch</a></div><div class="hero-footer"><span><i class="status-dot" aria-hidden="true"></i>Currently studying</span><span>AppSec focus</span><span>Malaysia</span></div></div><aside class="focus-card" aria-label="Current focus"><span class="small">The direction I am building toward</span><h2>Application<br>security.</h2><dl><div><dt>Current study</dt><dd>Master of Cyber Security</dd></div><div><dt>University</dt><dd>Universiti Malaya</dd></div><div><dt>Practical foundation</dt><dd>Linux · Networking · APIs</dd></div><div><dt>Next milestone</dt><dd>February 2027</dd></div></dl></aside></div></div>'''
site+=section_open('about',1,'A developer’s interest.<br>A security mindset.')+'<div class="about-grid"><div class="prose" data-word-section="about">'+paras(profile['about'])+'</div><ul class="note-list"><li><span>Current role</span>Postgraduate student</li><li><span>Career direction</span>Junior AppSec / security testing</li><li><span>Approach</span>Document the method. Check the result.</li><li><span>Public work</span><a href="https://github.com/HuLu338">github.com/HuLu338</a></li></ul></div><p class="word-note">'+str(counts['about'])+' words · About me</p></div></section>'
site+=section_open('skills',2,'Foundations I am developing.','Levels describe my current evidence and learning stage. Each skill points to a project, development work or a next step.')+'<div class="skills-grid">'
for skill in profile['skills']:
    site+=f'<article class="skill"><span class="level">{E(skill["level"])}</span><h3>{E(skill["name"])}</h3><p>{E(skill["description"])}</p><a href="{E(skill["link"])}">{E(skill["evidence"])} <span aria-hidden="true">↗</span></a></article>'
site+='</div></div></section>'
site+=section_open('training',3,'Certifications &amp; training.')+'''<ul class="training-list"><li><span class="label">Professional credentials</span><div><h3>No professional certification earned yet</h3><p>I will add credentials with a verification link when completed.</p></div><span class="when">Current status</span></li><li><span class="label">Course-based practice</span><div><h3>Isolated lab checks &amp; Nmap service discovery</h3><p>Documented WQE7001 practice. Collection methods and results are explained in the <a href="#projects">two projects</a>.</p></div><span class="when">November 2026</span></li><li><span class="label">Planned self-study</span><div><h3>Strengthen security foundations through projects</h3><p>Linux, networking and web/API testing, with repeatable checks and published results.</p></div><span class="when">Target: February 2027</span></li></ul></div></section>'''
site+=section_open('projects',4,'Practical work. Inspectable evidence.','Two course projects, each with its own objective, method, results and next steps.')+f'''<div class="projects-grid"><article class="project-card"><div class="project-art">{mini_svg}</div><div class="card-body"><div class="card-top"><span>Project 01</span><span>Linux / Networking</span></div><h3>Building an isolated virtual lab</h3><p>A private VMware segment, two training guests and checks that distinguish mutual reachability from network isolation.</p><a class="card-link" href="projects/virtual-lab-setup/">Read the lab project <span aria-hidden="true">↗</span></a></div></article><article class="project-card"><div class="project-art scan"><div class="mini-results" aria-label="Sample of observed services"><div><span>80 / tcp</span><span class="key">HTTP</span></div><div><span>3306 / tcp</span><span class="key">MySQL</span></div><div><span>8180 / tcp</span><span class="key">HTTP</span></div><small>Sample from 23 observed open ports</small></div></div><div class="card-body"><div class="card-top"><span>Project 02</span><span>Nmap / Analysis</span></div><h3>Service discovery with Nmap</h3><p>Read a saved TCP scan, explain its limits and turn service observations into a sensible AppSec follow-up plan.</p><a class="card-link" href="projects/nmap-service-scan/">Read the scan project <span aria-hidden="true">↗</span></a></div></article></div><p class="project-note">Both projects use the same owned or controlled training lab. Evidence notes distinguish learner-supplied captures from assistant-operated captures. A service label is not presented as a confirmed vulnerability.</p></div></section>'''
journey_html,_=markdown(journey)
site+=section_open('learning',5,'What the course is teaching me.')+f'''<div class="journey-grid"><div class="prose" data-word-section="learning">{journey_html}</div><aside class="journey-aside"><p class="when">Development target / February 2027</p><h3>Move from a scan result to a verified repair.</h3><p>Publish or improve one owned web/API project with two issue, repair and retest cases.</p><p>Check quality through repeatability, tests and review feedback. Track stars as interest, not proof.</p></aside></div><p class="word-note">{counts['learning']} words · Learning journey</p></div></section>'''
site+=section_open('career',6,'A pathway into AppSec.')+'<div class="career-block"><div class="prose" data-word-section="career">'+paras(profile['career'])+f'</div><p class="word-note">{counts["career"]} words · Career objective</p></div></div></section>'
site+=section_open('contact',7,'Let’s connect.')+f'''<div class="contact-grid"><div><p class="contact-copy">I welcome practical feedback, learning resources and conversations about application security. These are the professional contact details I have chosen to share.</p></div><div class="contact-links"><a href="mailto:{profile['email']}"><div><span>Email</span><strong>{profile['email']}</strong></div><b aria-hidden="true">↗</b></a><a href="{profile['linkedin']}" rel="noopener noreferrer"><div><span>LinkedIn</span><strong>linkedin.com/in/bingyan0712</strong></div><b aria-hidden="true">↗</b></a><a href="https://github.com/{profile['github']}" rel="noopener noreferrer"><div><span>GitHub</span><strong>github.com/{profile['github']}</strong></div><b aria-hidden="true">↗</b></a></div></div></div></section></main>'''+footer()
(ROOT/'index.html').write_text(site,encoding='utf-8')

projects=[('virtual-lab-setup','Building an isolated virtual lab','Check the environment before using a security tool. This project documents guest identity, private routing and mutual connectivity.'),('nmap-service-scan','Nmap service discovery and AppSec review','Use a saved scan to separate exposure, probable service identity and a vulnerability that would still need validation.')]
for folder,title,lead in projects:
    source=(ROOT/f'projects/{folder}/README.md').read_text(encoding='utf-8')
    content,toc=markdown(source,skip_h1=True)
    if folder=='nmap-service-scan':
        with (ROOT/f'projects/{folder}/evidence/open-ports.csv').open(encoding='utf-8',newline='') as handle:
            ports=list(csv.DictReader(handle))
        assert len(ports)==23
        content+='<h2 id="all-open-ports">All 23 observed open ports</h2><details class="port-details"><summary>Open the full service record and follow-up notes</summary><div class="table-scroll"><table><thead><tr><th scope="col">TCP port</th><th scope="col">Observed service / version</th><th scope="col">Meaning and follow-up</th></tr></thead><tbody>'+''.join('<tr><td>'+E(row['port'])+'</td><td>'+E(row['observed_service_version'])+'</td><td>'+E(row['meaning_and_follow_up'])+'</td></tr>' for row in ports)+'</tbody></table></div></details>'
        toc.append(('all-open-ports','All 23 open ports'))
    extra=''
    if folder=='virtual-lab-setup':
        figures=[('target-identity.png','Learner-supplied target identity capture.'),('target-routes-and-ping.png','Learner-supplied target routes and reverse ping.'),('kali-isolation-checks.png','Assistant-operated Kali checks on 4 November; the original label is retained.')]
    else:
        figures=[('nmap-first-segment.png','First segment of the assistant-operated saved-output display.'),('nmap-completion.png','Continuation of the same scan, ending with the recorded duration.')]
    for file,caption in figures:
        extra+=f'<figure><a href="evidence/{file}"><img src="evidence/{file}" alt="{E(caption)}" loading="lazy"></a><figcaption>{E(caption)} Open the image for its original resolution.</figcaption></figure>'
    output=head(title,'../../')+header('../../')+f'<main id="main"><div class="project-hero"><div class="wrap"><a class="breadcrumb" href="../../index.html#projects">← Back to projects</a><p class="eyebrow">Course lab project · Owned environment</p><h1>{E(title)}</h1><p class="project-lead">{E(lead)}</p></div></div><div class="wrap project-layout"><article class="project-body">'+content+'<h2 id="evidence-gallery">Evidence gallery</h2><div class="evidence-gallery">'+extra+'</div></article><aside class="project-toc"><h2>On this page</h2>'+''.join(f'<a href="#{ident}">{E(label)}</a>' for ident,label in toc)+'<a href="#evidence-gallery">Evidence gallery</a><p class="small-note">Private lab addresses identify the course guests. Commands and results are documentation of the recorded exercise, not permission to test another system.</p></aside></div></main>'+footer('../../')
    (ROOT/f'projects/{folder}/index.html').write_text(output,encoding='utf-8')

not_found=head('Page not found','/cybersecurity-portfolio/')+header('/cybersecurity-portfolio/')+'''<main id="main"><div class="wrap hero"><p class="eyebrow">404</p><h1>This page is not here.</h1><p class="hero-copy">Return to the portfolio to find the project or section you need.</p><a class="button" href="/cybersecurity-portfolio/">Return to the portfolio</a></div></main>'''+footer('/cybersecurity-portfolio/')
(ROOT/'404.html').write_text(not_found,encoding='utf-8')
print(json.dumps({'word_counts':counts,'html_pages':4,'profile':'Gong Bingyan','linkedin':profile['linkedin']},indent=2))
