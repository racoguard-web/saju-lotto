export default function Background() {
  return (
    <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden">
      {/* Soft warm gradient overlay */}
      <div
        className="absolute inset-0"
        style={{
          background: "radial-gradient(circle at 50% 0%, rgba(255,209,102,0.15) 0%, transparent 60%)",
        }}
      />
      {/* Floating decorations */}
      <div className="absolute text-7xl opacity-[0.07]" style={{ top: "5%", left: "3%" }}>🐾</div>
      <div className="absolute text-6xl opacity-[0.07]" style={{ top: "18%", right: "5%" }}>✨</div>
      <div className="absolute text-7xl opacity-[0.07]" style={{ bottom: "22%", left: "2%" }}>🍀</div>
      <div className="absolute text-6xl opacity-[0.07]" style={{ bottom: "8%", right: "5%" }}>🎰</div>
      <div className="absolute text-5xl opacity-[0.06]" style={{ top: "45%", right: "2%" }}>🐱</div>
      <div className="absolute text-5xl opacity-[0.06]" style={{ top: "65%", left: "4%" }}>⭐</div>
    </div>
  );
}
