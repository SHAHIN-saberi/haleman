"use client";

import { useCallback, useSyncExternalStore } from "react";

type Theme = "light" | "dark";

const STORAGE_KEY = "haleman-theme";
const THEME_EVENT = "haleman-theme-change";

function applyTheme(theme: Theme): void {
  const root = document.documentElement;
  root.setAttribute("data-theme", theme);
  root.style.colorScheme = theme;
}

function storedTheme(): Theme | null {
  try {
    const value = window.localStorage.getItem(STORAGE_KEY);
    return value === "light" || value === "dark" ? value : null;
  } catch {
    return null;
  }
}

/** The DOM attribute set by the pre-hydration bootstrap script IS the state. */
function currentTheme(): Theme {
  return document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "light";
}

function subscribe(onThemeChange: () => void): () => void {
  const query = window.matchMedia("(prefers-color-scheme: dark)");
  const onSystemChange = (event: MediaQueryListEvent) => {
    if (storedTheme()) return; // explicit user choice wins over the OS
    applyTheme(event.matches ? "dark" : "light");
    onThemeChange();
  };

  query.addEventListener("change", onSystemChange);
  window.addEventListener(THEME_EVENT, onThemeChange); // toggles in this tab
  window.addEventListener("storage", onThemeChange); // other tabs
  return () => {
    query.removeEventListener("change", onSystemChange);
    window.removeEventListener(THEME_EVENT, onThemeChange);
    window.removeEventListener("storage", onThemeChange);
  };
}

/**
 * ThemeToggle — pill button per design/design-system.md.
 * The theme lives in the DOM (`data-theme`), written before paint by the inline
 * bootstrap script; `localStorage["haleman-theme"]` only records an explicit
 * choice (without it the OS preference stays live). No theme flash, no effect
 * that writes state back into React.
 */
export default function ThemeToggle() {
  const theme = useSyncExternalStore(subscribe, currentTheme, () => "light" as Theme);

  const toggle = useCallback(() => {
    const next: Theme = currentTheme() === "dark" ? "light" : "dark";
    try {
      window.localStorage.setItem(STORAGE_KEY, next);
    } catch {
      /* private mode / storage disabled: the theme still applies for this session */
    }
    applyTheme(next);
    window.dispatchEvent(new Event(THEME_EVENT));
  }, []);

  return (
    <button
      type="button"
      onClick={toggle}
      aria-label="تغییر تم روشن و تیره"
      aria-pressed={theme === "dark"}
      className="inline-flex min-h-11 items-center justify-center rounded-full bg-primary px-5 text-[13.5px] font-bold text-on-primary transition-colors hover:bg-primary-h"
    >
      {/*
       * Both labels are rendered and CSS picks one from `html[data-theme]`,
       * which the inline bootstrap sets before first paint. So the label is
       * right even before hydration (no «تم تیره» flash for stored-dark users).
       */}
      <span className="in-data-[theme=dark]:hidden">تم تیره</span>
      <span className="hidden in-data-[theme=dark]:inline">تم روشن</span>
    </button>
  );
}
