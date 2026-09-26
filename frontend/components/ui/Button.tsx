import type { ButtonHTMLAttributes } from "react";

export type ButtonVariant = "primary" | "ghost" | "soft";

/**
 * `buttonClass()` keeps the button anatomy (design/design-system.md: pill radius,
 * min-height 44px, hover → primary-h, disabled 40% opacity, visible focus ring)
 * in one place so links styled as buttons stay identical to <Button/>.
 */
const BASE =
  "inline-flex min-h-11 items-center justify-center gap-2 rounded-full px-6 text-[13.5px] font-bold transition-colors " +
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary " +
  "disabled:cursor-not-allowed disabled:opacity-40";

const VARIANTS: Record<ButtonVariant, string> = {
  primary: "bg-primary text-on-primary hover:bg-primary-h",
  ghost: "border-[1.5px] border-primary bg-transparent text-primary hover:bg-primary-bg",
  // Soft is the only variant whose label colour differs per theme (palette v1.1):
  // light `--primary` on `--primary-bg` is 5.78:1, but dark `--primary` on `--primary-bg`
  // is 3.82:1, which fails tests.md §D. Darkening `--primary-bg` to fix it would flatten
  // the dark surfaces (contrast between the two surfaces 1.29 → 1.09), so the dark label
  // uses `--text` instead (10.4:1) and the surface stays soft. Hover keeps `on-primary`.
  soft: "bg-primary-bg text-primary hover:bg-primary-h hover:text-on-primary in-data-[theme=dark]:text-text in-data-[theme=dark]:hover:text-on-primary",
};

export function buttonClass(variant: ButtonVariant = "primary", className = ""): string {
  return [BASE, VARIANTS[variant], className].filter(Boolean).join(" ");
}

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: ButtonVariant;
};

export default function Button({ variant = "primary", className, ...rest }: ButtonProps) {
  return <button className={buttonClass(variant, className)} {...rest} />;
}
