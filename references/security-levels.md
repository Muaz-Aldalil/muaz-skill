# Security Rules by Level

Each level includes the rules from all previous levels plus its own additions.

---

## Cross-Cutting (all levels, always apply)

These rules apply to every project regardless of security level.

### DevTools Leak Prevention

| Tab | Rule | Reason |
|---|---|---|
| **Network** | No tokens/passwords/secrets in URL query params or fragments (`?token=`, `#access_token=`) | Logged in browser history, visible in Network request URL |
| **Network** | No PII in JWT payload — base64-decoded and visible in Network → Response | Anyone with DevTools can decode without the key |
| **Network** | Authorization headers (`Bearer ...`) acceptable; custom `X-API-Key` from client flagged | Standard pattern vs. leakable plaintext key |
| **Application** | Auth tokens → httpOnly cookies only. Never localStorage, sessionStorage, or IndexedDB | JS-inaccessible; XSS can't read them |
| **Application** | No API keys, secrets, or tokens in `window.__ENV` or global JS variables | Visible in Application → Scripts → Global |
| **Application** | No secrets stored in IndexedDB, WebSQL, or Cache Storage | XSS or compromised extension can read them |
| **Elements** | No sensitive data in `data-*` attributes, hidden inputs, or HTML comments | Visible in Elements panel to anyone |
| **Elements** | No tokens in hidden DOM (`<div hidden data-token="...">`) | Same — visible in inspector |
| **Sources** | No hardcoded secrets in client-side bundle JS files | Anyone can view bundled source |
| **Sources** | `VITE_` / `NEXT_PUBLIC_` / `REACT_APP_` prefixed vars are public — never put secrets there | Build system inlines them into client bundle |
| **Sources** | Source maps — production: disable or restrict to authenticated/internal only | Unminified source reveals API endpoints, logic, comments |
| **Console** | No `console.log/warn/error` with tokens, passwords, or user data in production | Visible in Console tab |
| **Console** | Strip console output in production build (eslint `no-console` + Terser drop) | Defense in depth against leftover debug logs |

### Security Headers

The server should send these on every response. Flag to backend if missing.

| Header | Value | What it prevents |
|---|---|---|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` | MITM downgrade attacks |
| `X-Frame-Options` | `DENY` or `SAMEORIGIN` | Clickjacking |
| `X-Content-Type-Options` | `nosniff` | MIME type sniffing |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Referer leakage |
| `Permissions-Policy` | `camera=(), microphone=(), geolocation=()` | Feature abuse |
| `Cross-Origin-Resource-Policy` | `same-origin` | Cross-origin data leakage |

### CSP (Content Security Policy)

Minimal baseline for all levels:
```
default-src 'self';
script-src 'self';
style-src 'self' 'unsafe-inline';
img-src 'self' data: https:;
connect-src 'self';
font-src 'self' https://fonts.gstatic.com;
frame-ancestors 'none';
```

- Report violations via `report-uri` or `report-to`
- Never use `'unsafe-inline'` for scripts — use nonces or hashes at L2+
- Never use `'unsafe-eval'` unless required (compile-to-JS tools) and document why

### Environment Variable & Build Security

- [ ] `VITE_*`, `NEXT_PUBLIC_*`, `REACT_APP_*` — treat as public, never put secrets here
- [ ] All other env vars are server-only — never import them from client code
- [ ] Use a single env file convention (`.env.local` for local, `.env.production` for CI)
- [ ] Strip debug code in production: `if (import.meta.env.DEV)` for Vite, `process.env.NODE_ENV === 'development'` for Next/CRA
- [ ] Remove `console.log` in production build (eslint rule + build plugin)
- [ ] Source maps: use `hidden-source-map` or disable in production
- [ ] Fail build if any file contains `SECRET_` or `PRIVATE_KEY` pattern in source

### Trusted Types (DOM XSS)

- [ ] Enable Trusted Types via CSP: `require-trusted-types-for 'script'`
- [ ] Create a Trusted Types policy for safe HTML manipulation
- [ ] Never use `innerHTML`, `outerHTML`, `insertAdjacentHTML` without a Trusted Types policy
- [ ] In React: avoid `dangerouslySetInnerHTML` — use a sanitized component (DOMPurify + Trusted Types)

### Error Handling (all levels)

- [ ] React Error Boundaries with generic fallback UI — never show component stack traces in production
- [ ] API error responses: generic messages — no stack traces, SQL queries, or internal paths
- [ ] Client-side error logging: strip user data before sending to logging service (Sentry, etc.)
- [ ] Never surface `Error.message` from thrown exceptions directly to UI

### Supply Chain Security (all levels)

- [ ] **SBOM generation**: produce CycloneDX or SPDX SBOM at build time — attach to releases
- [ ] **Dependency provenance**: verify package signatures (sigstore/cosign for containers, npm provenance for packages)
- [ ] **CI/CD secrets scanning**: scan every commit and PR for secrets (Gitleaks, truffleHog) — block CI on match
- [ ] **Signed commits**: require GPG/SSH signing on all commits in the default branch
- [ ] **Software attestation**: generate SLSA provenance attestations for build artifacts
- [ ] **Dependency review**: review new and updated dependencies for known malware before merge
- [ ] **Lock files**: commit lock files (package-lock.json, yarn.lock, go.sum) — pin exact versions

### Injection Defense Matrix

Organized by input vector — find your coding context and see what injections apply and at which level.

| Vector | Injection types | Primary defense | Applied |
|---|---|---|---|
| **User text / rich text** | XSS, HTML injection, JS injection, markdown renderer XSS | Context-aware output encoding + DOMPurify | L1 |
| **URLs / redirect targets** | Open redirect, `javascript:` / `data:` scheme injection | Allowlist origins, reject non-HTTP schemes | L1 |
| **CSS / style contexts** | CSS data exfiltration via attribute selectors, `url()` injection | CSP `style-src` with nonces, never interpolate user data in `<style>` | L1 |
| **File uploads** | SVG XSS, path traversal, polyglot files, zip bombs | Validate magic bytes + type + size server-side | L1 |
| **HTML attributes** | DOM clobbering (`id=`/`name=` overwriting globals), attribute injection | Use `setAttribute` safely, avoid generic `id` values on sensitive elements | L1 |
| **Database queries** | SQL injection, NoSQL injection (`$ne`, `$where`, `$regex`), XPath, LDAP | Parameterized queries / query builders — never string concat | L2 |
| **HTTP headers / cookies** | CRLF injection, log injection, cache poisoning, response splitting | Strip `\r\n` from header values, validate before logging | L2 |
| **Template engines** | SSTI (Jinja2, Pug, EJS, Twig), Expression Language (OGNL, SpEL) | Never pass user input as template code — sandbox if required | L2 |
| **Command execution** | Command injection, argument injection | Avoid shell spawn from input, use `execFile` with allowlist | L2 |
| **Export / download** | CSV formula injection (`=HYPERLINK`), PDF XSS | Escape leading `= + - @` in CSV, sanitize PDF render input | L2 |
| **XML parsers** | XXE (local file read, SSRF), XML bomb (billion laughs), XPath injection | Disable DTD and external entities — prefer JSON | L3 |
| **Serialization** | Insecure deserialization (pickle, YAML, Java serialization, PHP unserialize) | Use JSON — never deserialize untrusted input with polyglot parsers | L3 |
| **Service-to-service** | SSRF, DNS rebinding, host header injection | Allowlist outbound URLs, validate Host header, block internal IPs at gateway | L3 |
| **Uploaded configuration** | IaC injection (Terraform `local_exec` from var), env injection | Treat IaC vars as untrusted — no inline eval from user-supplied values | L3 |
| **Build / dependency** | Dependency confusion, typo-squatting, malicious packages | Scoped packages, lock files, registry allowlist, `npm provenance` | L3 |
| **WebSockets** | WS message injection, origin spoofing | Validate Origin on upgrade, authenticate on connect, validate all messages | L3 |
| **Prompt / LLM** | Direct prompt injection, indirect (retrieved data) prompt injection | Separate system vs user prompt, validate output, rate limit | L3\* |
| **API endpoints / resource IDs** | IDOR, mass assignment (role/price tampering) | Enforce ownership + authorization on every endpoint; use UUIDs | L2 |
| **Input validation (regex)** | ReDoS (catastrophic backtracking) | Anchor patterns, limit input length, timeout on regex execution | L2 |
| **Authentication / comparison** | Timing side-channel (leak password length, valid usernames, token values) | Constant-time comparison (`crypto.timingSafeEqual`) | L2 |
| **HTTP / proxy desync** | HTTP request smuggling, response splitting, web cache poisoning | Use HTTP/2; validate Content-Length vs Transfer-Encoding at proxy | L2 |
| **Links / navigation** | Tabnabbing, open redirect | `rel="noopener noreferrer"` on all `target="_blank"` links | L1 |
| **Business logic / workflows** | Race condition (TOCTOU), business logic abuse (coupon stacking, quota bypass) | Idempotency keys, transactional locking, state machine validation | L3 |
| **Mobile: deep links / intents** | Deep link hijacking, intent interception, custom scheme spoofing | Validate URL authority, verify source app package, prefer verified links | L2 |
| **Mobile: WebView bridges** | JS bridge injection, protocol handler abuse, local file access via WebView | Restrict bridge API to minimum, validate origin + message format, disable file access | L3 |
| **Mobile: app integrity** | Sideloading, repackaging, runtime hooking (Frida), rooted/jailbroken device | Play Integrity / DeviceCheck attestation at login + sensitive actions | L3 |

\* LLM row only when project uses AI/LLM features.

### Privacy & Browser Fingerprinting (all levels)

- [ ] **Limit fingerprinting APIs**: restrict Canvas, WebGL, AudioContext, Battery API via Permissions-Policy or conditional gating — fingerprinting poses a privacy risk without a security benefit
- [ ] **No third-party fingerprinting**: audit all embedded scripts for canvas reads, font enumeration, WebGL queries, and navigator property collection
- [ ] **Minimize passive collection**: avoid keystroke pattern logging, scroll depth tracking, and mouse movement recording unless the core feature requires it

---

## Level 1 — PUBLIC

*Applied to: static sites, portfolios, landing pages, no login, no payments*

### Frontend

- [ ] No secrets / API keys / tokens in source code or bundled JS
- [ ] SRI (Subresource Integrity) on all external CDN scripts and stylesheets
- [ ] HTTPS enforced — flag if served over HTTP
- [ ] CSP header applied (baseline from Cross-Cutting)
- [ ] No `eval()` — ever
- [ ] Sanitize any dynamic content rendered to DOM
- [ ] No `dangerouslySetInnerHTML` / `innerHTML` without sanitization
- [ ] Trusted Types enabled (from Cross-Cutting)
- [ ] Third-party scripts (analytics, fonts, widgets) loaded with `integrity=` attribute
- [ ] All forms use POST (never GET for mutations)
- [ ] Alt text on all meaningful images (a11y + basic SEO, not security but doubly enforces intent)
- [ ] All `target="_blank"` links use `rel="noopener noreferrer"` — prevents tabnabbing

### Backend / API

- [ ] CSP headers set on every response
- [ ] CORS: allow specific origins only (no `Access-Control-Allow-Origin: *` if any dynamic content)
- [ ] Security headers from Cross-Cutting all confirmed present
- [ ] Static asset serving: disable directory listing
- [ ] No sensitive data in static file names or paths

---

## Level 2 — AUTHENTICATED

*Applied to: SaaS, dashboards, e-commerce, apps with user accounts and sessions*

Includes **all Level 1 rules** plus the following.

### Frontend

- [ ] Auth tokens → httpOnly cookies only (never localStorage/sessionStorage/IndexedDB)
- [ ] OAuth / OIDC flow: use **Authorization Code + PKCE**, never Implicit Grant
- [ ] Session: show "Session expiring in 5 minutes" warning before auto-logout
- [ ] Logout clears ALL client-side state: cookies, cached user data, any stored UI state
- [ ] Login error messages must NOT reveal whether the email exists:
      BAD:  "No account found for this email"
      GOOD: "Invalid email or password"
- [ ] Disable autocomplete on sensitive fields:
      `autocomplete="new-password"` on password fields
      `autocomplete="one-time-code"` on OTP fields
- [ ] No sensitive data in URL query params (`?redirect=`, `?token=`, `?email=`)
- [ ] Input validation on ALL user-facing forms (client-side convenience + flag for server)
- [ ] Sensitive fields masked: passwords always, card numbers partially (`**** **** **** 4242`)
- [ ] Disable submit button after click until response received
- [ ] Show loading state during async operations ("Sending...", spinner)
- [ ] After N failed login attempts → show cooldown message in UI (no immediate retry)
- [ ] Dependency vulnerability scanning: automated scan on every PR — fail CI on critical/high
- [ ] Scheduled scanning: daily scan for new CVEs between PRs
- [ ] SCA tooling: use dedicated scanner (Dependabot, Grype, Snyk) — not just npm audit
- [ ] Auto-remediate: auto-PR for patch-level fixes, manual review for minor/major
- [ ] No packages with known XSS vulnerabilities
- [ ] CSP: upgrade to `'strict-dynamic'` with nonces — no `'unsafe-inline'`
- [ ] Third-party scripts: only what's required (strip unused analytics/widget SDKs)
- [ ] Error messages never reveal system internals:
      BAD:  "PostgreSQL error: duplicate key value"
      GOOD: "Something went wrong. Please try again."
- [ ] `SameSite=Lax` or `Strict` on all session/cookie set operations
- [ ] `Secure` flag on all cookies (only sent over HTTPS)
- [ ] `Path=/` scoped narrowly per cookie (not global `/`)
- [ ] DevTools leak prevention from Cross-Cutting fully verified before launch

### Backend / API

- [ ] **Password hashing**: bcrypt (cost ≥12) or argon2id — never plaintext, never MD5/SHA1
- [ ] **JWT**: short expiry access tokens (≤15 min), refresh tokens with rotation (7 days max)
- [ ] **JWT algorithm enforcement**: enforce a single algorithm server-side (RS256 or EdDSA) — never derive it from the JWT header (prevents algorithm confusion: `alg: none`, RS256→HS256 with public key)
- [ ] **JWT secret**: strong random value, rotated periodically, never in source code
- [ ] **Server-side input validation** — client validation is convenience, server is authoritative
- [ ] **SQL injection prevention**: parameterized queries / prepared statements — never string concatenation
- [ ] **CORS**: allowlist specific origins, methods, and headers — no wildcard with credentials
- [ ] **Rate limiting**: per IP + per user (e.g., 5 login attempts/min, 100 requests/min general)
- [ ] **CSRF tokens**: on all state-mutating endpoints (POST/PUT/PATCH/DELETE)
- [ ] **Session fixation prevention**: regenerate session/cookie ID on login and privilege escalation
- [ ] **Cookie attributes**: `HttpOnly`, `Secure`, `SameSite=Lax`, `Path=/`
- [ ] **Password strength policy**: minimum 8 chars (NIST recommends 12+), common password check
- [ ] **Account lockout**: temporary lockout after N failed attempts (e.g., 5 attempts → 15-min lockout)
- [ ] **Email verification**: verify email before granting full access
- [ ] **Password reset**: use time-limited, single-use tokens — never email password in plaintext
- [ ] **Security headers**: all headers from Cross-Cutting confirmed on every response
- [ ] **Helmet.js** (Express/Node) or equivalent middleware active
- [ ] **Request size limits**: cap body size (e.g., 1MB for JSON, 10MB for file uploads)
- [ ] **API versioning**: versioned endpoints (`/api/v2/`) to avoid breaking changes from old clients
- [ ] **OAuth / OIDC**: validate `aud`, `iss`, `exp`, `nonce` on every token verification
- [ ] **PKCE**: enforce S256 challenge method, reject plain
- [ ] **IDOR prevention**: enforce ownership/authorization checks on every endpoint — never trust the ID in the URL without verifying it belongs to the authenticated user
- [ ] **Mass assignment protection**: define explicit allowlists of writable fields per endpoint — never blindly write request body to DB/models
- [ ] **ReDoS prevention**: anchor regex patterns, enforce max input length, set regex execution timeout at the application level
- [ ] **Timing attack prevention**: use constant-time comparison (`crypto.timingSafeEqual`) for passwords, tokens, HMACs — never use `==`/`===` on secrets
- [ ] **HTTP request smuggling prevention**: prefer HTTP/2; validate Content-Length vs Transfer-Encoding; reject conflicting headers at the reverse proxy

---

## Level 3 — SENSITIVE

*Applied to: fintech, healthcare, legal, admin panels, PII-handling apps*

Includes **all Level 1 + Level 2 rules** plus the following.

### Frontend

- [ ] CSP: `'unsafe-inline'` and `'unsafe-eval'` are strictly forbidden — use nonces or SHA hashes
- [ ] CSP `report-uri` / `report-to` configured with active monitoring
- [ ] Inline event handlers (`onclick="..."`) replaced with `addEventListener` (required by strict CSP)
- [ ] No inline `<style>` blocks in production — external stylesheets only
- [ ] Third-party scripts: every one audited and justified — no unapproved third-party code
- [ ] All external scripts loaded with SRI + `async`/`defer`
- [ ] Prefer self-hosted over CDN for critical libraries (minimize supply chain risk)
- [ ] PII, health info, financial data NEVER in: localStorage / sessionStorage / URL params / browser history / hidden DOM
- [ ] Audio/visual confirmation before destructive actions ("Type DELETE to confirm")
- [ ] Bundle audit — verify no sensitive data leaks via Network tab or bundled source
- [ ] Mask all sensitive data in UI:
      Card numbers:  `**** **** **** 4242`
      Account numbers: `••••1234`
      SSN / National ID: `***-**-6789`
      Phone numbers: `+*** *** ** 789`
- [ ] MFA / 2FA flow: clear UI on each step, never expose backup codes in plain view
- [ ] WebAuthn / passkeys: support as primary or MFA method — prefer platform authenticator (Touch ID, Windows Hello, Android biometric) over SMS/OTP where available
- [ ] Auto-logout on inactivity (default ≤15 min, configurable)
- [ ] Show inactivity warning 2 minutes before auto-logout
- [ ] Re-authentication required for sensitive actions (change password, transfer funds, delete account, change MFA)
- [ ] Allowlist input validation: define exactly what's valid, reject everything else
- [ ] Max length enforced on ALL inputs (prevent buffer overflow / storage abuse)
- [ ] File upload: validate type + size + magic bytes client-side + flag server validation
- [ ] Drag-and-drop upload: validate file before drop event is accepted
- [ ] Screen capture prevention: `@media print` styles or overlay on sensitive data (not foolproof, defense-in-depth)
- [ ] Clipboard: don't write sensitive data to clipboard without explicit user action
- [ ] Payment forms: use iframe-based tokenization (Stripe Elements, etc.) — never touch raw card data

#### Mobile

- [ ] **Deep link validation**: verify URL authority on every incoming deep link — reject unrecognized schemes and hosts
- [ ] **Android App Links / iOS Universal Links**: prefer verified links over custom URL schemes — they can't be hijacked by another app
- [ ] **WebView bridge security**: expose the minimum JS bridge API surface — validate origin and message format on every bridge call
- [ ] **WebView hardening**: disable file access (`setAllowFileAccess(false)`), disable content URL access, disable clipboard access from WebView
- [ ] **App integrity**: implement Play Integrity (Android) or DeviceCheck (iOS) at login and before sensitive actions — detect rooted/jailbroken devices, repackaging, and runtime hooking
- [ ] **Certificate pinning**: pin TLS certificates or public keys in the mobile app — prevent MITM via compromised CA or proxy tools

### Backend / API

- [ ] **CSP**: strict with nonces, `report-uri` active, violations monitored and alerted
- [ ] **Data encryption at rest**: database-level encryption (AES-256) for PII/financial/health data
- [ ] **Data encryption in transit**: TLS 1.3 minimum, disable TLS 1.0/1.1
- [ ] **Audit logging**: every admin/privileged action logged with:
      User ID · Timestamp · Action · Resource ID · Before/After values · IP address
- [ ] **Audit log storage**: append-only, tamper-evident (e.g., signed logs or external log service)
- [ ] **Idempotency keys**: on all payment/financial endpoints — prevent double charges on retry
- [ ] **MFA enforcement**: require 2FA for all accounts, not optional
- [ ] **Re-authentication**: sensitive actions require fresh password or 2FA step-up
- [ ] **Data retention**: automatic purge of stale sessions, logs (retain as required by regulation, then delete)
- [ ] **Data deletion (right to be forgotten)**: user-initiated full data wipe — documented, verifiable
- [ ] **Cookie consent**: GDPR/Turkish KVKK compliant — explicit consent, granular opt-out
- [ ] **API keys for service accounts**: scoped to least privilege, per-environment, rotation policy
- [ ] **Webhook signature verification**: HMAC-SHA256 verification on incoming webhook payloads
- [ ] **SSRF protection**: allowlist outbound URLs, block internal IP ranges in proxy/API gateway
- [ ] **Secrets management**: use a secrets vault (HashiCorp Vault, AWS Secrets Manager, etc.) — never in `.env` files
- [ ] **Container security**: non-root user in Docker, read-only filesystem where possible, no privileged mode
- [ ] **Dependency scanning**: automated SCA (Snyk, Dependabot, or equivalent) in CI/CD pipeline
- [ ] **Penetration testing**: scheduled third-party testing at least annually
- [ ] **Incident response**: documented plan for data breach — notification timeline, rollback procedure

#### API Security

- [ ] **API gateway security**: enforce WAF rules at the edge (block SQLi, XSS, path traversal); IP allowlisting; edge rate limiting per API key; request size limits per endpoint
- [ ] **mTLS**: mutual TLS for service-to-service communication — verify client certificates at ingress for all internal traffic
- [ ] **API key rate limiting**: distinct per-key rate limits for service accounts (e.g., 1000 req/min per key) — decoupled from user session rate limits
- [ ] **WebSocket security**: validate `Origin` header on upgrade, authenticate on connect, validate message format and size on every frame
- [ ] **Race condition / TOCTOU**: use idempotency keys, pessimistic locking, or optimistic concurrency for all mutating workflows — prevent double-spend, inventory oversell, coupon multi-redeem
- [ ] **Business logic validation**: define allowed state transitions for stateful objects (order status, account tier, subscription) — reject any transition outside the workflow graph

#### Data Protection

- [ ] **Data classification**: tag every DB column with a tier — `public` / `internal` / `confidential` / `restricted` — enforce access controls based on tag
- [ ] **Database encryption detail**: column-level encryption (AES-256-GCM with key rotation) for individual sensitive fields (PII, credentials); whole-database TDE/disk encryption for bulk at-rest protection; document which strategy applies per table
- [ ] **Backup encryption**: encrypt all backups with AES-256 — store encryption key in a separate KMS from backup storage — test full restore process quarterly
- [ ] **Key management lifecycle**: use a dedicated KMS (AWS KMS, Azure Key Vault, HashiCorp Vault Enterprise) — automate key rotation, never hardcode keys, audit every key access

#### CI/CD & Pipeline Security

- [ ] **Secrets scanning in CI**: scan every commit and PR for secrets (Gitleaks, truffleHog) — block merge on confirmed match
- [ ] **SAST scanning**: static analysis in CI (CodeQL, Semgrep, SonarQube) — block PR merge on critical/high findings
- [ ] **DAST scanning**: dynamic scanning against staging environment before production deploy (OWASP ZAP, Burp Suite) — flag regression in known vulnerability classes
- [ ] **Cloud security posture scanning**: CSPM scanning for cloud config drift (AWS Config, Azure Policy, GCP Org Policy); IaC scanning for misconfigurations (tfsec, checkov, cdk-nag) — gated in CI pipeline
- [ ] **SBOM generation**: produce CycloneDX or SPDX SBOM at every build — attach to release artifact, submit to centralized dependency dashboard

#### Session & Monitoring

- [ ] **Concurrent session limits**: cap active sessions per user (default 5) — "kill all other sessions" on password change or privilege escalation
- [ ] **Logging standards**: structured JSON format — always log user ID, timestamp, action, resource ID, outcome, IP, correlation ID; **never log** passwords, tokens, PANs, secrets, raw request bodies, PII fields
- [ ] **Anomaly alerting**: alert on patterns — N failed logins from same IP in 5 min, privileged action outside business hours, unexpected spike in API key usage, new device/location for existing user

---

## Compliance Mapping

Key L3 controls mapped to common regulatory frameworks. Use this table during audits to demonstrate coverage.

| L3 Control | PCI-DSS 4.0 | HIPAA | SOC 2 (TSC) | GDPR |
|---|---|---|---|---|
| Encryption at rest (DB) | 3.4 | §164.312(a)(1) | CC6.1 | Art. 32 |
| Encryption in transit (TLS 1.3) | 4.1 | §164.312(e)(1) | CC6.7 | Art. 32 |
| Audit logging (admin actions) | 10.2 | §164.312(b) | CC7.2 | Art. 5(2) |
| Access control / least privilege | 7.1 | §164.312(a)(1) | CC6.2 | Art. 25 (PbD) |
| MFA enforcement | 8.4 | §164.312(d) | CC6.1 | — |
| Backup encryption + restore test | 3.5 | §164.308(a)(7) | CC6.1 | Art. 32 |
| Data retention + deletion | 3.1 | §164.316(b)(2) | CC6.4 | Art. 5(1)(e), 17 |
| Incident response plan | 12.10 | §164.308(a)(6) | CC7.3 | Art. 33 |
| Penetration testing | 11.4 | §164.308(a)(8) | CC7.1 | Art. 32 |
| Dependency scanning (SCA) | 6.4 | §164.308(a)(1) | CC8.1 | Art. 32 |
| SAST / DAST scanning | 6.4 | §164.308(a)(1) | CC8.1 | Art. 32 |
| Secrets management (vault) | 3.5 | §164.312(a)(1) | CC6.1 | Art. 25 |
| Webhook signature verification | — | §164.312(c)(2) | CC6.1 | Art. 32 |
| Cookie consent / GDPR | — | — | CC6.8 | Art. 7, 25 |
| SSRF / outbound allowlist | 6.4 | §164.308(a)(1) | CC6.1 | Art. 32 |
| SBOM / supply chain | 6.4 | — | CC8.1 | — |
