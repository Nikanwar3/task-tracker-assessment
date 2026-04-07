import { useState, useEffect, useCallback } from "react";
import FilterBar from "../components/FilterBar";
import TaskForm from "../components/TaskForm";
import TaskList from "../components/TaskList";
import {
  fetchTasks,
  createTask,
  updateTask,
  updateTaskStatus,
  deleteTask,
} from "../api/taskApi";

export default function Dashboard() {
  const [tasks, setTasks] = useState([]);
  const [filters, setFilters] = useState({ status: "", priority: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState(null);

  const loadTasks = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchTasks(filters);
      setTasks(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    loadTasks();
  }, [loadTasks]);

  async function handleCreate(payload) {
    setError(null);
    try {
      await createTask(payload);
      setShowForm(false);
      loadTasks();
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleUpdate(payload) {
    setError(null);
    try {
      await updateTask(editingTask.id, payload);
      setEditingTask(null);
      loadTasks();
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleStatusChange(id, newStatus) {
    setError(null);
    try {
      await updateTaskStatus(id, newStatus);
      loadTasks();
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleDelete(id) {
    if (!window.confirm("Delete this task?")) return;
    setError(null);
    try {
      await deleteTask(id);
      loadTasks();
    } catch (err) {
      setError(err.message);
    }
  }

  function openCreateForm() {
    setEditingTask(null);
    setShowForm(true);
  }

  function openEditForm(task) {
    setEditingTask(task);
    setShowForm(true);
  }

  function closeForm() {
    setShowForm(false);
    setEditingTask(null);
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Task Tracker</h1>
        <button className="btn btn-primary" onClick={openCreateForm}>
          + New Task
        </button>
      </header>

      {error && (
        <div className="alert alert-error" role="alert">
          {error}
          <button className="alert-close" onClick={() => setError(null)}>
            ×
          </button>
        </div>
      )}

      {showForm && (
        <div className="modal-overlay" onClick={closeForm}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <TaskForm
              initial={editingTask}
              onSubmit={editingTask ? handleUpdate : handleCreate}
              onCancel={closeForm}
            />
          </div>
        </div>
      )}

      <FilterBar filters={filters} onChange={setFilters} />

      <div className="task-count">
        {loading ? "" : `${tasks.length} task${tasks.length !== 1 ? "s" : ""}`}
      </div>

      <TaskList
        tasks={tasks}
        loading={loading}
        onEdit={openEditForm}
        onStatusChange={handleStatusChange}
        onDelete={handleDelete}
      />
    </div>
  );
}
