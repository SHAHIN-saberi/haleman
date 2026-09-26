import type { Metadata } from "next";

export const metadata: Metadata = { title: "قوانین و حریم خصوصی" };

/**
 * /terms — stub (T-003B). Copy approved at the T-003B plan gate (2026-09-26):
 * heading + the three W-02 consent lines + one line saying the full text is
 * still with the owner/legal (Q-08 open). No legal sentence is invented here;
 * the older one-line variant in M1-orders-1.md §T-003B-1 is superseded by that
 * approval (see the T-003B report, deviation D-1).
 */
const CONSENT_LINES = [
  "اینجا با یک ابزار هوشمند حرف می‌زنی، نه درمانگر. این گفت‌وگو تشخیص و درمان نیست.",
  "ناشناسی؛ هیچ‌چیز بدون اجازه‌ات برای کسی ارسال نمی‌شود.",
  "در بحران، فوراً راه کمک اضطراری می‌گیری.",
];

export default function TermsPage() {
  return (
    <div className="flex flex-1 flex-col gap-2.5">
      <h1 className="mb-1 text-[17px] font-bold leading-[2]">قوانین و حریم خصوصی</h1>

      {CONSENT_LINES.map((line) => (
        <p
          key={line}
          className="flex items-start gap-2 rounded-xl border border-border bg-card px-3 py-2.5 text-[12px] leading-[1.9]"
        >
          <span aria-hidden="true" className="text-sage">
            ✓
          </span>
          <span>{line}</span>
        </p>
      ))}

      <p className="text-[12px] leading-[1.9] text-soft">متن کامل پس از تأیید حقوقی منتشر می‌شود.</p>
    </div>
  );
}
