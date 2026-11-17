# Gong Bingyan · Cybersecurity Portfolio

Application security projects and documented course practice by Gong Bingyan, Universiti Malaya.

- **Portfolio:** https://hulu338.github.io/cybersecurity-portfolio/
- **Software projects:** [Web Vuln Lab](projects/web-vuln-lab/) · [OpenList Secure Platform](projects/openlist-security/) · [AuthGuardianPro](projects/authguardian/)
- **Course projects:** [Isolated virtual lab](projects/virtual-lab-setup/) · [Nmap service scan](projects/nmap-service-scan/)
- **GitHub:** https://github.com/HuLu338

Each project documents its scope, method, results, evidence and limitations. Software case studies link to pinned snapshots of existing repositories; their test assertions were inspected, without claiming a fresh passing test run. Use the `v1.0-submission` release for the graded snapshot.

## Repository guide

`index.html` is the website home page. Project folders contain an editable write-up, a web page and supporting evidence. `assets/` contains shared styles and diagrams. See [SECURITY.md](SECURITY.md) for publication and testing boundaries.

Edit `content/profile.json`, `content/projects.json`, `content/learning-journey.md` and the project `README.md` files, then regenerate and check the static pages with Python 3 (no extra packages):

```text
python scripts/build_site.py
python scripts/check_site.py
```

GitHub Pages serves `main` from the repository root. The feature-branch pull request records how the portfolio was assembled. Original evidence and its SHA-256 manifest are kept alongside each project; assistant-operated captures are identified in the write-ups.

The Web Vuln Lab case study includes an access-policy illustration explaining its source; it does not send a request or run a security test. The homepage introduces the portfolio owner and provides project/contact links. Archivo and Space Grotesk are served locally with their OFL licenses in `assets/fonts/`.
