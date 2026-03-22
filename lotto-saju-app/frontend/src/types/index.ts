export interface Elements {
  wood: number;
  fire: number;
  earth: number;
  metal: number;
  water: number;
}

export interface UserSaju {
  year: string;
  month: string;
  day: string;
  elements: Elements;
  lacking: string;
  lacking_all?: string[];
}

export interface TodayEnergy {
  stem: string;
  branch: string;
  element: string;
}

export interface LottoResponse {
  numbers: number[];
  reason: string;
  user_saju: UserSaju;
  today_energy: TodayEnergy;
}

export type ElementType = "wood" | "fire" | "earth" | "metal" | "water";

export const ELEMENT_LABELS: Record<string, string> = {
  wood: "목(木)",
  fire: "화(火)",
  earth: "토(土)",
  metal: "금(金)",
  water: "수(水)",
};

export const ELEMENT_COLORS: Record<string, string> = {
  wood: "#4CAF50",
  fire: "#FF6B6B",
  earth: "#D4A373",
  metal: "#90A4AE",
  water: "#42A5F5",
};

export const ELEMENT_ICONS: Record<string, string> = {
  wood: "ri-plant-fill",
  fire: "ri-fire-fill",
  earth: "ri-landscape-fill",
  metal: "ri-coin-fill",
  water: "ri-drop-fill",
};
