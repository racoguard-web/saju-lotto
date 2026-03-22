import { motion } from "framer-motion";
import type { UserSaju, TodayEnergy } from "../types";
import { ELEMENT_LABELS, ELEMENT_COLORS, ELEMENT_ICONS } from "../types";

interface FortuneCardProps {
  saju: UserSaju;
  todayEnergy: TodayEnergy;
}

const ELEMENT_KEYS = ["wood", "fire", "earth", "metal", "water"] as const;
const ELEMENT_KR: Record<string, string> = {
  wood: "목", fire: "화", earth: "토", metal: "금", water: "수",
};

function ElementBar({ element, count, isLacking, maxCount }: {
  element: string; count: number; isLacking: boolean; maxCount: number;
}) {
  const color = ELEMENT_COLORS[element] || "#A8B8C8";
  const icon = ELEMENT_ICONS[element] || "ri-question-fill";
  const label = ELEMENT_LABELS[element] || element;
  const pct = maxCount > 0 ? (count / maxCount) * 100 : 0;

  return (
    <div className="flex items-center gap-3">
      <div className="w-8 h-8 rounded-xl flex items-center justify-center shrink-0"
        style={{ background: `${color}20`, color }}>
        <i className={`${icon} text-sm`} />
      </div>
      <div className="flex-1 min-w-0">
        <div className="flex justify-between items-center mb-1">
          <span className="text-xs text-text-muted">{label}</span>
          <span className="text-xs font-bold" style={{ color }}>{count}</span>
        </div>
        <div className="h-2 rounded-full overflow-hidden" style={{ background: `${color}15` }}>
          <motion.div initial={{ width: 0 }} animate={{ width: `${pct}%` }}
            transition={{ duration: 0.8, ease: "easeOut" }}
            className="h-full rounded-full" style={{ background: color }} />
        </div>
      </div>
      {isLacking && (
        <span className="text-[10px] px-2 py-0.5 rounded-full font-bold shrink-0"
          style={{ background: "#FFF0E5", color: "#FF8C42" }}>
          보완
        </span>
      )}
    </div>
  );
}

export default function FortuneCard({ saju, todayEnergy }: FortuneCardProps) {
  const maxCount = Math.max(...Object.values(saju.elements), 1);

  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
      className="card p-5 sm:p-6">
      <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
        🔮 사주 분석
      </h3>

      {/* Pillars */}
      <div className="grid grid-cols-3 gap-2 mb-5">
        {[
          { label: "년주", value: saju.year },
          { label: "월주", value: saju.month },
          { label: "일주", value: saju.day },
        ].map((p, i) => (
          <motion.div key={p.label} initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }}
            className="rounded-2xl p-3 text-center"
            style={{ background: "#FFF8F0", border: "1.5px solid #FFE8D6" }}>
            <div className="text-[10px] text-text-muted mb-1 font-medium">{p.label}</div>
            <div className="text-2xl font-extrabold" style={{ color: "#FF8C42" }}>{p.value}</div>
          </motion.div>
        ))}
      </div>

      {/* Elements */}
      <div className="space-y-2.5 mb-5">
        {ELEMENT_KEYS.map((key) => (
          <ElementBar key={key} element={key} count={saju.elements[key]}
            isLacking={(saju.lacking_all || [saju.lacking]).includes(key)} maxCount={maxCount} />
        ))}
      </div>

      {/* Today energy */}
      <div className="rounded-2xl p-4 flex items-center gap-3"
        style={{ background: "#FFF8F0", border: "1.5px solid #FFE8D6" }}>
        <div className="w-10 h-10 rounded-full flex items-center justify-center text-lg"
          style={{ background: "#FFE8D6" }}>☀️</div>
        <div>
          <div className="text-[10px] text-text-muted font-medium">오늘의 기운</div>
          <div className="text-sm font-bold text-text">
            {todayEnergy.stem}{todayEnergy.branch}
            <span className="ml-1.5" style={{ color: "#FF8C42" }}>
              ({ELEMENT_KR[todayEnergy.element] || todayEnergy.element})
            </span>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
