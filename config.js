/**
 * ╔══════════════════════════════════════════════════════════════════════╗
 * ║                 SERVER CONFIGURATION — config.js                    ║
 * ║                                                                      ║
 * ║  THE ONLY FILE YOU NEED TO EDIT for port and path changes.          ║
 * ║  Domain, Tailscale network, and node topology live in nodes.json.   ║
 * ║  Every HTML page loads this. Every value flows from here.           ║
 * ║                                                                      ║
 * ║  Companion data files (same directory):                             ║
 * ║    nodes.json     — domain, Tailscale net, machine topology         ║
 * ║    services.json  — full service registry (catalogue, ports, tabs)  ║
 * ║    versions.json  — last confirmed working versions per service     ║
 * ║                                                                      ║
 * ║  USAGE IN HTML:                                                      ║
 * ║    <script src="config.js"></script>                                 ║
 * ║                                                                      ║
 * ║  JS:  CFG.domain  CFG.url('jellyfin')  CFG.ports.jellyfin          ║
 * ║       CFG.authentikAdmin  CFG.paths.caddyfile                       ║
 * ║       CFG.oidcIssuer('jellyfin')                                    ║
 * ║       await CFG.loadNodes()                                         ║
 * ║       await CFG.loadServices()                                      ║
 * ║       await CFG.getVersion('jellyfin')                              ║
 * ║                                                                      ║
 * ║  HTML auto-render attributes (data-cfg):                            ║
 * ║    data-cfg="domain"                → ixo.lol                       ║
 * ║    data-cfg="tailnet"               → ixo                           ║
 * ║    data-cfg="url:jellyfin"          → https://jellyfin.ixo.lol      ║
 * ║    data-cfg="tailscale:jellyfin"    → http://100.x.x.x:8096         ║
 * ║    data-cfg="local:jellyfin"        → http://localhost:8096          ║
 * ║    data-cfg="port:jellyfin"         → 8096                          ║
 * ║    data-cfg="path:users"            → D:\Users                      ║
 * ║    data-cfg="path:caddyfile"        → C:\caddy\Caddyfile            ║
 * ║    data-cfg="userpath"              → D:\Users\[username]           ║
 * ║    data-cfg="userpath:calibre"      → D:\Users\[username]\calibre   ║
 * ║    data-cfg="authentik-admin"       → https://auth.ixo.lol/if/admin/║
 * ║    data-cfg="authentik-base"        → https://auth.ixo.lol          ║
 * ║    data-cfg="authentik-api"         → https://auth.ixo.lol/api/v3   ║
 * ║    data-cfg="oidc-issuer:jellyfin"  → https://auth.ixo.lol/applic…  ║
 * ║    data-cfg="version:jellyfin"      → async from versions.json      ║
 * ║    data-cfg="tv-url"                → https://tv.ixo.lol             ║
 * ╚══════════════════════════════════════════════════════════════════════╝
 */

const CFG = {

  // ── DOMAIN ───────────────────────────────────────────────────────────────
  // Source of truth lives in nodes.json.
  // This value is the synchronous fallback used before nodes.json loads.
  // After loadNodes() resolves, CFG.domain is overwritten from nodes.json.
  // In practice all data-cfg rendering is sync using this value — nodes.json
  // is only needed for topology (node IPs, friend machines, etc.).
  domain: 'ixo.lol',

  // ── TAILNET ───────────────────────────────────────────────────────────────
  // Tailscale organization name. Used to build ts.net hostnames.
  // Source of truth: nodes.json → tailnet
  tailnet: 'ixo',

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
    invidious:        'invidious',
    wordle:           'wordle',
    hoarder:          'hoarder',
    streamarr:        null,   // LAN/Tailscale only — no public subdomain
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

    // Downloads / automation (Tailscale/LAN-only, admin-only)
    qbittorrent:       8090,
    sonarr:            8989,
    radarr:            7878,
    readarr:           8787,
    prowlarr:          9696,
    streamarr:         8102,

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
    hoarder:           8101,
    hoarder_meili:     7700,

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
    wordle:            8081,

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
    ddns:             'D:\\Server\\ddns',

    // Config files
    caddyfile:        'C:\\caddy\\Caddyfile',
    caddy_bin:        'C:\\caddy\\caddy.exe',
    nodes_json:       'D:\\Server\\Dashboard\\nodes.json',
  },

  // ── AUTHENTIK COMPUTED URLS ──────────────────────────────────────────────
  // All derived from CFG.domain. Never hardcode these in HTML.
  get authentikBase()  { return `https://auth.${this.domain}`; },
  get authentikAdmin() { return `https://auth.${this.domain}/if/admin/`; },
  get authentikApi()   { return `https://auth.${this.domain}/api/v3`; },

  // ── JELLYFIN PUBLIC TV URL ────────────────────────────────────────────────
  // The single port-forwarded public exception for Smart TV apps.
  // Source of truth: nodes.json → jellyfinPublic
  get jellyfinTvUrl()  { return `https://tv.${this.domain}`; },

  // ── HELPER METHODS ───────────────────────────────────────────────────────

  /**
   * Full HTTPS URL for a service subdomain (Tailscale-accessible via Caddy).
   * CFG.url('jellyfin') → 'https://jellyfin.ixo.lol'
   */
  url(serviceKey) {
    const sub = this.subdomains[serviceKey];
    if (!sub) return `[no subdomain for "${serviceKey}"]`;
    return `https://${sub}.${this.domain}`;
  },

  /**
   * Local URL for a service (same machine, no proxy).
   * CFG.local('jellyfin') → 'http://localhost:8096'
   */
  local(serviceKey) {
    const port = this.ports[serviceKey];
    if (!port) return `[no port for "${serviceKey}"]`;
    return `http://localhost:${port}`;
  },

  /**
   * Tailscale direct URL for a service on the hub node.
   * Only useful in docs explaining the Tailscale IP access path.
   * CFG.tailscaleUrl('jellyfin') → 'http://[hub-tailscale-ip]:8096'
   * (IP is a placeholder until nodes.json is filled in.)
   */
  tailscaleUrl(serviceKey) {
    const port = this.ports[serviceKey];
    if (!port) return `[no port for "${serviceKey}"]`;
    const ip = this._hubTailscaleIP || '[hub-tailscale-ip]';
    return `http://${ip}:${port}`;
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
   * CFG.oidcIssuer('jellyfin') → 'https://auth.ixo.lol/application/o/jellyfin/'
   */
  oidcIssuer(slug) {
    return `${this.authentikBase}/application/o/${slug}/`;
  },

  /**
   * Tailscale ts.net hostname for a named node.
   * CFG.tsHostname('hub') → 'server.ixo.ts.net'
   * Requires loadNodes() to have been called first.
   */
  tsHostname(nodeId) {
    const node = (this._nodes || []).find(n => n.id === nodeId);
    return node?.tailscaleHostname ?? `[${nodeId}.${this.tailnet}.ts.net]`;
  },

  // ── JSON DATA LOADERS ────────────────────────────────────────────────────
  _cache: {},
  _nodes: null,
  _hubTailscaleIP: null,

  /**
   * Load nodes from nodes.json.
   * Caches result. Also overwrites CFG.domain and CFG.tailnet from the file
   * so a single edit to nodes.json keeps everything in sync.
   */
  async loadNodes() {
    if (this._cache.nodes) return this._cache.nodes;
    try {
      const r = await fetch('nodes.json');
      const data = await r.json();
      this._cache.nodes = data;
      this._nodes = data.nodes || [];

      // Sync domain + tailnet from nodes.json into runtime CFG
      if (data.domain) this.domain = data.domain;
      if (data.tailnet) this.tailnet = data.tailnet;

      // Cache hub IP for tailscaleUrl() helper
      const hub = this._nodes.find(n => n.role === 'hub');
      if (hub?.tailscaleIP && !hub.tailscaleIP.startsWith('FILL')) {
        this._hubTailscaleIP = hub.tailscaleIP;
      }

      return data;
    } catch (e) {
      console.warn('nodes.json not found or invalid — using defaults', e);
      return null;
    }
  },

  /**
   * Load all services from services.json.
   * Returns array of service objects (metadata entry filtered out).
   */
  async loadServices() {
    if (this._cache.services) return this._cache.services;
    try {
      const r = await fetch('services.json');
      const raw = await r.json();
      const services = raw.filter(e => !e._comment && !e._note);
      this._cache.services = services;
      return services;
    } catch (e) {
      console.warn('services.json not found or invalid', e);
      return [];
    }
  },

  /**
   * Get a single service by id from services.json.
   */
  async getService(id) {
    const services = await this.loadServices();
    return services.find(s => s.id === id) ?? null;
  },

  /**
   * Load all versions from versions.json.
   */
  async loadVersions() {
    if (this._cache.versions) return this._cache.versions;
    try {
      const r = await fetch('versions.json');
      const data = await r.json();
      this._cache.versions = data;
      return data;
    } catch (e) {
      console.warn('versions.json not found or invalid', e);
      return {};
    }
  },

  /**
   * Get last confirmed version info for a service.
   */
  async getVersion(id) {
    const versions = await this.loadVersions();
    return versions[id] ?? null;
  },

  /**
   * Render a version badge into a DOM element.
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

  /**
   * Get node info by id from nodes.json.
   * Requires loadNodes() to have been called first, or calls it lazily.
   */
  async getNode(nodeId) {
    if (!this._nodes) await this.loadNodes();
    return (this._nodes || []).find(n => n.id === nodeId) ?? null;
  },

  /**
   * Get all friend nodes (role === 'friend-node') from nodes.json.
   */
  async getFriendNodes() {
    if (!this._nodes) await this.loadNodes();
    return (this._nodes || []).filter(n => n.role === 'friend-node');
  },
};

// ── AUTO-RENDER [data-cfg] ATTRIBUTES ─────────────────────────────────────
// Fills elements with data-cfg attributes from CFG values at DOM load.
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('[data-cfg]').forEach(el => {
    const val      = el.getAttribute('data-cfg');
    const colonIdx = val.indexOf(':');
    const type     = colonIdx === -1 ? val : val.slice(0, colonIdx);
    const key      = colonIdx === -1 ? ''  : val.slice(colonIdx + 1);
    let replacement = '';

    switch (type) {
      case 'domain':          replacement = CFG.domain;                                                       break;
      case 'tailnet':         replacement = CFG.tailnet;                                                      break;
      case 'url':             replacement = key ? CFG.url(key) : '';                                          break;
      case 'tailscale':       replacement = key ? CFG.tailscaleUrl(key) : '';                                 break;
      case 'local':           replacement = key ? CFG.local(key) : '';                                        break;
      case 'port':            replacement = key ? String(CFG.ports[key] ?? `[unknown port: ${key}]`) : '';    break;
      case 'path':            replacement = key ? (CFG.paths[key] ?? `[unknown path: ${key}]`) : '';          break;
      case 'userpath':        replacement = CFG.userPath(key || undefined);                                    break;
      case 'authentik-admin': replacement = CFG.authentikAdmin;                                                break;
      case 'authentik-base':  replacement = CFG.authentikBase;                                                 break;
      case 'authentik-api':   replacement = CFG.authentikApi;                                                  break;
      case 'oidc-issuer':     replacement = key ? CFG.oidcIssuer(key) : '';                                   break;
      case 'tv-url':          replacement = CFG.jellyfinTvUrl;                                                 break;
      case 'version':
        if (key) CFG.renderVersion(key, el);
        return;
    }

    if (replacement) el.textContent = replacement;
  });
});
