/**
 * ╔══════════════════════════════════════════════════════════════════════╗
 * ║                 SERVER CONFIGURATION — config.js                    ║
 * ║                                                                      ║
 * ║  THE ONLY FILE YOU NEED TO EDIT for domain, port, and path changes. ║
 * ║  Every HTML page loads this. Every value flows from here.           ║
 * ║                                                                      ║
 * ║  Companion data files (same directory):                             ║
 * ║    services.json  — full service registry (catalogue, ports, tabs)  ║
 * ║    versions.json  — last confirmed working versions per service     ║
 * ║                                                                      ║
 * ║  USAGE IN HTML:                                                      ║
 * ║    <script src="config.js"></script>                                 ║
 * ║                                                                      ║
 * ║  JS:  CFG.domain  CFG.url('jellyfin')  CFG.ports.jellyfin          ║
 * ║       CFG.authentikAdmin  CFG.paths.caddyfile                       ║
 * ║       CFG.oidcIssuer('jellyfin')                                    ║
 * ║       await CFG.loadServices()  await CFG.getVersion('jellyfin')    ║
 * ║                                                                      ║
 * ║  HTML auto-render attributes (data-cfg):                            ║
 * ║    data-cfg="domain"                → yourdomain.com                ║
 * ║    data-cfg="url:jellyfin"          → https://jellyfin.yourdomain.com║
 * ║    data-cfg="local:jellyfin"        → http://localhost:8096          ║
 * ║    data-cfg="port:jellyfin"         → 8096                          ║
 * ║    data-cfg="path:users"            → D:\Users                      ║
 * ║    data-cfg="path:caddyfile"        → C:\caddy\Caddyfile            ║
 * ║    data-cfg="userpath"              → D:\Users\[username]           ║
 * ║    data-cfg="userpath:calibre"      → D:\Users\[username]\calibre   ║
 * ║    data-cfg="authentik-admin"       → https://auth.domain/if/admin/ ║
 * ║    data-cfg="authentik-base"        → https://auth.domain           ║
 * ║    data-cfg="authentik-api"         → https://auth.domain/api/v3   ║
 * ║    data-cfg="oidc-issuer:jellyfin"  → https://auth.domain/applic…  ║
 * ║    data-cfg="version:jellyfin"      → async from versions.json      ║
 * ╚══════════════════════════════════════════════════════════════════════╝
 */

const CFG = {

  // ── YOUR DOMAIN ─────────────────────────────────────────────────────────
  // Change this ONE value. Every URL across every page updates automatically.
  domain: 'yourdomain.com',

  // ── SUBDOMAINS ───────────────────────────────────────────────────────────
  // Maps service keys to subdomain prefix.
  // Full external URL = https://[subdomain].[domain]
  // Keep in sync with services.json subdomain fields.
  subdomains: {
    home:             'home',
    auth:             'auth',
    jellyfin:         'jellyfin',
    calibre:          'books',
    audiobooks:       'audio',
    navidrome:        'music',
    immich:           'photos',
    nextcloud:        'cloud',
    vaultwarden:      'vault',
    kavita:           'comics',
    kavita_dnd:       'dnd',
    status:           'status',
    excalidraw:       'draw',
    stirling:         'pdf',
    upscayl:          'upscayl',
    readeck:          'read',
    linguacafe:       'lingua',
    anki:             'anki',
    librelingo:       'lingo',
    openwebui:        'ai',
    vikunja:          'tasks',
    mealie:           'recipes',
    uptime:           'uptime',
    romm:             'romm',
    emulatorjs:       'games',
    flasharcade:      'flash',
    foundry:          'vtt',
    kiwix:            'wiki',
    privatebin:       'paste',
    pxls:             'pxls',
    genart:           'art',
    jukebox:          'jukebox',
    invidious: 'invidious',
  },

  // ── PORTS ────────────────────────────────────────────────────────────────
  // Maps service keys to port numbers.
  // services.json is the canonical source; this object is the runtime lookup.
  // If you change a port: update here AND in services.json.
  ports: {
    // Core infrastructure
    caddy:             443,
    nextcloud:         80,
    authentik:         9000,
    stats_agent:       9001,
    control_server:    9002,
    achievement:       9003,
    session_manager:   9004,
    uptime_kuma:       3001,
    netdata:           19999,

    // Media
    jellyfin:          8096,
    jellyfin_https:    8920,
    calibre:           8083,
    audiobooks:        13378,
    navidrome:         4533,
    immich:            2283,
    kavita_comics:     5000,
    kavita_dnd:        5001,
    invidious:         8097,

    // Downloads / automation (LAN-only, admin-only)
    qbittorrent:       8090,
    sonarr:            8989,
    radarr:            7878,
    readarr:           8787,
    prowlarr:          9696,

    // Security
    vaultwarden:       8082,

    // Apps
    openwebui:         3000,
    ollama:            11434,
    recommendation:    5051,
    jukebox:           5050,
    kiwix:             8888,
    linguacafe:        8093,
    anki:              8091,
    librelingo:        8092,
    vikunja:           3456,
    mealie:            9925,
    excalidraw:        8086,
    readeck:           8087,
    privatebin:        8089,
    stirling:          8090,
    upscayl:           8094,
    pxls:              8095,
    genart:            5052,

    // Gaming
    emulatorjs:        8085,
    romm:              8098,
    sunshine:          47990,
    minecraft_vanilla: 25565,
    minecraft_modded:  25566,
    minecraft_rcon_v:  25575,
    minecraft_rcon_m:  25576,
    ark:               7777,
    ark_query:         27015,
    ss13:              1337,
    foundry:           30000,
    mtg_server:        8099,

    // Legacy
    plex_legacy:       32400,
  },

  // ── FILE SYSTEM PATHS ────────────────────────────────────────────────────
  // All canonical server paths. Update if you ever restructure your drives.
  paths: {
    // User data
    users:            'D:\\Users',

    // Media libraries
    media_movies:     'D:\\Media\\Movies',
    media_tv:         'D:\\Media\\TV',
    media_music:      'D:\\Music',
    books:            'D:\\Books',
    audiobooks:       'D:\\Audiobooks',
    comics:           'D:\\Comics',
    photos:           'D:\\Photos',
    downloads:        'D:\\Downloads',
    emulation_roms:   'D:\\Emulation',

    // Server infrastructure
    server:           'D:\\Server',
    achievements:     'D:\\Server\\Achievements',
    recommendations:  'D:\\Server\\Recommendations',
    dashboard:        'D:\\Server\\Dashboard',
    backups:          'D:\\Backups',

    // Config files
    caddyfile:        'C:\\caddy\\Caddyfile',
    caddy_bin:        'C:\\caddy\\caddy.exe',
  },

  // ── AUTHENTIK COMPUTED URLS ──────────────────────────────────────────────
  // All derived from CFG.domain. Never hardcode these in HTML.
  get authentikBase()  { return `https://auth.${this.domain}`; },
  get authentikAdmin() { return `https://auth.${this.domain}/if/admin/`; },
  get authentikApi()   { return `https://auth.${this.domain}/api/v3`; },

  // ── HELPER METHODS ───────────────────────────────────────────────────────

  /**
   * Full HTTPS URL for a service subdomain.
   * CFG.url('jellyfin') → 'https://jellyfin.yourdomain.com'
   */
  url(serviceKey) {
    const sub = this.subdomains[serviceKey];
    if (!sub) return `[no subdomain for "${serviceKey}"]`;
    return `https://${sub}.${this.domain}`;
  },

  /**
   * Local URL for a service.
   * CFG.local('jellyfin') → 'http://localhost:8096'
   */
  local(serviceKey) {
    const port = this.ports[serviceKey];
    if (!port) return `[no port for "${serviceKey}"]`;
    return `http://localhost:${port}`;
  },

  /**
   * Per-user data folder path.
   * CFG.userPath()            → 'D:\\Users\\[username]'
   * CFG.userPath('calibre')   → 'D:\\Users\\[username]\\calibre'
   */
  userPath(subfolder) {
    const base = `${this.paths.users}\\[username]`;
    return subfolder ? `${base}\\${subfolder}` : base;
  },

  /**
   * Authentik OIDC issuer URL for a given application slug.
   * CFG.oidcIssuer('jellyfin') → 'https://auth.yourdomain.com/application/o/jellyfin/'
   * The slug is the value set in Authentik when creating the application.
   */
  oidcIssuer(slug) {
    return `${this.authentikBase}/application/o/${slug}/`;
  },

  // ── JSON DATA LOADERS ────────────────────────────────────────────────────
  // Async loaders for companion data files.
  // Results are cached after first load — safe to call multiple times.

  _cache: {},

  /**
   * Load all services from services.json.
   * Returns array of service objects (metadata entry filtered out).
   * const services = await CFG.loadServices();
   */
  async loadServices() {
    if (this._cache.services) return this._cache.services;
    try {
      const r = await fetch('services.json');
      const data = await r.json();
      this._cache.services = data.filter(s => !s._comment);
      return this._cache.services;
    } catch(e) {
      console.error('CFG.loadServices() failed:', e);
      return [];
    }
  },

  /**
   * Load all version data from versions.json.
   * Returns object keyed by service id.
   * const versions = await CFG.loadVersions();
   */
  async loadVersions() {
    if (this._cache.versions) return this._cache.versions;
    try {
      const r = await fetch('versions.json');
      const data = await r.json();
      const clean = {};
      for (const [k, v] of Object.entries(data)) {
        if (!k.startsWith('_')) clean[k] = v;
      }
      this._cache.versions = clean;
      return this._cache.versions;
    } catch(e) {
      console.error('CFG.loadVersions() failed:', e);
      return {};
    }
  },

  /**
   * Get a single service entry by id.
   * const svc = await CFG.getService('jellyfin');
   */
  async getService(id) {
    const services = await this.loadServices();
    return services.find(s => s.id === id) ?? null;
  },

  /**
   * Get last confirmed version info for a service.
   * const v = await CFG.getVersion('jellyfin');
   * Returns: { version, checkedDate, notes } or null.
   */
  async getVersion(id) {
    const versions = await this.loadVersions();
    return versions[id] ?? null;
  },

  /**
   * Render a version badge into a DOM element.
   * CFG.renderVersion('jellyfin', document.getElementById('ver-badge'));
   *
   * If version is recorded: "v10.9.0  ·  last confirmed 2025-03-01"
   * If not yet recorded:    "version not yet recorded — update versions.json after first install"
   */
  async renderVersion(serviceId, el) {
    if (!el) return;
    const v = await this.getVersion(serviceId);
    if (!v || !v.version) {
      el.textContent = 'version not yet recorded — fill in versions.json after first confirmed working install';
      el.style.fontStyle = 'italic';
      el.style.color = 'var(--text-dim)';
    } else {
      const parts = [`v${v.version}`, `last confirmed ${v.checkedDate}`];
      if (v.notes) parts.push(v.notes);
      el.textContent = parts.join('  ·  ');
    }
  },
};

// ── AUTO-RENDER [data-cfg] ATTRIBUTES ─────────────────────────────────────
// Fills elements with data-cfg attributes from CFG values at DOM load.
// See the header comment block above for the full list of supported values.
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('[data-cfg]').forEach(el => {
    const val      = el.getAttribute('data-cfg');
    const colonIdx = val.indexOf(':');
    const type     = colonIdx === -1 ? val : val.slice(0, colonIdx);
    const key      = colonIdx === -1 ? ''  : val.slice(colonIdx + 1);
    let replacement = '';

    switch (type) {
      case 'domain':          replacement = CFG.domain;                                          break;
      case 'url':             replacement = key ? CFG.url(key)   : '';                           break;
      case 'local':           replacement = key ? CFG.local(key) : '';                           break;
      case 'port':            replacement = key ? String(CFG.ports[key] ?? `[unknown port: ${key}]`) : ''; break;
      case 'path':            replacement = key ? (CFG.paths[key] ?? `[unknown path: ${key}]`)   : ''; break;
      case 'userpath':        replacement = CFG.userPath(key || undefined);                       break;
      case 'authentik-admin': replacement = CFG.authentikAdmin;                                   break;
      case 'authentik-base':  replacement = CFG.authentikBase;                                    break;
      case 'authentik-api':   replacement = CFG.authentikApi;                                     break;
      case 'oidc-issuer':     replacement = key ? CFG.oidcIssuer(key) : '';                       break;
      case 'version':
        // Async render — data comes from versions.json
        if (key) CFG.renderVersion(key, el);
        return; // skip the synchronous set below
    }

    if (replacement) el.textContent = replacement;
  });
});
