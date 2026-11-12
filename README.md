# sekka-eg-website

The Sekka landing page, privacy policy, and support page, served at
https://sekka-eg.com (GitHub Pages, custom domain via `CNAME`).

- `index.html` — landing page
- `privacy/index.html` — privacy policy (canonical URL: https://sekka-eg.com/privacy/)
- `terms/index.html` — terms of use (https://sekka-eg.com/terms/)
- `support/index.html` — support page (https://sekka-eg.com/support/)

## Where the pages come from

These files are the built output of the `sekka-web` repo (`npm run build`, then
copy `dist/` here). Edit the text there, not here: the privacy policy is
`src/legal/privacy.ts` and the terms of use are `src/legal/terms.ts`.

## Privacy policy check

The policy has one copy, `privacy/index.html`. The old address
(`https://eliaamir.github.io/sekka-privacy/`, repo `sekka-privacy`) is retired
and only forwards here, for app versions 1.0.10 and older.

```
python3 scripts/check_privacy_sync.py
```

By default it reads `../sekka-privacy/index.html` and `privacy/index.html`. It
passes when the old page still forwards to https://sekka-eg.com/privacy/ and
this page has both language blocks. Given two pages that both carry the text,
it compares them word for word.
