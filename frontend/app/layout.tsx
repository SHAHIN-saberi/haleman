import type { Metadata, Viewport } from "next";
import AppHeader from "@/components/AppHeader";
import CrisisLayer from "@/components/CrisisLayer";
import "./globals.css";

export const metadata: Metadata = {
  title: "حال‌من",
  description: "قدم اول، ناشناس و امن — ابزار هوشمند برای بررسی اولیه حال روانی.",
};

// No `themeColor` here on purpose: meta tags cannot read CSS vars, and
// M1-orders-1.md T-002 §3 forbids hex values outside `styles/tokens.css`.
export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
};

/**
 * Pre-hydration theme bootstrap (T-002 §4).
 * Runs before first paint: stored choice wins, otherwise the system preference.
 * Keeps the light/dark tokens from `styles/tokens.css` free of a wrong-theme flash.
 */
const THEME_BOOTSTRAP = `(function(){try{var k="haleman-theme";var s=localStorage.getItem(k);var t=(s==="light"||s==="dark")?s:(window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light");var r=document.documentElement;r.setAttribute("data-theme",t);r.style.colorScheme=t;}catch(e){}})();`;

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="fa" dir="rtl" data-theme="light" suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: THEME_BOOTSTRAP }} />
      </head>
      <body className="bg-bg text-text">
        {/* Phone frame: max-width 480px centered, 360px still fine (design-system). */}
        <div className="mx-auto flex min-h-dvh w-full max-w-[480px] flex-col">
          <AppHeader />
          <main className="flex flex-1 flex-col px-4 pb-6 pt-4">{children}</main>
        </div>
        {/* Placeholder mounted on every route so T-015 (W-10) slots in later. */}
        <CrisisLayer />
      </body>
    </html>
  );
}
