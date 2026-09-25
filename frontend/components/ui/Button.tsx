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
  soft: "bg-primary-bg text-primary hover:bg-primary-h hover:text-on-primary",
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
