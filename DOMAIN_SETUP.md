# Custom domain: blog.989883.xyz

The Hexo source already contains `source/CNAME` with exactly:

```text
blog.989883.xyz
```

Complete these settings when the recovered site is ready to publish.

1. In GitHub account settings, open **Pages** and add `989883.xyz` as a
   verified domain. GitHub will provide a unique TXT record. Add that TXT
   record at the DNS provider, complete verification, and keep the TXT record.
2. In repository **Settings → Pages**, choose **Deploy from a branch**, select
   `gh-pages` and `/(root)`, then save.
3. In the same Pages screen, set **Custom domain** to `blog.989883.xyz`.
4. At the DNS provider, create this record (do not include `https://` or a
   repository path):

   | Type | Host/Name | Target/Value | TTL |
   | --- | --- | --- | --- |
   | CNAME | `blog` | `luchao2424631502.github.io` | Auto or 600 |

5. Remove any conflicting A, AAAA, or CNAME record for the `blog` host. Do not
   use a wildcard record for this setup. If the provider offers an HTTP proxy,
   use DNS-only mode while GitHub provisions the certificate.
6. Confirm DNS with `dig +short CNAME blog.989883.xyz`; it should resolve to
   `luchao2424631502.github.io.`
7. After GitHub reports the DNS check as successful, enable **Enforce HTTPS**.
   Certificate issuance and DNS propagation can take time.

The base domain `989883.xyz` does not need A or AAAA records for this blog
subdomain unless it is also intended to host or redirect a separate website.
