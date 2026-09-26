import type { ButtonHTMLAttributes } from "react";

export type ButtonVariant = "primary" | "ghost" | "soft" | "clay";

/**
 * `buttonClass()` keeps the button anatomy (design/design-system.md: pill radius,
 * min-height 44px, hover → primary-h, disabled 40% opacity, visible focus ring)
 * in one place so links styled as buttons stay identical to <Button/>.
 *
 * F-2: the animated properties are declared one by one on purpose. Tailwind's
 * colour utility animates `outline-color` too, so the focus ring faded in from
 * the label colour (`--on-primary` on a primary button = the page bg in light
 * theme → ~100 ms of invisible ring). Background and label keep their animation;
 * the ring appears instantly. Utility names are avoided in prose here because the
 * compiler's source scanner reads comments as well.
 */
const BASE =
  "inline-flex min-h-11 items-center justify-center gap-2 rounded-full px-6 text-[13.5px] font-bold transition-[background-color,color] " +
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
  // Crisis call button (W-10, Q-07): clay surface with the `--on-primary` label the
  // wireframe's `.btn` uses over it (light 4.89:1, dark 5.58:1). Hover returns to the
  // soft clay pair (`--clay-bg` + `--clay`, light 4.51:1, dark 4.95:1) because the
  // palette has no `--clay-h` token and this button must never look louder.
  clay: "bg-clay text-on-primary hover:bg-clay-bg hover:text-clay",
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
