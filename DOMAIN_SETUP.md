# 自定义域名：blog.989883.xyz

Hexo 源码中已经存在 `source/CNAME`，文件内容严格如下：

```text
blog.989883.xyz
```

恢复后的网站准备发布时，请完成以下设置：

1. 打开 GitHub 账户设置中的“Pages（页面）”，将 `989883.xyz` 添加为已验证域名。GitHub 会提供一条唯一的 TXT 记录。请在 DNS 服务商处添加这条 TXT 记录，完成验证后继续保留该记录，不要删除。
2. 打开仓库的“Settings（设置）→ Pages（页面）”，选择“Deploy from a branch（从分支部署）”，将分支设为 `gh-pages`、目录设为 `/(root)`，然后保存。
3. 在同一个 Pages 设置页面中，将“Custom domain（自定义域名）”设为 `blog.989883.xyz`。
4. 在 DNS 服务商处创建以下记录。记录值中不要包含 `https://` 或仓库路径。

   | 记录类型 | 主机记录 | 记录值 | TTL |
   | --- | --- | --- | --- |
   | CNAME | `blog` | `luchao2424631502.github.io` | 自动或 600 |

5. 删除与 `blog` 主机记录冲突的所有 A、AAAA 或 CNAME 记录。此配置不要使用通配符记录。如果 DNS 服务商提供 HTTP 代理功能，请在 GitHub 签发证书期间使用“仅 DNS”模式。
6. 运行 `dig +short CNAME blog.989883.xyz` 检查 DNS。正确结果应解析为 `luchao2424631502.github.io.`。
7. GitHub 显示 DNS 检查成功后，启用“Enforce HTTPS（强制使用 HTTPS）”。证书签发和 DNS 全球生效都可能需要一些时间。

仅使用博客子域名 `blog.989883.xyz` 时，根域名 `989883.xyz` 不需要配置 A 或 AAAA 记录。只有计划让根域名承载另一个网站或执行跳转时，才需要为其配置相应记录。
