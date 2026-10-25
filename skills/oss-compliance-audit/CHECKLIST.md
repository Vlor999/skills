# Compliance checklist

For each area: what to look for, the legal basis, and the usual fix. Severity hints are defaults; adjust them to the actual exposure (traffic, commercial use, what data is involved).

Contents: 1 Website privacy · 2 Legal notice · 3 Trademarks · 4 Licenses and notices · 5 Disclaimers and claims · 6 Security policy and supply chain · 7 Cyber Resilience Act · 8 Platform and channel rules · 9 Contributions · 10 Personal data in the software · 11 Other markets

Laws and dates change: when a finding rests on a date or threshold, say so and suggest the user checks the current text.

## 1. Website privacy (GDPR, ePrivacy)

Look for:
- Requests to third parties on page load: Google Fonts, font or script CDNs, analytics, tag managers, embedded videos and maps, social buttons, chat widgets, comment systems. Use `scripts/site-requests.js`, then confirm in the HTML/CSS/JS.
- Cookies and browser storage (`localStorage`, `sessionStorage`, IndexedDB), and who sets them.
- A privacy notice that matches reality: what the host logs, which APIs the page calls, what is stored. Absolute claims ("nothing leaves your device", "no data collected") checked against the code.
- Forms, newsletters, comments: what is collected, legal basis, where it goes.

Basis: GDPR art. 5, 6, 13 (transparency, legal basis) and art. 44+ (transfers outside the EU); ePrivacy directive art. 5(3), transposed in France by art. 82 of the Loi Informatique et Libertés (consent before storing or reading on the device, except strictly necessary storage or storage the user explicitly asked for, such as a chosen language). A German court (LG München I, 20 Jan 2022, 3 O 17493/20) held that loading Google Fonts from Google's servers without consent breached the GDPR; it triggered waves of demand letters.

Usual fix: self-host fonts and scripts (ship the font license next to the files), drop or replace analytics with a consent-free configuration (the CNIL exempts some audience measurement tools when configured strictly) or add a real consent mechanism, write a short accurate privacy section. 🔴 for Google Fonts, analytics or trackers without consent; 🟠 for inaccurate privacy claims; 🟡 for undisclosed but exempt storage.

## 2. Legal notice (France LCEN, Germany Impressum)

Look for: a "Legal notice" / "Mentions légales" page or section naming the publisher and the host.

Basis: France, Loi pour la confiance dans l'économie numérique (LCEN, 2004): a professional publisher gives its identity, address, contact and the host's details; a non-professional individual may stay anonymous towards the public by giving only the host's name and address (and phone number when available), provided the host has the publisher's identity. Germany: Impressum duty (DDG §5) for business-like sites aimed at Germany.

Usual fix: a compact block in the footer or a dedicated page: publisher (name, or "individual, non-professional publisher" plus a contact channel the user chooses), host (for GitHub Pages: GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA). Ask the user before publishing any name, email or address. 🟠 when missing on a French-published site.

## 3. Trademarks

Look for:
- Other companies' logos (Apple logo, Windows logo, store badges used without their guidelines), icons that imitate another product's.
- Other marks in the product name (e.g. "Mac", "iSomething", "Chrome", "Copilot") versus descriptive use ("for Mac", "works with GitHub"), which is generally allowed.
- An attribution line for the marks the site mentions ("X and Y are trademarks of Z, registered in the U.S. and other countries").
- "Not affiliated with" statement when the project works with another company's product.
- The project's own name: conflicts in INPI (France), EUIPO / TMview (EU), USPTO (US), package registries, app stores, domains.

Basis: trademark law (EU Regulation 2017/1001, French Code de la propriété intellectuelle, US Lanham Act) and each company's published trademark guidelines, which usually forbid using their logo in third-party material.

Usual fix: replace third-party logos with neutral icons, keep nominative text, add attribution and non-affiliation lines, suggest a name search before a launch or rename. 🔴 for a third-party logo or a third-party mark in the product name; 🟡 for missing attribution.

## 4. Licenses and third-party notices

Look for:
- A LICENSE file, a clear copyright holder, the license stated in package metadata and in the app bundle (e.g. `NSHumanReadableCopyright`, `package.json` `license`).
- Dependencies and vendored code whose license conflicts with the project's (GPL/AGPL code inside a permissive project that ships binaries, "non-commercial" licenses, code copied from Stack Overflow, which is CC BY-SA).
- Notices required by permissive licenses in what is actually distributed: MIT, BSD and Apache-2.0 require the copyright and license text (and Apache's NOTICE file) to ship with binaries, not only in the source repo. Check app bundles, installers, Docker images, minified bundles.
- Fonts (SIL OFL: ship the license; a subset or modified font cannot keep a Reserved Font Name), images and icons (CC BY needs attribution), sample data.

Basis: copyright law and the license terms themselves.

Usual fix: a `THIRD_PARTY_NOTICES` file generated from the dependency list and bundled in the artifact (and shown in the app's About screen when there is one), license headers kept on vendored files, a replacement for incompatible code. 🔴 for incompatible licenses in shipped code; 🟠 for notices missing from binaries.

## 5. Disclaimers and claims

Look for: a warranty disclaimer where users download and use the software (site, README, About screen), especially for software that touches hardware, money, health, security or other people's data; statements about third-party warranties or certifications; marketing claims that can't be backed (performance numbers, "secure", "100 % private", health effects).

Basis: the license's own disclaimer covers the code; consumer protection law (misleading commercial practices, EU directive 2005/29/EC, French Code de la consommation) applies once there is commercial activity.

Usual fix: one short "provided as is, without warranty, use at your own risk" line on the site and in the app, factual wording for claims, no promise about other companies' warranties. 🟠 when the software can damage hardware or data and the disclaimer exists only in LICENSE.

## 6. Security policy and supply chain

Look for: `SECURITY.md` with supported versions and a private reporting channel (GitHub private vulnerability reporting must also be enabled in the repo settings), secrets committed in the tree or history (keys, certificates, `.env`, tokens), CI workflows (third-party actions pinned by SHA, minimal permissions, secrets not echoed, untrusted values not interpolated in shell), signing of releases, update channel integrity (signed updates, HTTPS feed).

Basis: good practice; becomes a legal duty under the CRA for products in scope (section 7).

Usual fix: add `SECURITY.md`, ask the user to enable private reporting (a setting only they can change), rotate any leaked secret before removing it from history. 🔴 for leaked secrets or unsigned auto-updates; 🟠 for no reporting channel on software that runs privileged.

## 7. EU Cyber Resilience Act (Regulation 2024/2847)

Look for: whether the project is placed on the EU market in the course of a commercial activity (paid version, paid support tied to the product, monetised data, a company shipping it as part of a product). Donations alone do not make it commercial.

Basis: the CRA excludes free and open source software supplied outside a commercial activity; "open-source software stewards" have a lighter regime. Reporting of actively exploited vulnerabilities applies from 11 September 2026 and the main obligations from 11 December 2027.

Usual fix: usually nothing for a free hobby project; state the conclusion and the condition that would change it ("if you start selling a pro version, the CRA applies"). 🟡 by default, 🔴 for a commercial product with no vulnerability handling.

## 8. Platform and channel rules

Look for: the rules of every channel the project uses: Apple developer agreement and notarization, App Store / Google Play policies (privacy labels, data safety forms), browser extension stores (privacy disclosure, single purpose), package registries (npm, PyPI, crates.io, Homebrew acceptable use), GitHub Pages terms (not meant for commercial SaaS), use of private or undocumented OS APIs.

Usual fix: fill missing store disclosures, document known platform risks for the user (e.g. private API use can lead to certificate or listing revocation). Mostly 🟡 unless a store listing is already non-compliant.

## 9. Contributions

Look for: how contributions are licensed (`CONTRIBUTING.md` stating inbound = outbound, a DCO sign-off, or a CLA if the user may relicense later), a code of conduct if the community is active.

Usual fix: two or three lines in `CONTRIBUTING.md`. 🟡.

## 10. Personal data in the software itself

Look for: telemetry, crash reporting, accounts, sync, logs that contain personal data, third-party SDKs inside the app, what is sent to which processor and country.

Basis: GDPR in full (legal basis, information, data minimisation, processor agreements, transfers, retention, user rights).

Usual fix: opt-in telemetry, a privacy policy describing exactly what is collected, removal of unnecessary SDKs. 🔴 for undisclosed collection.

## 11. Other markets

If the project targets them, add: US state privacy laws (CCPA/CPRA for businesses above thresholds), UK GDPR, Swiss nFADP, accessibility duties (European Accessibility Act for commercial consumer products and services since 28 June 2025), export control of cryptography (publicly available open source is generally exempt under US EAR, but check before shipping to embargoed countries).
