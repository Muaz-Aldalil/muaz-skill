# Code Maintainability & Backend Readiness

Applies to all stacks and team sizes.

---

## Naming Conventions

```
Variables/Functions : camelCase   -> getUserProfile, isLoading, hasError
Components          : PascalCase  -> UserCard, AuthForm, DashboardLayout
Constants           : UPPER_SNAKE -> MAX_RETRY_COUNT, API_TIMEOUT_MS
CSS classes         : kebab-case  -> user-card, auth-form__input
Files               : kebab-case  -> user-card.tsx, use-auth.ts
Boolean vars        : is/has/can  -> isOpen, hasPermission, canSubmit
Event handlers      : handle prefix -> handleSubmit, handleClose
Async functions     : verb + noun -> fetchUser, createPost, deleteItem

RULE: Name by purpose, not by type.
BAD:  const data = await fetch(...)
GOOD: const userProfile = await fetchUserProfile(userId)
```

---

## Comments — Minimal and Purposeful

Write comments for WHY, not WHAT. If the code is clear, no comment needed.

**WHEN to comment:**
- Non-obvious business logic
- Workarounds with reasons ("// Safari bug: flex gap ignored on <select>")
- Important constraints ("// Must run before analytics init")
- Complex algorithms

**WHEN NOT to comment:**
- Self-explanatory code (const isLoggedIn = !!user)
- Restating what the code does
- Commented-out code (delete it, git has history)

**FORMAT (JSDoc on exported functions/components only):**
```typescript
/**
 * Fetches paginated list of users from the API.
 * Returns empty array on 404 — treats it as "no users yet", not an error.
 *
 * @param page - 1-indexed page number
 * @param limit - items per page (default: 20, max: 100)
 */
```

**RULE:** One JSDoc block per exported function/component.
**RULE:** No JSDoc on internal helpers — clear naming is enough.

---

## File & Folder Structure

Group by feature, not by type.

**BAD:**
```
/components/UserCard.tsx
/components/PostCard.tsx
/hooks/useUser.ts
/hooks/usePost.ts
```

**GOOD:**
```
/features/users/UserCard.tsx
/features/users/useUser.ts
/features/posts/PostCard.tsx
/features/posts/usePost.ts
```

**SHARED across features -> /shared/components/ or /shared/hooks/**
**RULE:** A junior should find any file in < 30 seconds.

---

## Function Size

- Max 30 lines per function. If longer -> split.
- One function = one responsibility.
- If you need to write "and" to describe it -> split it.

---

## Component Size

- Max 150 lines per component. If longer -> extract sub-components.
- Props > 5 -> create an interface/type, not inline.

---

## Simplicity First

Before reaching for a library or abstraction, check if the problem is small enough to solve inline:

- **No interface with one implementation** — if there's only one way to do it, don't abstract
- **No factory for one product** — direct construction is fine until you need a second variant
- **No context/provider when props suffice** — prop drilling 1-2 levels is simpler than context
- **No custom hook wrapping a single useState** — that's just a rename
- **No package that stdlib covers:**
  - `crypto.randomUUID()` over `uuid`
  - `Intl.DateTimeFormat` over `date-fns` for simple formatting
  - CSS transitions over `framer-motion` for hover/press
  - Template literal over `clsx` for ≤3 classes
- **Prefer native before custom:**
  - `<details>` over building an accordion component
  - CSS `:has()` over adding state to show/hide
  - `<dialog>` over a custom modal
  - HTML form + native validation over `react-hook-form` for ≤3 fields
- **No boilerplate comments** — "Handle form submission" on `handleSubmit` is noise
- **No `console.log` in generated code** — use error boundaries and monitoring instead

---

## Constants

- No magic numbers or strings in logic.
  BAD:  setTimeout(fn, 3000)
  GOOD: const TOAST_DURATION_MS = 3000; setTimeout(fn, TOAST_DURATION_MS)
- Shared constants -> /shared/constants/ or /config/constants.ts

---

## TypeScript (when used)

- No `any` — use `unknown` if type is truly unknown
- Explicit return types on all exported functions
- Props interface above every component
- API response types defined before use (not inferred)
- Enums for fixed sets of values (status, role, category)

---

## API Layer — Centralized, Never Inline

Create a dedicated API layer. Never call fetch() directly in components.

```
/services/api.ts          -> base client (headers, baseURL, error handling)
/services/users.ts        -> all user-related endpoints
/services/products.ts     -> all product-related endpoints
```

### Base Client Pattern
- Base URL from environment variable (never hardcoded)
- Auth token injected in request interceptor
- Timeout configured (default: 10000ms)
- Global error handler for 401 (redirect to login) and 500 (show toast)

**Example shape:**
```typescript
// services/users.ts
export const getUser   = (id: string)     => GET  /users/:id
export const updateUser = (id, data)       => PUT  /users/:id
export const deleteUser = (id: string)     => DELETE /users/:id
```

---

## API Contracts — Define Before Building UI

For every API call, document:
- Endpoint    : GET /api/users/:id
- Auth        : Required / Public
- Request     : { params: { id: string } }
- Response OK : { id, name, email, role, createdAt }
- Response ERR: { code: string, message: string }
- Status codes: 200 (ok) | 401 (unauth) | 404 (not found) | 422 (validation)

**RULE:** UI components never know about HTTP status codes.
The service layer translates them into typed errors.

---

## Error Handling — Typed and Explicit

Define error types:
```typescript
type ApiError = {
  code: 'UNAUTHORIZED' | 'NOT_FOUND' | 'VALIDATION' | 'SERVER_ERROR';
  message: string;
  field?: string; // for validation errors
}

// Component receives: { data, error: ApiError | null, isLoading }
// Component never does: catch (e: any) { console.log(e) }
```

---

## Environment Variables

All config that changes per environment -> .env file.
```
VITE_API_BASE_URL=
VITE_ANALYTICS_KEY=
```

**Rules:**
- .env.example committed to git (with empty values)
- .env never committed (in .gitignore)
- Prefix: VITE_ (Vite) | NEXT_PUBLIC_ (Next.js, client-side)
- No defaults for required vars — fail loudly if missing
- Validate all env vars at startup (not at runtime):
  ```typescript
  if (!import.meta.env.VITE_API_BASE_URL) {
    throw new Error('VITE_API_BASE_URL is required')
  }
  ```

---

## HTTP Status Code Handling (UI side)

| Status | Action |
|---|---|
| 200-299 | Success — update state, show success feedback |
| 400 | Validation error — show field-level error in form |
| 401 | Unauthorized — redirect to login, clear auth state |
| 403 | Forbidden — show "You don't have permission" (not 404) |
| 404 | Not found — show empty state with action |
| 422 | Unprocessable — map field errors to form fields |
| 429 | Rate limited — show "Try again in X seconds" with countdown |
| 500+ | Server error — show generic error + retry option, log to monitoring |

---

## Loading & Error State Contract

Every API call exposes 3 states to the component:
```typescript
{ data: T | null, isLoading: boolean, error: ApiError | null }
```

Component must handle all 3. No exceptions.

---

## Feature Flags

Keep flag logic isolated in a single config or service file — never scattered across 20 components.

```typescript
// BAD: scattered
<NewDashboard />  // hidden behind flag somewhere else
<button onClick={flags.newPay ? handleNew : handleOld} />

// GOOD: single gateway
function CheckoutGateway({ flags }) {
  if (flags.newCheckout) return <NewCheckout />;
  return <LegacyCheckout />;
}
```

**Rule:** Deleting a flag means deleting exactly one file (the gateway) + one config line. No search-and-replace across the codebase.

**Stale flags:** Remove after 6 months. If the feature is stable, the conditional is dead code.
