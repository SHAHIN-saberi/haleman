import Link from "next/link";
import { buttonClass } from "@/components/ui/Button";

/**
 * 404 (Q-11, owner-approved 2026-09-26): the Next default is English, which
 * breaks the Persian-only rule — this replaces it. Copy is byte-exact:
 * «این صفحه پیدا نشد» / «شاید نشانی را اشتباه وارد کرده‌ای.» / «بازگشت به خانه».
 */
export default function NotFound() {
  return (
    <div className="flex flex-1 flex-col items-center justify-center gap-4 text-center">
      <h1 className="text-[22px] font-bold leading-[2]">این صفحه پیدا نشد</h1>
      <p className="text-[12px] leading-[1.9] text-soft">شاید نشانی را اشتباه وارد کرده‌ای.</p>
      <Link href="/" className={buttonClass("primary")}>
        بازگشت به خانه
      </Link>
    </div>
  );
}
