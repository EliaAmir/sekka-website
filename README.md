# sekka-eg-website

The Sekka landing page, privacy policy, and support page, served at
https://sekka-eg.com (GitHub Pages, custom domain via `CNAME`).

- `index.html` — landing page
- `privacy/index.html` — privacy policy (canonical URL: https://sekka-eg.com/privacy/)
- `support/index.html` — support page (https://sekka-eg.com/support/)

## Keep in sync

The privacy policy exists in two places:

- `privacy/index.html` in this repo (canonical URL, linked from the app and
  the Play listing going forward)
- `index.html` in the `sekka-privacy` repo (legacy URL,
  `https://eliaamir.github.io/sekka-privacy/`, kept alive because released
  app versions and the Play listing still link there)

Any change to the policy text — what's collected, why, retention, contact —
**must land in both pages in the same sitting**, with the same "last
updated" date. Never edit one without the other.

After editing either page, run the sync checker from this repo. It extracts
the visible text of the `<main id="ar">` / `<main id="en">` blocks from both
pages and fails if they differ:

```
python3 scripts/check_privacy_sync.py
```

By default it compares `../sekka-privacy/index.html` against
`privacy/index.html`; pass explicit paths if your checkout layout differs.
