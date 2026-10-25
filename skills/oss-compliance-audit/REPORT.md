# Report format

Write the report in the user's language. Keep it factual: each finding has evidence the user can check.

```markdown
# Compliance audit: <project>

Scope: <surfaces audited> · Jurisdictions: <e.g. France, EU, US basics> · Commit: <sha>
Not legal advice: a list of concrete gaps and proposed fixes.

## 🔴 Fix before the next public release
1. **<Short title>** (`path:line` or URL)
   - Evidence: <what you saw: a request to fonts.googleapis.com, a missing file, a logo path>
   - Why: <rule and legal basis, one sentence>
   - Fix: <smallest change that removes the risk>

## 🟠 Fix soon
...

## 🟡 Keep in mind (nothing to do today)
...

## Checked, nothing to report
- <area>: <one line on what was checked>

## Decisions for you
- <choices only the user can make: contact to publish, publisher status, rename, jurisdictions, enabling a repository setting>

## Proposed fix plan
<ordered list of commits or PRs, one per area, and which ones need a visual check>
```

Example finding:

1. **Google Fonts loaded from Google's servers** (`site/index.html:24-26`)
   - Evidence: page load requests `fonts.googleapis.com` and `fonts.gstatic.com` (site-requests.js).
   - Why: sends each visitor's IP address to Google without consent (GDPR; LG München I, 3 O 17493/20).
   - Fix: self-host the `.woff2` files under `site/fonts/` with their OFL license and remove the Google `<link>` tags.
