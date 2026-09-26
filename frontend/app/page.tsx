import Link from "next/link";
import DeviceSession from "@/components/DeviceSession";
import { buttonClass } from "@/components/ui/Button";

/**
 * W-01 — welcome screen (product/wireframes/index.html, screen W-01 · US-01/US-05).
 * Copy is byte-exact from the wireframe, ZWNJ (U+200C) included in «حال‌من» / «گفت‌وگو».
 */
export default function HomePage() {
  return (
    <div className="flex flex-1 flex-col items-center justify-center gap-6">
      {/* Kicks off the anonymous device token; renders nothing. */}
      <DeviceSession />

      <div className="flex flex-col items-center text-center">
        <h1 className="text-[26px] font-bold leading-[2]">حال‌من</h1>
        <p className="text-[13px] leading-[2] text-soft">
          حالت چطوره؟
          <br />
          قدم اول، ناشناس و امن
        </p>
      </div>

      <div className="flex w-full flex-col items-center gap-3">
        <Link href="/consent" className={buttonClass("primary", "w-full")}>
          شروع گفت‌وگو
        </Link>
        {/*
         * Non-navigating for now: the «چطور کار می‌کند؟» target is an open
         * question (Q-08, pointed at the supervisors). Kept focusable so the
         * screen stays keyboard-complete — see T-002 report, deviation D-1.
         */}
        <button
          type="button"
          className="min-h-11 rounded-full bg-transparent px-4 text-[12px] text-soft transition-[color] hover:text-primary focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
        >
          چطور کار می‌کند؟
        </button>
      </div>
    </div>
  );
}
