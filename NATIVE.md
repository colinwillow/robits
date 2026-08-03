# Shipping ROBITS as a native iOS / Android app

The web game is wrapped with **Capacitor** — it runs the same `index.html` inside a native
WebView, with a real app icon, launch screen and store listing.

Everything the game loads is now **bundled locally** (Three.js, its GLTF/Skeleton addons, and
all four webfonts). Nothing is fetched from a CDN, so the app works offline and doesn't read as
"a website in a box" to App Review — the single most common rejection reason for wrapped web apps
(Guideline 4.2, Minimum Functionality).

> **These commands must run on a Mac with Xcode installed.** iOS apps cannot be built on Linux.
> The Android half works anywhere with Android Studio.

---

## One-time setup

```bash
npm install
npx cap add ios          # creates ios/    (macOS only)
npx cap add android      # creates android/
```

## Every build

```bash
npm run build            # assembles dist/ (the only files that ship) + verifies self-containment
npx cap sync             # copies dist/ into the native projects

npm run ios              # build + sync + open Xcode
npm run android          # build + sync + open Android Studio
```

`npm run build` **fails loudly** if any external code or font URL creeps back into `index.html`.
Keep it that way — it's the guard against silently shipping a build that breaks offline.

---

## What ships

`dist/` is assembled from: `index.html`, `vendor/` (Three.js + fonts), `models/`, `audio/`,
`images/`, `thumbs/`, `levels/`, the manifest and icons. **≈98 MB** — comfortably inside Apple's
limits, and under the cellular-download threshold.

Dev-only material (scratch harnesses, `code/`, source-resolution icons, `.git`) is excluded.

## Dev mode

All developer overlays — build badge, FPS counter, ☠ KO ALL, the collider viewer, test-range
banners — are gated behind `window._DEV`, which is **off by default**.

- `?dbg=1` turns it on (sticky, stored in `localStorage`)
- `?dbg=0` turns it off

A shipping build shows none of it. Verify before every submission: launch the app fresh and
confirm there's no FPS pill, no build stamp, and no KO-ALL button.

---

## Before you submit

**Assets & metadata**
- App icon (1024×1024, no alpha, no rounded corners — `icon-1024.png` is your source)
- Screenshots for every required device size
- Privacy policy URL (required even if you collect nothing)
- App Privacy questionnaire in App Store Connect. Multiplayer sends a display name and
  match state — declare it honestly.
- Age rating questionnaire. Cartoon robot combat → expect ~9+/12+.

**Technical**
- Test on a real device with **airplane mode on** — everything except multiplayer must work.
- Test the first launch on a clean install (no `localStorage`) — that's the reviewer's experience.
- Confirm safe-area insets on a notched device (already handled in CSS, but verify).
- Multiplayer is the one legitimately-remote feature. Make sure the game degrades gracefully
  with no network rather than hanging.

**Store strategy**
- **TestFlight first.** Internal testing skips full review and exercises the whole signing and
  upload pipeline while the stakes are zero.
- **Unlisted App Distribution** (request from Apple) publishes the app so it's reachable only by
  direct link — not in search, browse or charts. That's the way to be "quietly live".
- Ratings can be **reset** when you release a new version, so early rough reviews aren't permanent.
- Avoid the words *beta*, *demo* or *trial* in store metadata — that's a Guideline 2.1 rejection.
  Ship it as v1.0 of a real game, not as a preview.

**Google Play note:** new personal developer accounts must run a closed test with 12 testers for
14 continuous days before they can promote to production. Start that clock early.

Apple's rules move around — re-check the current App Review Guidelines before submitting.
