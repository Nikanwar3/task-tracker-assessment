import { PRIORITIES, STATUSES, STATUS_LABELS, PRIORITY_LABELS } from "../utils/constants";

export default function FilterBar({ filters, onChange }) {
  return (
    <div className="filter-bar">
      <label>
        Status
        <select
          value={filters.status}
          onChange={(e) => onChange({ ...filters, status: e.target.value })}
        >
          <option value="">All</option>
          {STATUSES.map((s) => (
            <option key={s} value={s}>
              {STATUS_LABELS[s]}
            </option>
          ))}
        </select>
      </label>

      <label>
        Priority
        <select
          value={filters.priority}
          onChange={(e) => onChange({ ...filters, priority: e.target.value })}
        >
          <option value="">All</option>
          {PRIORITIES.map((p) => (
            <option key={p} value={p}>
              {PRIORITY_LABELS[p]}
            </option>
          ))}
        </select>
      </label>

      <button
        className="btn btn-secondary"
        onClick={() => onChange({ status: "", priority: "" })}
      >
        Clear Filters
      </button>
    </div>
  );
}
