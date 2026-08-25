const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

const mapTask = (task) => ({
  id: task.id,
  title: task.titulo,
  description: task.descripcion,
  status: task.estado,
  category: task.categoria,
  createdAt: task.created_at,
});

const request = async (path, options = {}) => {
  const response = await fetch(`${API_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    const firstError = Object.values(body).flat()[0];
    throw new Error(firstError || "No fue posible completar la operación.");
  }

  return response.json();
};

export const getTasks = async () => {
  const tasks = await request("/tasks/");
  return tasks.map(mapTask);
};

export const createTask = async ({ title, description }) => {
  const task = await request("/tasks/", {
    method: "POST",
    body: JSON.stringify({
      titulo: title,
      descripcion: description,
    }),
  });

  return mapTask(task);
};

export const analyzeTask = async (id) => {
  const task = await request(`/tasks/${id}/analyze/`, { method: "POST" });
  return mapTask(task);
};
