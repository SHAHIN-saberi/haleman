/**
 * Presentation-only helpers (no business logic — frontend/README.md).
 * Persian digits for every user-facing number (`tech/tests.md` §D).
 */

const FA_DIGITS = ["۰", "۱", "۲", "۳", "۴", "۵", "۶", "۷", "۸", "۹"] as const;

export function toFaDigits(value: string | number): string {
  return String(value).replace(/[0-9]/g, (digit) => FA_DIGITS[Number(digit)] ?? digit);
}
