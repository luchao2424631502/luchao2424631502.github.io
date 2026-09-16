# llc'blog Hexo source

This branch contains the recovered, editable Hexo source for
`https://blog.989883.xyz`. Generated files are deployed to the `gh-pages`
branch; the original generated site remains preserved on `master` and
`legacy-static`.

## Local workflow

```bash
npm ci
npm run server
```

Create or edit Markdown files under `source/_posts`, commit them to the
`source` branch, and publish only after a successful local build:

```bash
npm run build
npm run deploy
```

The one-time HTML-to-Markdown recovery utility is kept under `tools/` for
auditability. It reads page blobs directly from Git so case-colliding paths in
the legacy static site do not cause data loss on macOS.

## 中文文档

- [日常发布流程](PUBLISHING_GUIDE.md)
- [自定义域名配置](DOMAIN_SETUP.md)
- [旧站恢复报告](RECOVERY_REPORT.md)
