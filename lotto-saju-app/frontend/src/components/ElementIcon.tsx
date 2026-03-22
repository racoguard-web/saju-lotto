import { ELEMENT_ICONS, ELEMENT_LABELS, ELEMENT_COLORS } from "../types";

interface ElementIconProps {
  element: string;
  size?: "sm" | "md" | "lg";
  showLabel?: boolean;
}

export default function ElementIcon({
  element,
  size = "md",
  showLabel = false,
}: ElementIconProps) {
  const icon = ELEMENT_ICONS[element] || "ri-question-fill";
  const label = ELEMENT_LABELS[element] || element;
  const color = ELEMENT_COLORS[element] || "#94A3B8";

  const sizeClasses = {
    sm: "w-7 h-7 text-xs",
    md: "w-10 h-10 text-base",
    lg: "w-14 h-14 text-xl",
  };

  return (
    <div className="flex flex-col items-center gap-1">
      <div
        className={`${sizeClasses[size]} rounded-lg flex items-center justify-center`}
        style={{
          backgroundColor: `${color}15`,
          color: color,
          border: `1px solid ${color}30`,
        }}
      >
        <i className={icon} />
      </div>
      {showLabel && (
        <span className="text-[10px] text-text-muted">{label}</span>
      )}
    </div>
  );
}
