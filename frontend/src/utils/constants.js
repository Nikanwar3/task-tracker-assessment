export const PRIORITIES = ["low", "medium", "high"];

export const STATUSES = ["todo", "in_progress", "done", "archived"];

export const STATUS_LABELS = {
  todo: "To Do",
  in_progress: "In Progress",
  done: "Done",
  archived: "Archived",
};

export const PRIORITY_LABELS = {
  low: "Low",
  medium: "Medium",
  high: "High",
};

// Which next statuses a user can move a task to from the current status
export const ALLOWED_TRANSITIONS = {
  todo: ["in_progress", "archived"],
  in_progress: ["todo", "done", "archived"],
  done: ["archived"],
  archived: ["todo"],
};
