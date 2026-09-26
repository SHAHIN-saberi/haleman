"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import Button from "@/components/ui/Button";
import { getMe, postConsent } from "@/lib/api";

/**
 * W-02 — informed consent (product/wireframes/index.html, screen W-02 · US-05).
 * Copy is byte-exact from the wireframe, ZWNJ (U+200C) included.
 *
 * This screen keeps no consent state of its own: the row is written by
 * `POST /api/consent/` (T-003A) and the server is the only gate. On mount it
 * reads `/api/me/` once — with the shared cache deliberately bypassed — so a
 * device whose consent is already on record is not asked twice.
 */
const CONSENT_LINES = [
  "اینجا با یک ابزار هوشمند حرف می‌زنی، نه درمانگر. این گفت‌وگو تشخیص و درمان نیست.",
  "ناشناسی؛ هیچ‌چیز بدون اجازه‌ات برای کسی ارسال نمی‌شود.",
  "در بحران، فوراً راه کمک اضطراری می‌گیری.",
];

export default function ConsentPage() {
  const router = useRouter();
  const [pending, setPending] = useState(false);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    let cancelled = false;
    getMe()
      .then((me) => {
        if (!cancelled && me.consent?.informed === true) router.replace("/chat");
      })
      .catch(() => {
        /* Offline or backend down: the screen still renders and the button reports it. */
      });
    return () => {
      cancelled = true;
    };
  }, [router]);

  async function accept() {
    if (pending) return;
    setPending(true);
    setFailed(false);
    try {
      await postConsent();
      router.replace("/chat");
    } catch (reason: unknown) {
      setPending(false);
      setFailed(true);
      if (process.env.NODE_ENV !== "production") {
        console.warn("[haleman] consent POST failed", reason);
      }
    }
  }

  return (
    <div className="flex flex-1 flex-col gap-2.5">
      <h1 className="mb-1 text-[17px] font-bold leading-[2]">قبل از شروع</h1>

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

      {/* Wireframe W-02 keeps the action right under the cards (no bottom anchoring). */}
      <div className="flex flex-col gap-2 pt-4">
        {failed && (
          <p role="alert" className="text-[12px] leading-[1.9] text-clay">
            ارتباط برقرار نشد. لطفاً دوباره تلاش کن.
          </p>
        )}
        <Button type="button" className="w-full" onClick={accept} disabled={pending} aria-busy={pending}>
          فهمیدم، شروع کن
        </Button>
        <Link
          href="/terms"
          className="min-h-11 rounded-full py-3 text-center text-[12px] text-soft transition-[color] hover:text-primary focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
        >
          متن کامل قوانین و حریم خصوصی
        </Link>
      </div>
    </div>
  );
}
