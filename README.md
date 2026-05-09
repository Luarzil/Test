# Family Shopping Assistant

This is a single-file app (`index.html`) you can run in any modern browser.

## Easiest way to use it on your phone (no coding required)

## Option A (Fastest): use the new in-app download button
1. Open the app in your browser.
2. Tap **Download App File**.
3. Send that downloaded `.html` file to your phone.
4. Open it in Chrome/Safari.

## Option B: open the file directly
1. On your computer, open this folder and locate `index.html`.
2. Email `index.html` to yourself (or AirDrop/Google Drive it).
3. On your phone, download the file.
4. Open it in Chrome (Android) or Safari (iPhone).

> Note: Some phone browsers make local files awkward. If that happens, use Option B.

## Option C (Recommended): host it free with GitHub Pages
1. Create a GitHub account (if needed).
2. Create a new repository, e.g. `shopping-assistant`.
3. Upload `index.html` to that repo.
4. In the repo, go to **Settings → Pages**.
5. Under **Build and deployment**, choose:
   - Source: **Deploy from a branch**
   - Branch: **main** and folder **/** (root)
6. Save, wait 1-2 minutes.
7. GitHub gives you a URL like:
   `https://YOURNAME.github.io/shopping-assistant/`
8. Open that URL on your phone.
9. In mobile browser menu, tap **Add to Home Screen**.

Now it behaves like an app.

## Run it locally on your computer (optional)
If you want to test first:

```bash
python3 -m http.server 8080
```

Then open:
- `http://localhost:8080` on your computer
- or `http://YOUR_COMPUTER_IP:8080` on phone (same Wi-Fi)

## How your wife can use the same list
This version is private/local. There is no cloud account backend.

You can still sync manually:
1. On phone A: tap **Export JSON**.
2. Share that file to phone B.
3. On phone B: tap **Import JSON**.

## Files
- `index.html` – the app
