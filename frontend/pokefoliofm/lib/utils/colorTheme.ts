// utils/colorTheme.ts
export const colorThemeMap: Record<
  string,
  { primary: string; secondary: string; accent: string }
> = {
  blue: { primary: "#3b82f6", secondary: "#60a5fa", accent: "#93c5fd" },
  brown: { primary: "#a16207", secondary: "#d97706", accent: "#fbbf24" },
  yellow: { primary: "#facc15", secondary: "#fde047", accent: "#fef08a" },
  green: { primary: "#16a34a", secondary: "#4ade80", accent: "#86efac" },
  red: { primary: "#dc2626", secondary: "#f87171", accent: "#fca5a5" },
  purple: { primary: "#9333ea", secondary: "#a855f7", accent: "#c084fc" },
  gray: { primary: "#6b7280", secondary: "#9ca3af", accent: "#d1d5db" },
  pink: { primary: "#ec4899", secondary: "#f472b6", accent: "#f9a8d4" },
  white: { primary: "#f3f4f6", secondary: "#e5e7eb", accent: "#d1d5db" },
  black: { primary: "#111827", secondary: "#374151", accent: "#6b7280" },
};
