# Recovery report

- Legacy revision: `8c6d62976b7b04e369e6323b7142b1316379e7bd`
- Recovery date: 2026-09-15
- Recovered Markdown posts: 298
- Recovered fenced code blocks: 792
- Recovered static image files: 89
- Recovered standalone pages: About and Links
- Hexo build: passed with Hexo 8.1.2 and Fluid 1.9.9
- Legacy post routes regenerated exactly: 298 of 298
- Missing local image/script sources in generated HTML: 0
- npm audit findings: 0 vulnerabilities

The original repository contained generated HTML rather than Hexo source.
Published text, metadata, code, images, and routes were recovered from that
HTML. Original Markdown whitespace, Hexo-only source syntax, unpublished
drafts, and configuration values that were not rendered into the site cannot
be reconstructed exactly.

The legacy Git tree contains both `tags/GCC/` and `tags/gcc/`, which collide on
the default case-insensitive macOS filesystem. The mirror backup preserves both
Git objects. Canonical article routes do not have a case collision.
