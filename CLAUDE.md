# CLAUDE.md — Projektkontext „Tagesprotokoll"

Diese Datei ist der Wissensspeicher für Claude-Code-Sitzungen.
**Sie wird zuerst gelesen** — alles, was hier steht, ist sofort wieder verfügbar.

Sprache: Der Nutzer kommuniziert auf Deutsch. Antworten bitte auf Deutsch.

---

## 1. Was ist das?

Eine **Progressive Web App** für ein Tagesprotokoll (vermutlich Handwerk/Hygiene).
Eine einzige HTML-Datei (`index.html`) mit Inline-CSS und -JS, plus Service Worker
(`sw.js`) und Web-App-Manifest (`manifest.json`). Hosting: **GitHub Pages auf
`main`** — jeder Push auf `main` geht **sofort live**.

Live-URL: https://jgc-coding.github.io/Tagesprotokoll-/

Repo: `jgc-coding/tagesprotokoll-` (Remote-Zugriff nur auf diese Repo erlaubt).

---

## 2. Funktionsumfang (Stand jetzt)

- Einträge schreiben (Textarea mit Auto-Resize), Zeitstempel automatisch.
- **Schnellauswahl-Chips** über dem Eingabefeld; in den Einstellungen
  beliebig **hinzufügbar / löschbar / sortierbar**, persistiert in
  `localStorage['proto_quick']`. Defaults siehe `QUICK_DEFAULT` in `index.html`:
  `Ende der vorherigen Aktion`, `Wasserhahn an`, `Wasserhahn aus`,
  `Eigene Hände waschen`, `Tür aufmachen`, `Boden wischen`.
- **Diktat (Online)**: MediaRecorder → Groq-API `whisper-large-v3`.
  API-Key über die Einstellungen *oder* per Langdruck aufs Mikro.
  Gespeichert in `localStorage['groq_api_key']`.
- **Export**: Markdown, PDF (via Browser-Druckdialog), TXT (mit UTF-8 BOM).
- **Archiv** (IndexedDB `proto_db`, Store `exports`): jeder Export wird
  automatisch dort abgelegt; Liste mit Öffnen/Löschen.
- **Backup/Restore**: in den Einstellungen JSON-Datei
  herunterladen / wieder einlesen (Einträge, Schnellauswahl, Theme).
- **Ordner-Auto-Sicherung**: nur wo `window.showDirectoryPicker` existiert
  (Desktop-Chrome/Edge). Handle wird in IndexedDB `proto_fs` Store `kv`
  unter Key `dir` gespeichert. Schreibt bei jedem `save()` automatisch
  `tagesprotokoll-backup.json` in den gewählten Ordner.
- **Theme**: hell / dunkel / automatisch (folgt `prefers-color-scheme`),
  persistiert in `localStorage['proto_theme']`. Bootstrap-Skript im `<head>`
  setzt `data-theme` früh, damit nichts aufblitzt.
- **Einträge bearbeiten/löschen**: Langdruck (~500 ms) auf einen Eintrag
  öffnet ein Aktions-Fenster mit *Bearbeiten* und *Löschen*. Kein festes ✕.
- **Zeitstrahl-Optik**: Einträge an einer durchgehenden Linie mit Punkten
  (`.entry::before`/`::after`), Zeit links, Text rechts.
- **PWA**: Service Worker mit network-first für HTML, cache-first für Assets.

---

## 3. Design-Entscheidungen

**Gewählte Variante: warm** (siehe `preview/b-warm.html`).
Farbpalette (Gelb/Creme/Salbei/Hellgrün/Blau aus einer Inspirations-Vorlage):

| Rolle           | Hell (Standard)             | Dunkel                       |
|-----------------|-----------------------------|------------------------------|
| `--bg`          | `#f6f0d8` (Creme)           | `#1b201a`                    |
| `--paper`       | `#fffdf4`                   | `#262c22`                    |
| `--ink`         | `#3c5538`                   | `#e9ecdb`                    |
| `--muted`       | `#86926f`                   | `#8c977a`                    |
| `--accent`      | `#5e8159` (Salbei)          | `#9cc06f`                    |
| `--accent-soft` | `#b0cd7f` (Hellgrün)        | s.o.                         |
| `--warm`        | `#ead36a` (Gelb)            | gleich                       |
| `--danger`      | `#b5654a` (Terracotta)      | `#d98b6f`                    |
| `--line`        | `#e6ddba`                   | `#39402f`                    |

- Fonts: **Fraunces** (Headlines), **DM Mono** (Body/Zeiten) — von Google Fonts.
- Eingabezeile bewusst groß (`min-height: 5.5rem`, Mikro/＋ `3rem`).
- Topbar transparent, weicher gelber Lichtschein oben
  (`radial-gradient` mit `--glow`).

**Verworfene Varianten** (liegen noch unter `/preview/`):
`a.html` (Sonnenaufgang), `b.html` (Mitternacht dunkel), `b-hell.html`
(Mitternacht hell), `c.html` (Karten). Können entfernt werden, wenn sie
nicht mehr gebraucht werden.

---

## 4. Wichtige Datei-Strukturen

- **`index.html`** — ganze App, ~1700 Zeilen.
  - `<head>`: Theme-Bootstrap-IIFE direkt nach `<style>`.
  - 1. `<script>`: Groq-Helfer (Endpoint, Key-Storage, `transcribeViaGroq`).
  - 2. `<script>` (Hauptskript): State, Clock, Save, Add/Render/Delete,
    Archiv, Export, Mic, View-Toggle, Init.
  - 3. `<script>` (Settings/Theme/Backup/Long-Press): alles, was später
    dazukam. Greift via globalem `let`/`function`-Scope auf das Hauptskript zu.
- **`sw.js`** — Service Worker. **Cache-Konstante (`CACHE`) bei jeder
  Asset-Änderung hochzählen**, sonst bleiben alte Icons/Assets gecached.
- **`manifest.json`** — PWA-Manifest. `theme_color: #5e8159`,
  `background_color: #f6f0d8`. Icons als `"any maskable"`.
- **`icon-192.png` / `icon-512.png`** — Salbei-Verlauf mit Zeitstrahl-Motiv,
  generiert mit `make_icons.py` (PIL). Reproducible: einfach
  `python3 make_icons.py` ausführen.
- **`preview/`** — alte Design-Prototypen (siehe oben). Nur Mockups, keine Logik.

---

## 5. Versionierung beim Deploy

Bei jedem Push, der Code/Assets verändert, **beide hochzählen**:

- `index.html` → `const APP_VERSION = N;` (zeigt sich in der Fußzeile als `vN`)
- `sw.js`      → `const CACHE = 'protokoll-vN';`

Aktueller Stand: **APP_VERSION 13, CACHE `protokoll-v11`** (Stand nach
Commit `b80bc70`).

HTML wird per network-first geladen → App-Updates kommen sofort an.
Andere Assets (Icons, Manifest, sw.js) liegen im Cache; deshalb die
Versionierung.

---

## 6. Nutzer-Kontext

- **Gerät**: hauptsächlich **Android-Handy** (Chrome).
  → Folder-Auto-Backup über File System Access API **funktioniert dort nicht**
  (zeigt automatisch nur die manuelle Backup-Datei-Option).
- E-Mail: `kontakt@jgc-handwerk.de`.
- Nutzer hat schon einmal selbst gepushed (`v11` lief) — der Workflow
  ist etabliert. Live-Push erwünscht.
- Sehr pragmatischer Ton, will klare Vorschläge + ehrliche Hinweise zu
  Grenzen (z.B. Android-Einschränkungen).

---

## 7. Was als Nächstes anstehen könnte

Vom Nutzer in einer früheren Antwort angefragt / von mir als sinnvoll
vorgeschlagen (noch offen):

- **Hinweis-Tooltip** für den Langdruck (Bearbeiten ist aktuell nicht
  selbsterklärend) — Nutzer hatte das als offene Frage stehen.
- **Sicherheitsabfrage beim Löschen** im neuen Aktions-Fenster: ja/nein —
  offene Frage an den Nutzer.
- **Dauer zwischen Einträgen** automatisch anzeigen (passt zur
  Schnellauswahl „Ende der vorherigen Aktion").
- **Suchen/Filtern** in den Einträgen.
- **Foto pro Eintrag** anhängen.
- **Mehrere Schnellauswahl-Sets** (z.B. je Baustelle/Kunde umschaltbar).

---

## 8. Konventionen / Stolperfallen

- **`localStorage`-Keys** (alle Strings):
  - `proto_v2`        — Einträge (Array)
  - `proto_quick`     — Schnellauswahl-Labels
  - `proto_theme`     — `light` / `dark` / `auto`
  - `groq_api_key`    — Groq-API-Key
- **IndexedDB**:
  - DB `proto_db`, Store `exports` — Export-Archiv
  - DB `proto_fs`,   Store `kv`     — Ordner-Handle für Auto-Backup
- **Cross-Skript-Zugriff**: Top-Level `let`/`const`/`function` in klassischen
  Scripts liegen im gemeinsamen globalen Lexical Scope; Settings-Skript greift
  bewusst direkt auf `entries`, `QUICK`, `save`, `renderAll`, `esc`, `download`,
  `todayStamp` aus den anderen Skript-Blöcken zu. Reassignments
  (`entries = data.entries`) funktionieren über Scripts hinweg, weil dasselbe
  Binding adressiert wird.
- **Vor jedem Commit**: JS-Syntax-Check und Inline-Handler-Prüfung:
  ```bash
  node -e 'const fs=require("fs");const h=fs.readFileSync("index.html","utf8");
    const re=/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi;let m,c="";
    while((m=re.exec(h))){c+=";{ "+m[1]+"\n}\n"}
    try{new Function(c);console.log("OK")}catch(e){console.error(e.message);process.exit(1)}'
  for fn in $(grep -oE 'onclick="[a-zA-Z_]+\(' index.html | sed -E 's/onclick="//; s/\(//' | sort -u); do
    grep -qE "function $fn\b" index.html && echo "ok $fn" || echo "FEHLT $fn"
  done
  ```
- **Kein Browser-Test im Container** möglich. Wenn UI-Änderungen drin sind,
  dem Nutzer das ehrlich sagen und um Quertest auf dem Handy bitten.
- **Android-Icon-Cache** ist hartnäckig: nach Icon-Änderung muss die App
  vom Startbildschirm entfernt und neu „Zum Startbildschirm hinzufügen"
  werden, sonst bleibt das alte Icon.
- **Branch-Policy**: Setup nennt zwar einen Feature-Branch
  `claude/improve-protocol-export-h9rRp`, der Nutzer arbeitet aber direkt
  auf `main` und wünscht Live-Pushes. Im Zweifel bei größeren Eingriffen
  trotzdem kurz nachfragen.

---

## 9. Letzte Commits (Kontext für Folge-Arbeiten)

```
b80bc70 Add timeline rail, long-press edit/delete, and warm app icons
f197218 Adopt warm design in live app + add Settings (theme, quick-select, backup)
d355670 Add warm Mitternacht variant from yellow/sage/blue palette
edafbb3 Add light-background Mitternacht variant with dark/light toggle
87d59e6 Rework Mitternacht preview: green palette, fix bullet/text overlap, taller input
b5e915e Add design prototypes under /preview/ (does not touch the app)
```
