"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Button from "@/components/ui/Button";
import { ApiError, getChat } from "@/lib/api";

/**
 * /chat — M1 placeholder (T-003B; the real W-03 conversation lands in T-005).
 *
 * The server is the gate, not the client: `GET /api/chat/` answers
 * 403 `consent_required` when the device has no informed consent on record, and
 * this screen follows that answer back to /consent. No flag is kept in
 * localStorage, a cookie or component state to stand in for the server.
 */
export default function ChatPage() {
  const router = useRouter();
  const [status, setStatus] = useState<"checking" | "ready" | "unreachable">("checking");
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    let cancelled = false;
    getChat()
      .then(() => {
        if (!cancelled) setStatus("ready");
      })
      .catch((reason: unknown) => {
        if (cancelled) return;
        if (reason instanceof ApiError && reason.status === 403) {
          router.replace("/consent");
          return;
        }
        setStatus("unreachable");
        if (process.env.NODE_ENV !== "production") {
          console.warn("[haleman] /api/chat/ unavailable", reason);
        }
      });
    return () => {
      cancelled = true;
    };
  }, [router, attempt]);

  if (status === "unreachable") {
    return (
      <div className="flex flex-1 flex-col justify-end">
        <div className="flex flex-col items-center gap-3 rounded-xl border border-border bg-card px-3 py-4">
          <p className="text-[12px] leading-[1.9] text-soft">ارتباط برقرار نشد.</p>
          <Button type="button" variant="soft" onClick={() => setAttempt((value) => value + 1)}>
            تلاش دوباره
          </Button>
        </div>
      </div>
    );
  }

  if (status === "checking") {
    /* Blank until the server answers: a redirected visitor should not read a
       chat screen on the way to /consent. */
    return <div className="flex-1" aria-busy="true" />;
  }

  return (
    <div className="flex flex-1 flex-col">
      <p className="max-w-[85%] self-start rounded-[16px] rounded-ss-[4px] border border-border bg-card px-3 py-2 text-[13.5px] leading-[1.9]">
        سلام! امروز روزت چطور گذشت؟
      </p>

      <div className="mt-auto flex items-center gap-2 pt-3">
        <input
          disabled
          aria-label="متن پیام"
          placeholder="بنویس..."
          className="min-h-11 flex-1 rounded-full border border-border bg-card px-4 text-[13px] text-text placeholder:text-soft disabled:opacity-60"
        />
        <Button type="button" className="px-5" disabled>
          ارسال
        </Button>
      </div>
    </div>
  );
}
