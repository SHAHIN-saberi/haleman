import { buttonClass } from "@/components/ui/Button";

/**
 * CrisisLayer — W-10 slot, mounted once in the root layout so it exists on
 * every route (product rule 2; `tech/tests.md` §C.2).
 *
 * Q-07 (owner-approved 2026-09-26): M1 shows the minimal always-visible referral
 * line — the W-10 call button «تماس با اورژانس ۱۱۵» as a `tel:` link, byte-exact
 * copy. T-015 replaces this bar with the full overlay (empathy card, flow pause,
 * ghost «حالا امنم، ادامه میدهم»), so nothing here is final UI.
 *
 * `sticky`, not `fixed`, on purpose: the bar keeps its place in the flow, so it
 * can never cover the last control of a page and no page needs added padding.
 */
export default function CrisisLayer() {
  return (
    <div className="sticky bottom-0 z-20 bg-bg px-4 pb-3 pt-2">
      <a href="tel:115" className={buttonClass("clay", "w-full")}>
        تماس با اورژانس ۱۱۵
      </a>
    </div>
  );
}
