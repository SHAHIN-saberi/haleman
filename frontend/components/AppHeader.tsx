"use client";

import { usePathname } from "next/navigation";
import ThemeToggle from "@/components/ThemeToggle";

/**
 * App header shared by every route (root layout).
 * T-002F(3): wireframe W-01 (`/`) has no header brand — the page's own H1
 * «حال‌من» is the brand there — so the brand text is omitted on `/` only.
 * `<ThemeToggle/>` stays in the same place (inline-end) on every route,
 * and every other route keeps the brand.
 * `usePathname()` is resolved during prerender, so the served HTML is already
 * correct before hydration (no brand flash on `/`).
 */
export default function AppHeader() {
  const showBrand = usePathname() !== "/";

  return (
    <header
      className={`flex items-center gap-3 border-b border-border bg-card px-4 py-3 ${
        showBrand ? "justify-between" : "justify-end"
      }`}
    >
      {showBrand && <span className="text-[17px] font-bold">حال‌من</span>}
      <ThemeToggle />
    </header>
  );
}
