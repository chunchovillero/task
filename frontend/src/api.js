import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api",
  timeout: 30000,
});

export const getTasks = async (status = "all") => {
  const params = status === "all" ? {} : { status };
  const response = await api.get("/tasks/", { params });
  return response.data;
};

export const createTask = async (task) => {
  const response = await api.post("/tasks/", task);
  return response.data;
};

export const updateTask = async (id, changes) => {
  const response = await api.patch(`/tasks/${id}/`, changes);
  return response.data;
};

export const analyzeTask = async (id) => {
  const response = await api.post(`/tasks/${id}/analyze/`);
  return response.data;
};

