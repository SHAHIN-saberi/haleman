import { defineConfig, globalIgnores } from "eslint/config";
import nextCoreWebVitals from "eslint-config-next/core-web-vitals";

/**
 * Flat ESLint config (ESLint CLI, `npm run lint`).
 * `eslint-config-next` v16 exports flat-config arrays; no extra plugins/deps.
 */
export default defineConfig([
  ...nextCoreWebVitals,
  globalIgnores([
    ".next/**",
    "out/**",
    "node_modules/**",
    "next-env.d.ts",
    "public/**",
  ]),
]);
