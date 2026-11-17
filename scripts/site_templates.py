"""Templates shared by the portfolio home page and five case studies."""
import csv
import html
import hashlib
import json

E = html.escape

def build(root, profile, journey, counts, inline, markdown):
    projects = json.loads((root / 'content/projects.json').read_text(encoding='utf-8'))
    def asset(path, prefix=''):
        version=hashlib.sha256((root/path).read_bytes()).hexdigest()[:12]
        return prefix+path+'?v='+version
    def head(title, prefix=''):
        return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{E(title)}. Application security, software projects and course evidence by Gong Bingyan.">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self'; font-src 'self'; script-src 'self'; style-src 'self'; base-uri 'self'; form-action 'none'; object-src 'none'">
<meta name="color-scheme" content="light"><meta name="theme-color" content="#f6f7f2"><title>{E(title)} | Gong Bingyan</title>
<link rel="icon" href="{prefix}assets/images/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{asset('assets/portfolio.css',prefix)}">
<link rel="stylesheet" href="{asset('assets/signal-design.css',prefix)}">
<link rel="preload" href="{prefix}assets/fonts/archivo.woff2" as="font" type="font/woff2" crossorigin><script src="{asset('assets/portfolio.js',prefix)}" defer></script></head>
<body><a class="skip-link" href="#main">Skip to content</a>'''

    def header(prefix='', home=False):
        target = '' if home else prefix + 'index.html'
        nav = [('projects','Projects'),('about','About'),('skills','Skills'),('training','Training'),('learning','Learning'),('career','Career'),('contact','Contact')]
        return f'''<header class="site-header"><div class="wrap header-inner"><a class="brand" href="{target or '#top'}" aria-label="Gong Bingyan home"><span class="monogram" aria-hidden="true">gb.</span><span>Gong Bingyan<small>Cybersecurity portfolio</small></span></a><button class="nav-toggle" aria-expanded="false" aria-controls="site-nav">Menu <span aria-hidden="true">+</span></button><nav class="site-nav" id="site-nav" aria-label="Main navigation">{''.join(f'<a href="{target}#{ident}">{label}</a>' for ident,label in nav)}</nav></div></header>'''

    def footer(prefix=''):
        return f'''<footer class="site-footer"><div class="wrap footer-inner"><div><strong>Gong Bingyan</strong><p>Application security learning, with code and evidence.</p></div><div><a href="https://github.com/{profile['github']}/cybersecurity-portfolio">Source &amp; Git history</a><a href="{prefix}SECURITY.md">Evidence &amp; contribution notes</a></div></div></footer></body></html>'''

    def section(ident, title, intro=''):
        return f'<section class="section" id="{ident}" aria-labelledby="{ident}-title"><div class="wrap"><div class="section-head"><h2 id="{ident}-title">{title}</h2>' + (f'<p>{intro}</p>' if intro else '') + '</div>'

    def paras(items):
        return ''.join('<p>' + inline(p) + '</p>' for p in items)

    def policy_demo():
        return '''<aside class="policy-demo" aria-labelledby="policy-title"><div class="demo-top"><span>Policy illustration</span><span class="demo-mark" aria-hidden="true">{ }</span></div><h3 id="policy-title">Who can read this file?</h3><p class="demo-intro">The owner or an administrator. Try the policy below.</p><div class="policy-options" role="group" aria-label="Illustrate a caller's role"><button data-policy="owner" aria-pressed="true">Owner</button><button data-policy="other" aria-pressed="false">Other user</button><button data-policy="admin" aria-pressed="false">Admin</button></div><div class="request-flow"><div><span>Request</span><strong>Read file</strong></div><i aria-hidden="true">→</i><div><span>Policy</span><strong>Check access</strong></div></div><div class="policy-result" id="policy-result" role="status" aria-live="polite"><span class="result-status" id="policy-status">200 OK</span><strong id="policy-message">The owner can read the file.</strong></div><p class="demo-note">A source-based illustration, not a live request.</p><a href="#results-and-evidence">Read the code and test cases</a></aside>'''

    def art(slug):
        if slug == 'web-vuln-lab':
            return '<div class="code-art" aria-label="Simplified owner or administrator check"><span class="code-comment">The policy behind a file request</span><code><span class="code-blue">if</span> (ownerMatches || isAdmin) {<br>  <span class="code-blue">return</span> file;<br>}<br><span class="code-blue">throw</span> forbidden();</code><span class="art-caption">Simplified from the source</span></div>'
        if slug == 'openlist-security':
            return '<div class="pipeline-art" aria-label="Configuration to rule findings and review"><span>OpenList config</span><i aria-hidden="true">↓</i><div><b>TLS</b><b>Tokens</b><b>Access</b></div><i aria-hidden="true">↓</i><span>Findings, score &amp; review</span></div>'
        if slug == 'authguardian':
            return '<div class="identity-art" aria-label="Identity, permissions and audit"><span>Identity</span><i aria-hidden="true">→</i><span>Permissions</span><i aria-hidden="true">→</i><span>Audit</span></div>'
        if slug == 'virtual-lab-setup':
            return '<div class="lab-art"><span>Kali<small>192.168.77.10</small></span><i aria-hidden="true">↔</i><span>Metasploitable<small>192.168.77.20</small></span></div>'
        return '<div class="scan-art"><span>Saved TCP scan</span><strong>23 open <i>/</i> 977 closed</strong><small>1,000 common ports · recorded run</small></div>'

    site = head('Application security portfolio') + header(home=True)
    site += '''<main id="main"><section class="hero" id="top" aria-label="Introduction" data-motion="paused"><div class="hero-art" aria-hidden="true"></div><div class="hero-gridlines" aria-hidden="true"></div><div class="wrap hero-inner"><h1>Code deserves<br>a closer look.</h1><p class="hero-intro">Master of Cyber Security student at Universiti Malaya, focusing on application security and secure software development.</p><div class="actions hero-actions"><a class="button" href="#projects">Explore projects</a><a class="button secondary" href="#contact">Contact me</a></div></div><div class="wrap hero-controls"><a class="scroll-link" href="#about">Meet the person behind the code <span aria-hidden="true">↓</span></a><button class="motion-toggle" aria-label="Background animation" aria-pressed="false" hidden><span class="motion-icon" aria-hidden="true"></span><span class="motion-label">Play motion</span></button></div></section>'''
    site += section('about','Software experience.<br>Security questions.','A background in development, and a growing focus on how applications should behave at their boundaries.')
    site += '<div class="about-grid"><div class="prose" data-word-section="about">' + paras(profile['about']) + '</div><dl class="profile-facts"><div><dt>Currently</dt><dd>Master of Cyber Security<br>Universiti Malaya</dd></div><div><dt>Career direction</dt><dd>Junior application security<br>Security testing</dd></div><div><dt>Based in</dt><dd>Malaysia</dd></div><div><dt>On GitHub</dt><dd><a href="https://github.com/HuLu338">HuLu338</a></dd></div></dl></div></div></section>'
    site += section('projects','Selected work','Three existing software projects and two course labs. Each case study links the explanation to code, test assertions or original records.')
    site += '<div class="filters" role="group" aria-label="Filter projects" hidden>' + ''.join(f'<button data-filter="{E(c)}" aria-pressed="{str(c=="All work").lower()}">{E(c)}</button>' for c in ['All work','Application security','Security engineering','Identity security','Course practice']) + '</div><p class="filter-count" role="status" aria-live="polite">Showing 5 projects</p><div class="projects-grid">'
    for p in projects:
        site += f'<article class="project-card {"featured" if p["featured"] else "compact"} {"wide" if p["slug"]=="authguardian" else ""}" data-category="{E(p["category"])}"><div class="project-art {p["slug"]}">{art(p["slug"])}</div><div class="card-body"><p class="project-category">{E(p["category"])} <span>/ {E(p["type"])}</span></p><h3><a href="projects/{p["slug"]}/">{E(p["title"])}</a></h3><p class="card-subtitle">{E(p["subtitle"])}</p><p class="card-description">{E(p["description"])}</p><ul class="tech-list" aria-label="Technologies">' + ''.join(f'<li>{E(t)}</li>' for t in p['stack']) + f'</ul><div class="card-links"><a href="projects/{p["slug"]}/">Read case study</a>' + (f'<a class="source-link" href="{p["source"]}">GitHub source</a>' if p['source'] else '') + '</div></div></article>'
    site += '</div><p class="project-note">Software case studies describe existing prototypes and inspected test assertions; no new passing test run is implied. Course evidence retains its original collection notes.</p></div></section>'
    site += section('skills','Skills, with a place to look.','Current levels are grounded in the linked work. These are learning and project skills, rather than claims of professional AppSec experience.') + '<div class="skills-grid">'
    for s in profile['skills']:
        site += f'<article class="skill"><span class="level">{E(s["level"])}</span><h3>{E(s["name"])}</h3><p>{E(s["description"])}</p><a href="{E(s["link"])}">{E(s["evidence"])}</a></article>'
    site += '</div></div></section>'
    site += section('training','Training &amp; qualifications') + '''<div class="training-layout"><div class="credential-note"><span class="level">Current status</span><h3>No professional certification earned yet.</h3><p>I will add credentials with verification links when completed.</p></div><div class="training-list"><article><span>Current study</span><h3>Master of Cyber Security</h3><p>Universiti Malaya. Course-based practice includes isolated lab checks and Nmap service discovery.</p></article><article><span>Target: February 2027</span><h3>Build stronger security foundations</h3><p>Improve Linux/networking skills, trusted identity handling and repeatable application-security checks.</p></article></div></div></div></section>'''
    journey_html, _ = markdown(journey)
    site += section('learning','Learning journey','What two course activities taught me about network evidence, tool output and the questions I still need to answer.') + '<div class="journey-grid"><div class="prose" data-word-section="learning">' + journey_html + '</div><aside class="journey-aside"><span class="level">Next milestone</span><h3>February 2027</h3><p>Replace request-parameter identity in the web lab with trusted session-based identity.</p><p>Publish fresh allowed/denied results for two access-control scenarios, with repeatable instructions.</p><a href="projects/web-vuln-lab/">See the starting point</a></aside></div></div></section>'
    site += section('career','Where I want to go.','Junior AppSec or security testing, working closely with developers.') + '<div class="career-block prose" data-word-section="career">' + paras(profile['career']) + '</div></div></section>'
    site += section('contact','Talk code. Ask questions.','I welcome practical feedback and conversations about application security.') + f'''<div class="contact-grid"><a href="mailto:{profile['email']}"><span>Email</span><strong>{profile['email']}</strong></a><a href="{profile['linkedin']}"><span>LinkedIn</span><strong>bingyan0712</strong></a><a href="https://github.com/{profile['github']}"><span>GitHub</span><strong>{profile['github']}</strong></a></div></div></section></main>''' + footer()
    (root/'index.html').write_text(site,encoding='utf-8',newline='\n')

    gallery = {
        'virtual-lab-setup': [('target-identity.png','Learner-supplied target identity capture.'),('target-routes-and-ping.png','Learner-supplied target routes and reverse ping.'),('kali-isolation-checks.png','Assistant-operated Kali checks on 4 November; original label retained.')],
        'nmap-service-scan': [('nmap-first-segment.png','First segment of the assistant-operated saved-output display.'),('nmap-completion.png','Continuation of the same recorded scan, including its duration.')]
    }
    for p in projects:
        folder = root/'projects'/p['slug']
        content, toc = markdown((folder/'README.md').read_text(encoding='utf-8'),skip_h1=True)
        if p['slug']=='web-vuln-lab':
            marker='<h2 id="results-and-evidence">'
            assert marker in content
            content=content.replace(marker,'<h2 id="policy-illustration">An access decision, illustrated</h2>'+policy_demo()+marker,1)
            position=next(i for i,(ident,_) in enumerate(toc) if ident=='results-and-evidence')
            toc.insert(position,('policy-illustration','Policy illustration'))
        if p['slug']=='nmap-service-scan':
            with (folder/'evidence/open-ports.csv').open(encoding='utf-8',newline='') as f: ports=list(csv.DictReader(f))
            assert len(ports)==23
            content += '<h2 id="all-open-ports">All 23 observed open ports</h2><details class="port-details"><summary>Open the full service record and follow-up notes</summary><div class="table-scroll"><table><thead><tr><th scope="col">TCP port</th><th scope="col">Observed service / version</th><th scope="col">Meaning and follow-up</th></tr></thead><tbody>' + ''.join('<tr><td>'+E(r['port'])+'</td><td>'+E(r['observed_service_version'])+'</td><td>'+E(r['meaning_and_follow_up'])+'</td></tr>' for r in ports) + '</tbody></table></div></details>'
            toc.append(('all-open-ports','All 23 open ports'))
        if p['slug'] in gallery:
            content += '<h2 id="evidence-gallery">Evidence gallery</h2><div class="evidence-gallery">' + ''.join(f'<figure><a href="evidence/{file}"><img src="evidence/{file}" alt="{E(caption)}" loading="lazy"></a><figcaption>{E(caption)} Open the image for its original resolution.</figcaption></figure>' for file,caption in gallery[p['slug']]) + '</div>'
            toc.append(('evidence-gallery','Evidence gallery'))
        output = head(p['title'],'../../') + header('../../') + f'<main id="main"><div class="project-hero"><div class="wrap"><a class="breadcrumb" href="../../index.html#projects">Back to selected work</a><p class="project-category">{E(p["category"])} / {E(p["type"])}</p><h1>{E(p["title"])}</h1><p class="project-lead">{E(p["lead"])}</p>' + (f'<a class="button secondary" href="{p["source"]}">Open source repository</a>' if p['source'] else '') + '</div></div><div class="wrap project-layout"><article class="project-body">' + content + '</article><aside class="project-toc"><h2>In this case study</h2>' + ''.join(f'<a href="#{ident}">{E(title)}</a>' for ident,title in toc) + '<p>Read the evidence and its limits together. Test only systems you own or are authorized to assess.</p></aside></div></main>' + footer('../../')
        (folder/'index.html').write_text(output,encoding='utf-8',newline='\n')
    output=head('Page not found','/cybersecurity-portfolio/')+header('/cybersecurity-portfolio/')+'<main id="main"><div class="wrap not-found"><p>404</p><h1>This page is not here.</h1><p>Return to the portfolio to find the project or section you need.</p><a class="button" href="/cybersecurity-portfolio/">Return to the portfolio</a></div></main>'+footer('/cybersecurity-portfolio/')
    (root/'404.html').write_text(output,encoding='utf-8',newline='\n')
    print(json.dumps({'word_counts':counts,'html_pages':len(projects)+2,'projects':len(projects)},indent=2))
