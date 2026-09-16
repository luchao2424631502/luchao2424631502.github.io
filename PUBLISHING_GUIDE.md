# 博客日常发布流程

本文档是每次新增或修改博客时使用的固定流程。Hexo 源码位于 `source`
分支，生成的网站文件发布到 `gh-pages` 分支；不要直接编辑 `gh-pages`
中的 HTML。

## 一、首次在新电脑准备环境

```bash
git clone --branch source \
  git@github.com:luchao2424631502/luchao2424631502.github.io.git blog-source
cd blog-source
npm ci
```

`npm ci` 会严格按照 `package-lock.json` 安装已经固定的 Hexo、Fluid 和
部署插件版本。

## 二、每次写文章前同步源码

```bash
cd /Users/Admin/personal/blog/source
git switch source
git pull --ff-only origin source
```

如果其他电脑修改过博客，这一步可以避免基于旧源码继续编辑。

## 三、新建或修改 Markdown

新建文章：

```bash
npx hexo new post "文章标题"
```

新文件会出现在 `source/_posts/`。也可以直接复制下面的模板：

```yaml
---
title: 文章标题
date: 2026-09-16 20:00:00
categories:
  - 技术
tags:
  - Hexo
  - GitHub Pages
---

这里开始写正文。
```

旧文章已有显式 `permalink`，不要随意修改，以免原链接失效。新文章通常
不需要手写 `permalink`，Hexo 会使用 `_config.yml` 中的规则生成地址。

## 四、本地检查

先执行一次完整构建：

```bash
npm run clean
npm run build
```

再启动本地预览：

```bash
npm run server
```

浏览器访问 `http://localhost:4000/`，至少检查：

- 首页能打开，新增文章出现在列表中；
- 正文、代码块、图片、分类和标签正常；
- 文章内部链接没有写成本机绝对路径；
- 页面中没有不应公开的密码、令牌或个人资料。

检查结束后按 `Ctrl+C` 停止本地服务器。

## 五、先备份源码，再发布网站

```bash
git status
git add .
git commit -m "发布：文章标题"
git push origin source
```

确认源码已推送成功后，再发布静态网站：

```bash
npm run deploy
```

该命令会依次清理旧构建、重新生成网站，并将 `public/` 中的静态文件
推送到远端 `gh-pages` 分支。

## 六、发布后验证

等待 GitHub Pages 完成部署，然后检查：

```text
https://blog.989883.xyz/
```

建议同时打开新文章的完整 URL，并检查 GitHub 仓库中 `gh-pages` 分支
的最新提交时间。如果域名刚设置，DNS 和 HTTPS 证书可能需要一段时间
才能生效。

## 七、出现问题时

- 构建失败：不要运行部署；先根据终端错误修改 Markdown 或配置。
- 源码推送失败：先解决 Git 冲突，不要使用 `git push --force` 覆盖
  `source` 分支。
- 新站严重异常：在仓库 `Settings → Pages` 中临时把发布源切回
  `master /(root)` 或 `legacy-static /(root)`，即可恢复旧静态站。
- `gh-pages` 是生成产物，允许部署工具更新；`source`、`master` 和
  `legacy-static` 才是需要长期保护的内容。

## 最简日常清单

```bash
cd /Users/Admin/personal/blog/source
git pull --ff-only origin source
npx hexo new post "文章标题"       # 修改已有文章时跳过
npm run clean && npm run build
npm run server                      # 浏览器检查，完成后 Ctrl+C
git add .
git commit -m "发布：文章标题"
git push origin source
npm run deploy
```
