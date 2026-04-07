import { useState, useEffect } from "react";
import { PRIORITIES, STATUSES, STATUS_LABELS, PRIORITY_LABELS } from "../utils/constants";

const EMPTY_FORM = {
  title: "",
  description: "",
  priority: "medium",
  status: "todo",
  due_date: "",
};

export default function TaskForm({ initial, onSubmit, onCancel }) {
  const [form, setForm] = useState(EMPTY_FORM);
  const [errors, setErrors] = useState({});
  const isEdit = Boolean(initial);

  useEffect(() => {
    if (initial) {
      setForm({
        title: initial.title || "",
        description: initial.description || "",
        priority: initial.priority || "medium",
        status: initial.status || "todo",
        due_date: initial.due_date || "",
      });
    } else {
      setForm(EMPTY_FORM);
    }
  }, [initial]);

  function validate() {
    const errs = {};
    if (!form.title.trim()) errs.title = "Title is required.";
    if (form.due_date) {
      const today = new Date().toISOString().split("T")[0];
      if (form.due_date < today) errs.due_date = "Due date cannot be in the past.";
    }
    return errs;
  }

  function handleChange(e) {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
    setErrors((prev) => ({ ...prev, [name]: undefined }));
  }

  function handleSubmit(e) {
    e.preventDefault();
    const errs = validate();
    if (Object.keys(errs).length > 0) {
      setErrors(errs);
      return;
    }
    const payload = {
      title: form.title.trim(),
      description: form.description.trim() || null,
      priority: form.priority,
      due_date: form.due_date || null,
    };
    // Only include status on create
    if (!isEdit) payload.status = form.status;
    onSubmit(payload);
  }

  return (
    <form className="task-form" onSubmit={handleSubmit} noValidate>
      <h2>{isEdit ? "Edit Task" : "New Task"}</h2>

      <div className="form-group">
        <label htmlFor="title">Title *</label>
        <input
          id="title"
          name="title"
          type="text"
          value={form.title}
          onChange={handleChange}
          placeholder="What needs to be done?"
          maxLength={255}
        />
        {errors.title && <span className="field-error">{errors.title}</span>}
      </div>

      <div className="form-group">
        <label htmlFor="description">Description</label>
        <textarea
          id="description"
          name="description"
          value={form.description}
          onChange={handleChange}
          placeholder="Optional details..."
          rows={3}
        />
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="priority">Priority *</label>
          <select id="priority" name="priority" value={form.priority} onChange={handleChange}>
            {PRIORITIES.map((p) => (
              <option key={p} value={p}>
                {PRIORITY_LABELS[p]}
              </option>
            ))}
          </select>
        </div>

        {!isEdit && (
          <div className="form-group">
            <label htmlFor="status">Status *</label>
            <select id="status" name="status" value={form.status} onChange={handleChange}>
              {STATUSES.filter((s) => s !== "archived").map((s) => (
                <option key={s} value={s}>
                  {STATUS_LABELS[s]}
                </option>
              ))}
            </select>
          </div>
        )}

        <div className="form-group">
          <label htmlFor="due_date">Due Date</label>
          <input
            id="due_date"
            name="due_date"
            type="date"
            value={form.due_date}
            onChange={handleChange}
          />
          {errors.due_date && <span className="field-error">{errors.due_date}</span>}
        </div>
      </div>

      <div className="form-actions">
        <button type="submit" className="btn btn-primary">
          {isEdit ? "Save Changes" : "Create Task"}
        </button>
        <button type="button" className="btn btn-secondary" onClick={onCancel}>
          Cancel
        </button>
      </div>
    </form>
  );
}
