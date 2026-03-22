import { motion } from "framer-motion";
import DatePicker, { registerLocale } from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { ko } from "date-fns/locale/ko";

registerLocale("ko", ko);

interface BirthDateInputProps {
  name: string;
  onNameChange: (value: string) => void;
  birthDate: string;
  onBirthDateChange: (value: string) => void;
  disabled: boolean;
}

export default function BirthDateInput({
  name, onNameChange, birthDate, onBirthDateChange, disabled,
}: BirthDateInputProps) {
  const inputStyle = (filled: boolean) => ({
    background: "white",
    border: filled ? "2px solid #FF8C42" : "2px solid #FFE8D6",
    boxShadow: filled
      ? "0 0 0 3px rgba(255,140,66,0.1)"
      : "0 2px 8px rgba(0,0,0,0.03)",
  });

  const dateValue = birthDate ? new Date(birthDate + "T00:00:00") : null;

  const handleDateChange = (date: Date | null) => {
    if (date) {
      const y = date.getFullYear();
      const m = String(date.getMonth() + 1).padStart(2, "0");
      const d = String(date.getDate()).padStart(2, "0");
      onBirthDateChange(`${y}-${m}-${d}`);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}
      className="w-full max-w-xs mx-auto space-y-3"
    >
      <div>
        <label className="block text-base text-text-muted mb-1.5 text-center font-medium">
          이름을 알려주세요 🐱
        </label>
        <input
          type="text"
          value={name}
          onChange={(e) => onNameChange(e.target.value)}
          disabled={disabled}
          placeholder="예) 김행운"
          maxLength={10}
          className="w-full px-4 py-3 rounded-2xl text-text text-center text-base font-medium focus:outline-none transition-all disabled:opacity-40 placeholder:text-text-dim"
          style={inputStyle(!!name)}
        />
      </div>

      <div>
        <label className="block text-base text-text-muted mb-1.5 text-center font-medium">
          생년월일 🎂
        </label>
        <DatePicker
          selected={dateValue}
          onChange={handleDateChange}
          disabled={disabled}
          locale="ko"
          dateFormat="yyyy년 MM월 dd일"
          placeholderText="날짜를 선택하세요"
          maxDate={new Date()}
          minDate={new Date("1920-01-01")}
          renderCustomHeader={({
            date,
            changeYear,
            changeMonth,
          }) => {
            const years = Array.from({ length: new Date().getFullYear() - 1920 + 1 }, (_, i) => 1920 + i).reverse();
            const months = Array.from({ length: 12 }, (_, i) => i);
            return (
              <div style={{ display: "flex", justifyContent: "center", gap: 6, padding: "6px 0" }}>
                <select
                  value={date.getFullYear()}
                  onChange={({ target: { value } }) => changeYear(Number(value))}
                  style={{
                    padding: "4px 8px", borderRadius: 10, border: "1.5px solid #FFD6B0",
                    fontSize: 14, fontWeight: 600, background: "white", color: "#3D2C2C", cursor: "pointer",
                  }}
                >
                  {years.map((y) => <option key={y} value={y}>{y}년</option>)}
                </select>
                <select
                  value={date.getMonth()}
                  onChange={({ target: { value } }) => changeMonth(Number(value))}
                  style={{
                    padding: "4px 8px", borderRadius: 10, border: "1.5px solid #FFD6B0",
                    fontSize: 14, fontWeight: 600, background: "white", color: "#3D2C2C", cursor: "pointer",
                  }}
                >
                  {months.map((m) => <option key={m} value={m}>{m + 1}월</option>)}
                </select>
              </div>
            );
          }}
          className="w-full px-4 py-3 rounded-2xl text-text text-center text-base font-medium focus:outline-none transition-all disabled:opacity-40 placeholder:text-text-dim cursor-pointer"
          wrapperClassName="w-full"
          popperClassName="cute-datepicker"
        />
      </div>

      <style>{`
        .react-datepicker {
          font-family: "Pretendard Variable", "Pretendard", sans-serif !important;
          border: 2px solid #FFE8D6 !important;
          border-radius: 20px !important;
          box-shadow: 0 8px 30px rgba(255, 140, 66, 0.12) !important;
          overflow: hidden;
        }
        .react-datepicker__header {
          background: #FFF5E8 !important;
          border-bottom: 2px solid #FFE8D6 !important;
          border-radius: 0 !important;
          padding-top: 12px !important;
        }
        .react-datepicker__current-month {
          color: #3D2C2C !important;
          font-weight: 700 !important;
          font-size: 15px !important;
          margin-bottom: 8px !important;
        }
        .react-datepicker__day-name {
          color: #9B8A8A !important;
          font-weight: 600 !important;
          font-size: 12px !important;
          width: 36px !important;
          line-height: 36px !important;
        }
        .react-datepicker__day {
          width: 36px !important;
          line-height: 36px !important;
          border-radius: 50% !important;
          color: #3D2C2C !important;
          font-weight: 500 !important;
          transition: all 0.15s !important;
        }
        .react-datepicker__day:hover {
          background: #FFE8D6 !important;
          border-radius: 50% !important;
        }
        .react-datepicker__day--selected {
          background: #FF8C42 !important;
          color: white !important;
          font-weight: 700 !important;
        }
        .react-datepicker__day--selected:hover {
          background: #E87830 !important;
        }
        .react-datepicker__day--today {
          font-weight: 800 !important;
          color: #FF8C42 !important;
        }
        .react-datepicker__day--today.react-datepicker__day--selected {
          color: white !important;
        }
        .react-datepicker__day--outside-month {
          color: #D4C4C4 !important;
        }
        .react-datepicker__navigation {
          top: 12px !important;
        }
        .react-datepicker__navigation-icon::before {
          border-color: #FF8C42 !important;
          border-width: 2px 2px 0 0 !important;
        }
        .react-datepicker__triangle {
          display: none !important;
        }
        .react-datepicker__year-dropdown,
        .react-datepicker__month-dropdown {
          background: white !important;
          border: 2px solid #FFE8D6 !important;
          border-radius: 12px !important;
          box-shadow: 0 4px 16px rgba(0,0,0,0.08) !important;
        }
        .react-datepicker__year-option,
        .react-datepicker__month-option {
          padding: 4px 12px !important;
          font-size: 13px !important;
        }
        .react-datepicker__year-option:hover,
        .react-datepicker__month-option:hover {
          background: #FFF5E8 !important;
        }
        .react-datepicker__year-option--selected_year,
        .react-datepicker__month-option--selected_month {
          color: #FF8C42 !important;
          font-weight: 700 !important;
        }
        .react-datepicker__year-read-view,
        .react-datepicker__month-read-view {
          font-size: 14px !important;
          padding: 2px 8px !important;
          border: 1.5px solid #FFD6B0 !important;
          border-radius: 10px !important;
          background: white !important;
        }
        .react-datepicker__year-read-view:hover,
        .react-datepicker__month-read-view:hover {
          border-color: #FF8C42 !important;
        }
        .react-datepicker__year-read-view--down-arrow,
        .react-datepicker__month-read-view--down-arrow {
          border-color: #FF8C42 !important;
          border-width: 2px 2px 0 0 !important;
        }
        .react-datepicker-popper {
          z-index: 50 !important;
        }
        .react-datepicker__input-container input {
          background: white;
          border: 2px solid #FFE8D6;
          box-shadow: 0 2px 8px rgba(0,0,0,0.03);
          border-radius: 16px;
        }
        .react-datepicker__input-container input:focus {
          border-color: #FF8C42;
          box-shadow: 0 0 0 3px rgba(255,140,66,0.1);
          outline: none;
        }
        .react-datepicker__day-name:first-child,
        .react-datepicker__day:nth-child(7n+1) {
          color: #FF6B6B !important;
        }
        .react-datepicker__day-name:last-child,
        .react-datepicker__day:nth-child(7n) {
          color: #4A90D9 !important;
        }
        .react-datepicker__day--selected:nth-child(7n+1),
        .react-datepicker__day--selected:nth-child(7n) {
          color: white !important;
        }
      `}</style>
    </motion.div>
  );
}
