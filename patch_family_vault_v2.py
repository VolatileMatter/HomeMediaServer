#!/usr/bin/env python3
"""
patch_family_vault_v2.py
========================
Supersedes patch_family_vault.py (assume it has NOT been run yet).
Run this single script instead of the old one.

Changes applied
───────────────
PART A — raspi.html & services.json (from previous patch)
  A1. raspi.html: Philosophy callout in Overview tab
  A2. raspi.html: Electricity table — annual saving row + footnote
  A3. raspi.html: AI Recommender note in Storage cross-machine section
  A4. raspi.html: Watchtower section in Maintenance tab
  A5. services.json: Watchtower entry added before Portainer

PART B — raspi.html nav move
  B1. index.html: Move raspi nav item from wherever it is into the
      Setup / Infrastructure group so it appears in the setup section.
      (The grimoire uses a sidebar nav with group headers — raspi.html
      currently lives under the Infrastructure group. We move it to
      appear directly under a "Setup" or "Hardware" group, before
      the services group.)

PART C — Pi compatibility section on every service setup tab
  For every HTML file that has a setup pane, inject a
  🍓 Pi Sentry Compatibility callout block immediately after the
  setup-complete-bar. The block is tailored per file with the
  correct verdict (Pi-capable / PC-only / already on Pi).

Run from the Grimoire root directory:
    python patch_family_vault_v2.py

Backups are written as <filename>.<timestamp>.bak before any modification.
The script is idempotent — if the Pi callout is already present it skips.
"""

import re, shutil, sys
from pathlib import Path
from datetime import datetime

ROOT = Path(".")

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def backup(path: Path):
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = path.with_suffix(f".{stamp}.bak")
    shutil.copy2(path, bak)

def load(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def save(path: Path, content: str):
    path.write_text(content, encoding="utf-8")

def patch_str(content: str, old: str, new: str, label: str, path: Path) -> str:
    if old not in content:
        print(f"  [SKIP] {path.name}: anchor not found — {label}")
        return content
    if content.count(old) > 1:
        print(f"  [WARN] {path.name}: anchor matches {content.count(old)}× — {label}")
    return content.replace(old, new, 1)

def already_patched(content: str) -> bool:
    return 'pi-compat-callout' in content


# ─────────────────────────────────────────────────────────────────────────────
# PI COMPATIBILITY CALLOUT GENERATOR
# ─────────────────────────────────────────────────────────────────────────────

def pi_callout(verdict: str, already_on_pi: bool, reason: str) -> str:
    """
    verdict: 'pi'   — can run on Pi (not currently there)
             'pc'   — must stay on PC
             'here' — already deployed on Pi
    reason: short explanation string (HTML safe)
    """
    if already_on_pi:
        color   = "rgba(76,175,125,.12)"
        border  = "rgba(76,175,125,.35)"
        icon    = "🍓"
        badge   = '<span style="background:rgba(76,175,125,.2);color:#4caf7d;font-family:\'Share Tech Mono\',monospace;font-size:.62rem;padding:2px 8px;border-radius:3px;letter-spacing:.08em">RUNNING ON PI</span>'
        verdict_text = "This service is already deployed on the Pi Sentry."
    elif verdict == 'pi':
        color   = "rgba(76,175,125,.07)"
        border  = "rgba(76,175,125,.25)"
        icon    = "🍓"
        badge   = '<span style="background:rgba(76,175,125,.12);color:#4caf7d;font-family:\'Share Tech Mono\',monospace;font-size:.62rem;padding:2px 8px;border-radius:3px;letter-spacing:.08em">PI-CAPABLE</span>'
        verdict_text = "Can be migrated to the Pi Sentry if the PC is decommissioned or to reduce Windows load."
    else:  # pc-only
        color   = "rgba(200,100,80,.07)"
        border  = "rgba(200,100,80,.25)"
        icon    = "💪"
        badge   = '<span style="background:rgba(200,100,80,.12);color:#e05c5c;font-family:\'Share Tech Mono\',monospace;font-size:.62rem;padding:2px 8px;border-radius:3px;letter-spacing:.08em">PC ONLY</span>'
        verdict_text = "Cannot run on the Pi Sentry — must stay on the Windows PC."

    return f'''
  <!-- ── Pi Sentry Compatibility ── -->
  <div class="pi-compat-callout" style="display:flex;align-items:flex-start;gap:14px;background:{color};border:1px solid {border};border-radius:4px;padding:14px 18px;margin-bottom:20px">
    <div style="font-size:1.4rem;flex-shrink:0">{icon}</div>
    <div style="flex:1">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">
        <span style="font-family:\'Share Tech Mono\',monospace;font-size:.7rem;text-transform:uppercase;letter-spacing:.1em;color:var(--text)">Pi Sentry Compatibility</span>
        {badge}
      </div>
      <p style="margin:0 0 4px;font-size:.83rem;line-height:1.5;color:var(--text)">{verdict_text}</p>
      <p style="margin:0;font-size:.8rem;line-height:1.5;color:var(--text-dim)">{reason}</p>
    </div>
  </div>

'''


# ─────────────────────────────────────────────────────────────────────────────
# PER-FILE PI COMPATIBILITY DATA
# Maps html filename → (verdict, reason, already_on_pi)
# ─────────────────────────────────────────────────────────────────────────────
# verdict: 'pi' = can run on Pi | 'pc' = must stay on PC | (use already_on_pi=True for deployed)
# Shared tabFiles (e.g. seedbox.html covers qbittorrent/sonarr/radarr/readarr/prowlarr) get one entry.

FILE_COMPAT = {
    # ── Media ──────────────────────────────────────────────────────────────
    "movies.html": (
        "pc", False,
        "Jellyfin requires NVENC/NVDEC hardware transcoding (GTX 1070 Ti) to serve 1080p to multiple "
        "TVs simultaneously. CPU-only transcoding on the Pi 5 produces unwatchable stuttering at "
        "1080p. Stays on the PC permanently."
    ),
    "calibre.html": (
        "pi", False,
        "Calibre-Web is a lightweight Python app with no GPU dependency. It runs comfortably on "
        "the Pi 5's 16GB of RAM. Migration would move the app and library to /mnt/archive/Books/, "
        "with Caddy proxying to the Pi's Tailscale IP."
    ),
    "audiobooks.html": (
        "pi", True,
        "Audiobookshelf is already deployed on the Pi Sentry. It runs as a Docker container at "
        "port 13378, serving audiobooks and podcasts 24/7 from /mnt/archive/Audiobooks/."
    ),
    "navidrome.html": (
        "pi", False,
        "Navidrome is a lightweight Go binary with very low resource usage (~50MB RAM). It can "
        "run on the Pi 5 with music served from /mnt/archive/Music/. Currently on the PC for "
        "convenience, but migration is straightforward."
    ),
    "immich.html": (
        "pc", False,
        "Immich relies on GPU-accelerated machine learning (face detection, CLIP embeddings, object "
        "recognition) for its Smart Search and People features. The Pi 5 has no GPU — ML inference "
        "falls back to CPU only, which takes hours per batch instead of minutes."
    ),
    "kavita.html": (
        "pi", True,
        "Kavita (Comics) is already deployed on the Pi Sentry at port 5000 with the comics library "
        "at /mnt/archive/Comics/. The DnD instance (port 5001) is configured but data migration from "
        "the PC is pending — move /mnt/archive/DnD/ to the Pi and update the Caddy block."
    ),
    "owncloud.html": (  # Nextcloud
        "pi", True,
        "Nextcloud is already deployed on the Pi Sentry as a Docker container at port 8080, serving "
        "cloud storage from /mnt/archive/. The Pi's 24/7 uptime makes it the ideal host — files are "
        "always accessible even when the PC is off."
    ),
    "invidious.html": (
        "pi", False,
        "Invidious is a Docker-based Go application with moderate CPU usage during video proxying. "
        "The Pi 5 can handle it for light household use, but video proxy throughput may be lower "
        "than on the PC. A viable migration for low-traffic use."
    ),
    "tunarr.html": (
        "pi", False,
        "Tunarr is a Node.js server that schedules and serves channel streams. It can run on the "
        "Pi 5, but the channel filler content (downloaded by meTube) currently lives on the PC's "
        "local storage. Migration requires moving filler folders to the archive drive."
    ),
    "streamarr.html": (
        "pc", False,
        "Streamarr runs inside a Mullvad VPN network namespace (Gluetun in WSL2) which is tightly "
        "coupled to the Windows/WSL2 environment on the PC. Replicating the Gluetun namespace setup "
        "on Pi OS is possible but adds significant complexity with no clear benefit."
    ),

    # ── Apps ───────────────────────────────────────────────────────────────
    "ollama.html": (
        "pc", False,
        "Ollama requires a GPU for usable inference speeds. The GTX 1070 Ti runs a 7B model at "
        "~50–80 tokens/second. The Pi 5 CPU would produce ~2–4 tokens/second — unusable for "
        "real conversation. Open WebUI stays co-located with Ollama on the PC."
    ),
    "recommendations.html": (
        "pc", False,
        "The Recommendations API delegates its actual inference to Ollama. Since Ollama must stay "
        "on the PC (GPU requirement), this service stays co-located. It scans the Z:\\ drive "
        "(Pi's archive) for book and media context, but runs on the PC."
    ),
    "excalidraw.html": (
        "pi", False,
        "Excalidraw is a stateless Docker container — it serves static assets and has no persistent "
        "data or server-side computation. Runs comfortably on the Pi 5. Low priority migration since "
        "it works fine on the PC."
    ),
    "readeck.html": (
        "pi", False,
        "Readeck is a lightweight Go application that fetches and stores clean article copies. "
        "Per-user Docker instances are modest in RAM. Viable Pi migration, though article fetching "
        "throughput depends on Pi's network and CPU."
    ),
    "privatebin.html": (
        "pi", False,
        "PrivateBin is a PHP application with minimal resource requirements — it just stores "
        "encrypted blobs on disk. Trivially easy to run on the Pi 5 via Docker."
    ),
    "stirling.html": (
        "pi", False,
        "Stirling-PDF is a Java/Docker application for PDF processing. OCR tasks are CPU-intensive "
        "but the Pi 5's ARM Cortex-A76 cores handle them adequately. Migration is straightforward. "
        "Expect slower OCR processing than on the PC for large documents."
    ),
    "upscayl.html": (
        "pi", False,
        "Upscayl's web version performs all upscaling client-side in the browser via WASM — the "
        "server just serves static files. Essentially zero Pi compute required. Easy migration."
    ),
    "pxls.html": (
        "pi", False,
        "Pxls is a Java application with PostgreSQL and Redis dependencies, all running in Docker. "
        "Moderate memory footprint (~300–600 MB total). The Pi 5's 16GB RAM handles it comfortably."
    ),
    "genart.html": (
        "pi", False,
        "Generative Art is a static file server (Python http.server). The Pi serves files equally "
        "well as the PC. All computation is client-side in the browser. Trivial migration."
    ),
    "hoarder.html": (
        "pc", False,
        "Hoarder uses a headless Chromium instance for full-page snapshots. arm64 Chromium on "
        "Pi OS has a history of instability and crashes (noted during research). Stays on the PC "
        "until arm64 Chromium reliability improves."
    ),
    "mealie.html": (
        "pi", False,
        "Mealie is a lightweight Python/Docker web application. Very low resource usage. The Pi 5 "
        "handles it easily. Viable migration — data lives in a small SQLite/Postgres database."
    ),
    "utilities.html": (
        "pi", False,
        "Vikunja and Uptime Kuma are both lightweight Docker applications with negligible resource "
        "requirements. Both can run on the Pi 5. Uptime Kuma is a natural fit since the Pi is always "
        "on — it can monitor the PC's online status and alert when the PC goes down unexpectedly."
    ),
    "languages.html": (
        "pi", False,
        "LinguaCafe (Docker), Anki Sync Server, and LibreLingo are all lightweight web applications "
        "with minimal compute requirements. All viable Pi migrations. LinguaCafe's NLP processing "
        "is modest enough for the Pi 5's ARM cores."
    ),
    "jukebox.html": (
        "pi", False,
        "Jukebox is a small custom Python/Flask application serving static Web Audio API content. "
        "Negligible resource usage — well within Pi 5 capabilities."
    ),
    "monica.html": (
        "pi", False,
        "Monica is a PHP/Docker application backed by MySQL. Lightweight and stateless in compute. "
        "The AI inbox feature delegates to Ollama on the PC — so Monica can run on the Pi while "
        "still calling the PC's Ollama endpoint over the Tailscale network."
    ),
    "wikipedia.html": (
        "pi", False,
        "Kiwix is a lightweight Go application serving ZIM files. The Pi 5's 16GB RAM and the "
        "archive drive's storage capacity make it an ideal host — Kiwix would benefit from being "
        "always-on since offline Wikipedia is most useful when the PC isn't running."
    ),
    "vaultwarden.html": (
        "pi", False,
        "Vaultwarden is a Rust application with very low resource usage (~30–80 MB RAM). "
        "It benefits from 24/7 uptime since password access shouldn't depend on the PC being on. "
        "High-value migration candidate."
    ),
    "security.html": (
        "pc", False,
        "IPBan and Vaultwarden share this tab. IPBan monitors the Windows Event Log — it is "
        "Windows-specific and cannot run on the Pi. Authentik and Caddy (also in this tab) are "
        "the authentication hub for all services; migrating them would require re-routing all "
        "service traffic and is not planned."
    ),
    "sso.html": (
        "pc", False,
        "Authentik is the SSO hub for the entire server. It must co-locate with Caddy on the PC "
        "since Caddy's forward_auth calls happen at the reverse proxy layer. Separating them would "
        "add a cross-node hop to every authenticated request."
    ),
    "domain.html": (
        "pc", False,
        "Caddy runs on the PC as the TLS-terminating reverse proxy for all *.ixo.lol subdomains "
        "over Tailscale. Moving it to the Pi would require routing all traffic through the Pi, which "
        "would break the smart-plug power model (Pi controls PC power; Caddy must be up when the Pi "
        "is up)."
    ),

    # ── Gaming ─────────────────────────────────────────────────────────────
    "romm.html": (
        "pi", True,
        "RomM is already deployed on the Pi Sentry at port 8098, serving the unified ROM catalog "
        "from /mnt/archive/Roms/. The PC's Xenia folder is cross-mounted read-only so Xbox 360 "
        "titles appear in the catalog even when served from the PC."
    ),
    "emulatorjs.html": (
        "pi", True,
        "EmulatorJS is already deployed on the Pi Sentry at port 8085. ROMs are served from "
        "/mnt/archive/Roms/. Per-user save files are managed by the Flask save server. All "
        "emulation runs client-side in the browser — the Pi only serves static assets."
    ),
    "flasharcade.html": (
        "pi", False,
        "Flash Arcade is a static file server (nginx + Docker) with Ruffle WASM handling all "
        "emulation in the browser. The Pi 5 serves static files just as well as the PC. "
        "Straightforward migration."
    ),
    "vtt.html": (
        "pi", False,
        "Foundry VTT is a Node.js application. It has moderate RAM usage (~300MB–1GB depending on "
        "world complexity and loaded modules). The Pi 5's 16GB RAM handles it comfortably. "
        "Migration would move world data and assets to /mnt/archive/."
    ),
    "mtg.html": (
        "pi", False,
        "The MTG Deck Server is a custom lightweight Python/Flask service. Minimal resource usage. "
        "Easy Pi migration — deck files would live at /mnt/archive/MTG/ and be accessible via "
        "the SMB share."
    ),
    "wordle.html": (
        "pi", False,
        "The custom Wordle is a small Docker container (~50MB). The Pi 5 handles it trivially. "
        "scores.json would move to /mnt/archive/Docker/wordle/."
    ),
    "minecraft.html": (
        "pi", False,
        "Vanilla Minecraft Java server can run on the Pi 5 for small player counts (2–4 players). "
        "Modded Minecraft is more demanding and may struggle on the Pi's ARM cores with heavy mod "
        "packs. Recommend keeping modded on the PC and only considering Vanilla for Pi."
    ),
    "ark.html": (
        "pc", False,
        "ARK: Survival Evolved requires 6–10 GB RAM and high CPU performance. The Pi 5 cannot "
        "provide the compute or RAM needed for a playable ARK server. PC-only."
    ),
    "ss13.html": (
        "pi", False,
        "Space Station 13 (BYOND) has a very small footprint (~200–400 MB RAM). BYOND's DMAPI "
        "is available for Linux arm64 and should run on the Pi 5. A viable migration for "
        "this niche service."
    ),
    "gamecube.html": (
        "pc", False,
        "Dolphin (GameCube/Wii emulator) requires a high-performance x86 CPU and GPU for "
        "accurate emulation at full speed. ARM emulation on the Pi 5 is not supported by Dolphin. "
        "Streamed via Sunshine — PC-only permanently."
    ),
    "xbox360.html": (
        "pc", False,
        "Xenia (Xbox 360 emulator) requires x86-64 architecture and a discrete GPU. There is no "
        "ARM port of Xenia. PC-only permanently, streamed via Sunshine."
    ),
    "sims2.html": (
        "pc", False,
        "The Sims 2 is a DirectX/Windows game streamed via Sunshine. It requires the GTX 1070 Ti "
        "for smooth rendering. PC-only permanently."
    ),
    "fireemblem.html": (
        "pc", False,
        "Fire Emblem games run via Dolphin (GameCube/Wii emulator). See GameCube tab — same GPU and "
        "x86 architecture constraints apply. PC-only, streamed via Sunshine."
    ),
    "marioparty.html": (
        "pc", False,
        "Mario Party runs via Dolphin. Same constraints as GameCube/Wii — x86 architecture and GPU "
        "required. PC-only, streamed via Sunshine."
    ),
    "pokemon.html": (
        "pi", True,
        "Pokemon (GBA/NDS) runs entirely in the browser via EmulatorJS, which is already deployed "
        "on the Pi Sentry. All emulation is client-side WASM. The Pi serves ROM files and save "
        "states from /mnt/archive/Roms/."
    ),
    "castlevania.html": (
        "pi", True,
        "Castlevania games (NES/SNES/GBA/NDS) run via EmulatorJS, already on the Pi Sentry. "
        "Browser-based emulation with client-side WASM — the Pi only serves static assets and saves."
    ),
    "goglibrary.html": (
        "pc", False,
        "GOG games (Divinity, Zoo Tycoon, Warlords) are DirectX/Windows applications streamed via "
        "Sunshine. They require the PC's GPU for rendering. PC-only permanently."
    ),
    "steam.html": (
        "pc", False,
        "Steam library games require the PC's GPU, Windows, and often DirectX. Streamed via "
        "Sunshine. PC-only permanently."
    ),
    "sunshine.html": (
        "pc", False,
        "Sunshine is a game streaming host that uses NVENC (NVIDIA GPU) for hardware-accelerated "
        "video encoding. The Pi 5 has no NVENC equivalent. PC-only permanently."
    ),

    # ── Downloads ──────────────────────────────────────────────────────────
    "seedbox.html": (
        "pi", False,
        "qBittorrent, Sonarr, Radarr, Readarr, and Prowlarr are all lightweight *arr-stack services "
        "that run well on the Pi 5. Moving the seedbox to the Pi would let downloads run 24/7 "
        "without needing the PC on. The 15TB archive drive is already where completed files land. "
        "Note: qBittorrent's Mullvad VPN binding would need to be re-configured for Pi OS."
    ),

    # ── Infrastructure ─────────────────────────────────────────────────────
    "dashsetup.html": (
        "pc", False,
        "The Stats Agent and Control Server are custom Python services deeply integrated with "
        "Windows — they query Windows performance counters, manage Windows services, and interact "
        "with the dashboard. They are Windows-specific and cannot run on the Pi."
    ),
    "dashboard.html": (
        "pc", False,
        "Netdata monitors system performance metrics from the Windows host. It is installed as a "
        "native Windows service and cannot run on the Pi. A separate Netdata instance could be "
        "installed on the Pi for Pi-specific metrics, but the main dashboard monitors the PC."
    ),
    "achievements.html": (
        "pc", False,
        "The Achievement Server is a custom Python/Flask service that polls other services on the "
        "PC (Jellyfin, Navidrome, etc.) and receives webhooks from them. It must co-locate with "
        "those services on the PC to poll their local APIs reliably."
    ),
    "raspi.html": (
        "pi", True,
        "This page documents the Pi Sentry itself — the node that runs all Pi-deployed services. "
        "Portainer, Watchtower, and Docker management live here by definition."
    ),
}

# HTML files that should NOT get a Pi section (infra pages, the home page, etc.)
SKIP_FILES = {
    "index.html", "home.html", "overview.html", "hardware.html",
    "ports.html", "restarting.html", "memory.html", "best-practices.html",
    "services.html", "new-user.html", "monitor-control.html",
    "dashboard-setup.html", "user-homepage.html", "user-homepage-setup.html",
    "user-settings.html", "feedback.html", "linux.html",
    "service-template.html", "shared.css",
}

# ─────────────────────────────────────────────────────────────────────────────
# INJECTION LOGIC
# Insert Pi callout after the setup-complete-bar closing divs, before first
# <div class="v1-banner"> or first <div class="section"> inside pane-setup.
#
# Strategy: find id="pane-setup" then find the first </div> that ends the
# setup-complete-bar div (we detect by looking for id="complete-sub" closing).
# We insert right before the first <div class="v1-banner"> or <div class="section">
# that follows the setup-complete-bar.
# ─────────────────────────────────────────────────────────────────────────────

# Regex: matches the close of the setup-complete-bar block.
# We look for the complete-sub element closing (end of bar) then capture what follows.
SETUP_BAR_END_RE = re.compile(
    r'(id=["\']complete-sub["\'][^>]*>[^<]*</div>)'  # complete-sub inner div
    r'(\s*</div>)*'                                    # closing parent divs of the bar
    r'\s*\n(\s*</div>\s*\n)?'                         # optional outer wrapper close
    r'(\s*\n)?'
    r'(\s*<div class=["\']v1-banner["\'])',            # capture: v1-banner or section start
    re.DOTALL
)

# Simpler fallback: just look for the first <div class="v1-banner"> or
# <div class="section"> inside pane-setup.
BANNER_RE = re.compile(r'(<div class=["\']v1-banner["\'])')
SECTION_RE = re.compile(r'(<div class=["\']section["\'])')
HR_RE = re.compile(r'(<hr\s*/?>)')


def inject_pi_callout(html: str, callout: str, filename: str) -> tuple[str, bool]:
    """
    Inject the Pi callout into the setup pane.
    Returns (modified_html, was_modified).
    """
    if already_patched(html):
        return html, False

    # Find the pane-setup div
    pane_start = html.find('id="pane-setup"')
    if pane_start == -1:
        pane_start = html.find("id='pane-setup'")
    if pane_start == -1:
        return html, False

    # From pane_start, look for the first v1-banner or first <div class="section"> or <hr>
    search_zone = html[pane_start:]

    # Best injection point: right before the v1-banner
    m = BANNER_RE.search(search_zone)
    if m:
        insert_pos = pane_start + m.start()
        return html[:insert_pos] + callout + html[insert_pos:], True

    # Fallback: right before first <div class="section">
    m = SECTION_RE.search(search_zone)
    if m:
        insert_pos = pane_start + m.start()
        return html[:insert_pos] + callout + html[insert_pos:], True

    # Fallback 2: right before first <hr>
    m = HR_RE.search(search_zone)
    if m:
        insert_pos = pane_start + m.start()
        return html[:insert_pos] + callout + html[insert_pos:], True

    return html, False


# ─────────────────────────────────────────────────────────────────────────────
# PART A — raspi.html & services.json patches (from original patch)
# ─────────────────────────────────────────────────────────────────────────────

RASPI_FILE = ROOT / "raspi.html"
SERVICES_FILE = ROOT / "services.json"

PHILOSOPHY_ANCHOR = '''\
  <div class="section">
    <div class="section-title">📡 Quick Reference</div>'''

PHILOSOPHY_CARD = '''\
  <div class="section">
    <div class="section-title">🏛️ Family Digital Vault — Philosophy</div>
    <div class="grid-2">
      <div class="card">
        <div class="card-title">🛡️ Sovereignty</div>
        <p style="font-size:.84rem;line-height:1.6">No subscriptions. No "delisting" of content. No data mining. Every movie, game, book, and photo is owned outright and stored on hardware you control. Nothing disappears because a streaming deal expired.</p>
      </div>
      <div class="card">
        <div class="card-title">⚡ Efficiency</div>
        <p style="font-size:.84rem;line-height:1.6">The Pi Sentry (~10W) runs 24/7 and handles everything that doesn't need a GPU. The Windows PC (~200W) only powers on when someone wants Jellyfin or game streaming — cutting idle electricity to near zero overnight.</p>
      </div>
      <div class="card">
        <div class="card-title">📂 Organization</div>
        <p style="font-size:.84rem;line-height:1.6">Centralized libraries for all ages, accessible from any device on the network. One unified catalog for ROMs, one for movies, one for books — no scattered drives or duplicated folders.</p>
      </div>
      <div class="card">
        <div class="card-title">🔄 Longevity</div>
        <p style="font-size:.84rem;line-height:1.6">The Penta SATA HAT supports up to 5 drives. As the family's collection grows, slide in another HDD — no reinstall, no migration. Monthly cold-storage backups protect against drive failure.</p>
      </div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">📡 Quick Reference</div>'''

OLD_POWER_TABLE = '''\
  <div class="section">
    <div class="section-title">⚡ Smart Plug Architecture</div>
    <div class="card">
      <table>
        <tr><th>Device</th><th>Avg draw</th><th>Hours/day</th><th>Monthly cost (San Diego ~$0.33/kWh)</th></tr>
        <tr><td>Pi 5 + 2 HDDs (24/7)</td><td>~25W</td><td>24</td><td>~$6</td></tr>
        <tr><td>PC via smart plug (4 hrs/day)</td><td>~200W</td><td>4</td><td>~$8</td></tr>
        <tr><td>PC always-on 24/7</td><td>~150W idle</td><td>24</td><td>~$36</td></tr>
        <tr><td colspan="3"><strong>Monthly saving (smart plug vs always-on)</strong></td><td><strong>~$28</strong></td></tr>
      </table>
    </div>
  </div>'''

NEW_POWER_TABLE = '''\
  <div class="section">
    <div class="section-title">⚡ Smart Plug Architecture</div>
    <div class="card">
      <table>
        <tr><th>Device</th><th>Avg draw</th><th>Hours/day</th><th>Monthly cost (San Diego ~$0.33/kWh)</th></tr>
        <tr><td>Pi 5 + 2 HDDs (24/7)</td><td>~25W</td><td>24</td><td>~$6</td></tr>
        <tr><td>PC via smart plug (4 hrs/day)</td><td>~200W</td><td>4</td><td>~$8</td></tr>
        <tr><td>PC always-on 24/7</td><td>~150W idle</td><td>24</td><td>~$36</td></tr>
        <tr><td colspan="3"><strong>Monthly saving (smart plug vs always-on)</strong></td><td><strong>~$28/month</strong></td></tr>
        <tr><td colspan="3"><strong>Annual saving</strong></td><td><strong>~$250–$340/year</strong> <span style="color:var(--text-dim);font-size:.8em">†</span></td></tr>
      </table>
      <p style="font-size:.77rem;color:var(--text-dim);margin-top:8px">† Range reflects actual PC usage variance. At 4 hrs/day the saving is ~$336/year; at 2 hrs/day (light-use months) it narrows to ~$250/year. San Diego residential rate ~$0.33/kWh (Tier 1 SDG&amp;E, 2025).</p>
    </div>
  </div>'''

OLD_AI_ANCHOR = '''\
      <p>This adds ~1–3ms latency vs local disk and is completely fine for streaming.'''

NEW_AI_ANCHOR = '''\
      <p>The AI Recommender (Ollama + Open WebUI on the PC) also reads <code>Z:\\</code> — it scans the Books, Audiobooks, and Movies folders so its recommendations stay aware of what's actually in the family library without needing a separate sync step.</p>
      <p>This adds ~1–3ms latency vs local disk and is completely fine for streaming.'''

OLD_MAINTENANCE_SCHEDULE_END = '''\
  <div class="section">
    <div class="section-title">📊 Health Monitoring Commands</div>'''

NEW_WATCHTOWER_SECTION = '''\
  <div class="section">
    <div class="section-title">🐋 Optional: Watchtower (Automated Docker Updates)</div>
    <div class="card">
      <p>Watchtower monitors running Docker containers and automatically pulls updated images, then restarts containers with the new version. It's optional — this server prefers <strong>manual, deliberate updates</strong> — but can be useful for low-risk containers like EmulatorJS or Portainer where you want updates without SSH.</p>
      <div class="callout callout-warn" style="margin-top:10px">
        <div class="callout-icon">⚠️</div>
        <div class="callout-body"><strong>Use with caution.</strong> Auto-updates can break things silently — especially for services like Nextcloud or RomM that occasionally have breaking schema changes between versions. If you enable Watchtower, exclude critical services explicitly.</div>
      </div>
      <pre style="margin-top:12px"># Add to docker-compose.yml on the Pi (optional, disabled by default):

  watchtower:
    image: containrrr/watchtower:latest
    container_name: watchtower
    restart: unless-stopped
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      WATCHTOWER_SCHEDULE: "0 0 4 * * *"
      WATCHTOWER_LABEL_ENABLE: "true"
      WATCHTOWER_NOTIFICATIONS: stdout
      WATCHTOWER_CLEANUP: "true"

# To opt a container IN to Watchtower management:
# labels:
#   - "com.centurylinklabs.watchtower.enable=true"

# To opt OUT (when monitoring all by default):
# labels:
#   - "com.centurylinklabs.watchtower.enable=false"

# Dry-run to see what it would update:
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  containrrr/watchtower --run-once --dry-run</pre>
    </div>
  </div>

  <div class="section">
    <div class="section-title">📊 Health Monitoring Commands</div>'''

OLD_SERVICES_PORTAINER_ANCHOR = '''\
  {
    "id": "portainer",
    "name": "Portainer",
    "icon": "🐳",
    "tagline": "Docker management UI for the Pi Sentry.'''

NEW_SERVICES_WITH_WATCHTOWER = '''\
  {
    "id": "watchtower",
    "name": "Watchtower",
    "icon": "🐋",
    "tagline": "Optional Docker auto-updater for the Pi Sentry. Monitors container images and restarts with new versions on a schedule. Disabled by default — enable per-container via label. Pi 5 only.",
    "category": "infra",
    "port": null,
    "subdomain": null,
    "docker": true,
    "tabFile": "raspi",
    "storage": "<10 MB",
    "cpu": "Very low (runs briefly on schedule)",
    "ram": "20–40 MB",
    "gpu": false,
    "ssoMethod": "none",
    "lanOnly": true,
    "adminOnly": true
  },
  {
    "id": "portainer",
    "name": "Portainer",
    "icon": "🐳",
    "tagline": "Docker management UI for the Pi Sentry.'''

# ─────────────────────────────────────────────────────────────────────────────
# PART B — index.html: move raspi nav item into the Setup/Hardware section
# ─────────────────────────────────────────────────────────────────────────────
# Current nav groups in index.html include a "System" or "Infrastructure" group
# that has raspi. We want it in the setup/hardware group so it appears at top.
# Looking at the known nav structure, raspi is under a "System" nav group.
# We move it to appear right after the hardware nav item.
# The exact anchor is the raspi nav button line.

INDEX_FILE = ROOT / "index.html"

# Raspi nav button to move — remove from current location and insert after hardware
RASPI_NAV_BTN = '    <button class="nav-item" id="nav-raspi"          onclick="go(\'raspi\')"><span class="ni">🍓</span>Pi Sentry</button>'

# The hardware nav button — we insert raspi right after it
HARDWARE_NAV_BTN_LINE = '    <button class="nav-item" id="nav-hardware"       onclick="go(\'hardware\')"><span class="ni">💾</span>Hardware</button>'

HARDWARE_NAV_WITH_RASPI = '''    <button class="nav-item" id="nav-hardware"       onclick="go(\'hardware\')"><span class="ni">💾</span>Hardware</button>
    <button class="nav-item" id="nav-raspi"          onclick="go(\'raspi\')"><span class="ni">🍓</span>Pi Sentry</button>'''


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def run_part_a():
    print("\n══ PART A — raspi.html & services.json ══════════════════════")

    # raspi.html
    if not RASPI_FILE.exists():
        print(f"  [SKIP] raspi.html not found")
    else:
        backup(RASPI_FILE)
        html = load(RASPI_FILE)
        html = patch_str(html, PHILOSOPHY_ANCHOR, PHILOSOPHY_CARD,
                         "A1: Philosophy callout", RASPI_FILE)
        html = patch_str(html, OLD_POWER_TABLE, NEW_POWER_TABLE,
                         "A2: Electricity annual saving row", RASPI_FILE)
        html = patch_str(html, OLD_AI_ANCHOR, NEW_AI_ANCHOR,
                         "A3: AI Recommender note", RASPI_FILE)
        html = patch_str(html, OLD_MAINTENANCE_SCHEDULE_END, NEW_WATCHTOWER_SECTION,
                         "A4: Watchtower maintenance section", RASPI_FILE)
        save(RASPI_FILE, html)
        print(f"  [OK ] raspi.html")

    # services.json
    if not SERVICES_FILE.exists():
        print(f"  [SKIP] services.json not found")
    else:
        backup(SERVICES_FILE)
        svc = load(SERVICES_FILE)
        svc = patch_str(svc, OLD_SERVICES_PORTAINER_ANCHOR, NEW_SERVICES_WITH_WATCHTOWER,
                        "A5: Watchtower service entry", SERVICES_FILE)
        save(SERVICES_FILE, svc)
        print(f"  [OK ] services.json")


def run_part_b():
    print("\n══ PART B — index.html nav move ══════════════════════════════")

    if not INDEX_FILE.exists():
        print(f"  [SKIP] index.html not found")
        return

    html = load(INDEX_FILE)

    # Check if raspi nav button exists at all
    if RASPI_NAV_BTN not in html:
        print(f"  [SKIP] index.html: raspi nav button not found with expected text — check manually")
        return

    # Check if hardware button exists
    if HARDWARE_NAV_BTN_LINE not in html:
        print(f"  [SKIP] index.html: hardware nav button not found — check manually")
        return

    # Check if already moved (raspi btn appears right after hardware btn)
    if HARDWARE_NAV_WITH_RASPI in html:
        print(f"  [SKIP] index.html: raspi already adjacent to hardware — no change needed")
        return

    backup(INDEX_FILE)

    # Step 1: remove raspi button from its current location
    # It may have a newline before/after — strip carefully
    html = html.replace(RASPI_NAV_BTN + "\n", "", 1)
    if RASPI_NAV_BTN in html:  # fallback if no trailing newline
        html = html.replace(RASPI_NAV_BTN, "", 1)

    # Step 2: insert after hardware button
    html = html.replace(HARDWARE_NAV_BTN_LINE, HARDWARE_NAV_WITH_RASPI, 1)

    save(INDEX_FILE, html)
    print(f"  [OK ] index.html: raspi moved to hardware/setup section")


def run_part_c():
    print("\n══ PART C — Pi compatibility sections ═══════════════════════")

    # Collect all HTML files in the root directory
    html_files = sorted(ROOT.glob("*.html"))
    patched = 0
    skipped = 0
    missing = 0

    for html_path in html_files:
        fname = html_path.name
        if fname in SKIP_FILES:
            continue

        if fname not in FILE_COMPAT:
            # Unknown file — try to inject a generic placeholder if it has a setup pane
            html = load(html_path)
            if 'id="pane-setup"' not in html and "id='pane-setup'" not in html:
                continue  # No setup pane, skip silently
            if already_patched(html):
                skipped += 1
                continue
            print(f"  [WARN] {fname}: not in FILE_COMPAT — using generic placeholder")
            callout = pi_callout('pi', False, 'Pi compatibility not yet assessed for this service — update FILE_COMPAT in the patch script.')
            missing += 1
        else:
            verdict, on_pi, reason = FILE_COMPAT[fname]
            callout = pi_callout(verdict, on_pi, reason)

            html = load(html_path)
            if 'id="pane-setup"' not in html and "id='pane-setup'" not in html:
                skipped += 1
                continue
            if already_patched(html):
                skipped += 1
                continue

        new_html, modified = inject_pi_callout(html, callout, fname)
        if modified:
            backup(html_path)
            save(html_path, new_html)
            verdict_str, on_pi_val, _ = FILE_COMPAT.get(fname, ('?', False, ''))
            status = "RUNNING ON PI" if on_pi_val else verdict_str.upper()
            print(f"  [OK ] {fname} ({status})")
            patched += 1
        else:
            print(f"  [FAIL] {fname}: injection point not found — no v1-banner or section div")

    print(f"\n  Patched: {patched}  |  Already done / no setup pane: {skipped}  |  Missing from compat map: {missing}")


def main():
    # Verify we're in the right directory
    if not (ROOT / "index.html").exists() and not (ROOT / "services.json").exists():
        print("ERROR: Run this script from the Grimoire root directory.")
        sys.exit(1)

    run_part_a()
    run_part_b()
    run_part_c()

    print("\n✅ All patches complete.")
    print("   Review .bak files if anything looks wrong, then delete them.")
    print("   Spot-check a few HTML files to verify the Pi callout positioning.")


if __name__ == "__main__":
    main()
