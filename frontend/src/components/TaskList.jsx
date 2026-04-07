import { STATUS_LABELS, PRIORITY_LABELS, ALLOWED_TRANSITIONS } from "../utils/constants";

const PRIORITY_CLASS = { low: "priority-low", medium: "priority-medium", high: "priority-high" };
const STATUS_CLASS = {
  todo: "status-todo",
  in_progress: "status-in-progress",
  done: "status-done",
  archived: "status-archived",
};

export default function TaskList({ tasks, onEdit, onStatusChange, onDelete, loading }) {
  if (loading) return <p className="state-msg">Loading tasks...</p>;
  if (!tasks.length) return <p className="state-msg">No tasks found. Create one above.</p>;

  return (
    <div className="task-list">
      {tasks.map((task) => (
        <TaskCard
          key={task.id}
          task={task}
          onEdit={onEdit}
          onStatusChange={onStatusChange}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
}

function TaskCard({ task, onEdit, onStatusChange, onDelete }) {
  const nextStatuses = ALLOWED_TRANSITIONS[task.status] || [];

  return (
    <div className={`task-card ${STATUS_CLASS[task.status]}`}>
      <div className="task-card-header">
        <span className={`badge ${PRIORITY_CLASS[task.priority]}`}>
          {PRIORITY_LABELS[task.priority]}
        </span>
        <span className={`badge ${STATUS_CLASS[task.status]}`}>
          {STATUS_LABELS[task.status]}
        </span>
      </div>

      <h3 className="task-title">{task.title}</h3>

      {task.description && <p className="task-desc">{task.description}</p>}

      {task.due_date && (
        <p className="task-due">
          Due: <strong>{task.due_date}</strong>
        </p>
      )}

      <div className="task-card-actions">
        {task.status !== "archived" && (
          <button className="btn btn-sm btn-secondary" onClick={() => onEdit(task)}>
            Edit
          </button>
        )}

        {nextStatuses.map((s) => (
          <button
            key={s}
            className="btn btn-sm btn-primary"
            onClick={() => onStatusChange(task.id, s)}
          >
            → {STATUS_LABELS[s]}
          </button>
        ))}

        <button className="btn btn-sm btn-danger" onClick={() => onDelete(task.id)}>
          Delete
        </button>
      </div>

      <p className="task-meta">
        Created: {new Date(task.created_at).toLocaleDateString()}
      </p>
    </div>
  );
}
