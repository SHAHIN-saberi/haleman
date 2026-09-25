#!/usr/bin/env node
/**
 * check-tokens.mjs — T-002 gate evidence (run: `npm run check:tokens`).
 *
 * Proves, mechanically:
 *  1. `styles/tokens.css` defines exactly the 15 design-system tokens, per theme.
 *  2. The 14 palette tokens of each theme equal `design/brand-kit/palette.md`
 *     row-for-row (row order of the palette tables == token order here), so the
 *     hexes are 1:1 and nothing was invented.
 *  3. `--shadow` matches the wireframe/order values.
 *  4. No hex color literal exists anywhere else in `frontend/` (tokens only).
 */
import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const frontend = resolve(here, "..");
const repo = resolve(frontend, "..");
const palettePath = join(repo, "design", "brand-kit", "palette.md");
const tokensPath = join(frontend, "styles", "tokens.css");

const TOKENS = [
  "bg", "card", "surface2", "text", "soft", "border", "primary", "primary-h",
  "on-primary", "primary-bg", "sage", "sage-bg", "clay", "clay-bg", "shadow",
];
const PALETTE_TOKENS = TOKENS.filter((token) => token !== "shadow");
const EXPECTED_SHADOW = {
  light: "0 10px 30px rgba(43, 53, 66, .08)",
  dark: "0 10px 30px rgba(0, 0, 0, .35)",
};

const failures = [];
const check = (ok, message) => {
  if (!ok) failures.push(message);
  console.log(`${ok ? "ok  " : "FAIL"} ${message}`);
};

const hexesOf = (text) => text.match(/#[0-9A-Fa-f]{6}/g) ?? [];

/* ---------- 1. palette.md tables ---------- */
if (!existsSync(palettePath)) {
  console.error(
    `FAIL cannot read ${relative(repo, palettePath)}\n` +
      "     This lane gate must run from a repo checkout (the Docker build context is\n" +
      "     ./frontend only, so it is intentionally NOT part of `npm run build`).",
  );
  process.exit(1);
}
const palette = readFileSync(palettePath, "utf8");
const themeSection = (heading) => {
  const start = palette.indexOf(heading);
  if (start === -1) throw new Error(`palette.md: section "${heading}" not found`);
  const rest = palette.slice(start + heading.length);
  const end = rest.indexOf("\n## ");
  return end === -1 ? rest : rest.slice(0, end);
};
const paletteLight = hexesOf(themeSection("## تم روشن")).map((h) => h.toUpperCase());
const paletteDark = hexesOf(themeSection("## تم تیره")).map((h) => h.toUpperCase());

/* ---------- 2. tokens.css themes ---------- */
const tokens = readFileSync(tokensPath, "utf8");
const themeBlock = (theme) => {
  const marker = `:root[data-theme="${theme}"] {`;
  const start = tokens.indexOf(marker);
  if (start === -1) throw new Error(`tokens.css: block "${marker}" not found`);
  const end = tokens.indexOf("}", start);
  return tokens.slice(start + marker.length, end);
};
const varsOf = (block) => {
  const vars = new Map();
  for (const line of block.split("\n")) {
    const match = /^\s*--([a-z0-9-]+)\s*:\s*(.+?);\s*$/.exec(line);
    if (match) vars.set(match[1], match[2].trim());
  }
  return vars;
};

const lightVars = varsOf(themeBlock("light"));
const darkVars = varsOf(themeBlock("dark"));

for (const [theme, vars, paletteHexes] of [
  ["light", lightVars, paletteLight],
  ["dark", darkVars, paletteDark],
]) {
  check(
    [...vars.keys()].filter((key) => key !== "color-scheme").join(",") === TOKENS.join(","),
    `${theme}: token names/order == design-system list (${TOKENS.length} tokens)`,
  );

  const cssHexes = PALETTE_TOKENS.map((token) => (vars.get(token) ?? "").toUpperCase());
  check(
    paletteHexes.length === PALETTE_TOKENS.length,
    `${theme}: palette.md exposes ${PALETTE_TOKENS.length} hexes (got ${paletteHexes.length})`,
  );
  const mismatches = cssHexes
    .map((hex, index) => ({ token: PALETTE_TOKENS[index], css: hex, palette: paletteHexes[index] }))
    .filter((row) => row.css !== row.palette);
  check(
    mismatches.length === 0,
    `${theme}: tokens.css hexes == palette.md row-for-row` +
      (mismatches.length === 0
        ? ""
        : ` — mismatches: ${mismatches.map((m) => `${m.token}: css ${m.css} vs palette ${m.palette}`).join("; ")}`),
  );

  check(
    vars.get("shadow") === EXPECTED_SHADOW[theme],
    `${theme}: --shadow == "${EXPECTED_SHADOW[theme]}"`,
  );
}

const cssHexSet = hexesOf(tokens).map((h) => h.toUpperCase());
const paletteHexSet = [...paletteLight, ...paletteDark].sort();
check(
  JSON.stringify([...cssHexSet].sort()) === JSON.stringify(paletteHexSet),
  "tokens.css hex set == palette.md hex set (bidirectional, incl. duplicates)",
);

/* ---------- 3. no hexes anywhere else in frontend/ ---------- */
const SOURCE_DIRS = ["app", "components", "lib", "styles", "scripts"];
const SOURCE_FILES = ["next.config.ts", "postcss.config.mjs", "eslint.config.mjs", "package.json", "tsconfig.json"];
const walk = (dir) => {
  const out = [];
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    if (statSync(full).isDirectory()) {
      if (["node_modules", ".next", "public", "out"].includes(entry)) continue;
      out.push(...walk(full));
    } else {
      out.push(full);
    }
  }
  return out;
};

const scanned = [
  ...SOURCE_DIRS.flatMap((dir) => walk(join(frontend, dir))),
  ...SOURCE_FILES.map((file) => join(frontend, file)),
].filter((file) => file !== tokensPath);

const offenders = scanned.flatMap((file) =>
  hexesOf(readFileSync(file, "utf8")).map((hex) => `${relative(repo, file)}: ${hex}`),
);
check(offenders.length === 0, `no hex literals outside styles/tokens.css (scanned ${scanned.length} files)`);
for (const offender of offenders) console.log(`     ${offender}`);

console.log(
  failures.length === 0
    ? `\nOK: tokens 1:1 with palette.md, ${scanned.length} files scanned, 0 stray hexes`
    : `\nFAIL: ${failures.length} token check(s) failed`,
);
process.exit(failures.length === 0 ? 0 : 1);
