import { useCallback, useEffect, useState } from "react";

import { analyzeTask, createTask, getTasks, updateTask } from "./api";

const INITIAL_FORM = { title: "", description: "" };

const categoryLabels = {
  unclassified: "Sin clasificar",
  personal: "Personal",
  work: "Trabajo",
  urgent: "Urgente",
  other: "Otra",
};

function getErrorMessage(error) {
  const detail = error.response?.data?.detail;
  if (detail) return detail;

  const validation = error.response?.data;
  if (validation && typeof validation === "object") {
    const firstMessage = Object.values(validation).flat()[0];
    if (firstMessage) return firstMessage;
  }

  return "No fue posible completar la operación.";
}

export default function App() {
  const [tasks, setTasks] = useState([]);
  const [form, setForm] = useState(INITIAL_FORM);
  const [filter, setFilter] = useState("all");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [analyzingId, setAnalyzingId] = useState(null);
  const [error, setError] = useState("");

  const loadTasks = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      setTasks(await getTasks(filter));
    } catch (requestError) {
      setError(getErrorMessage(requestError));
    } finally {
      setLoading(false);
    }
  }, [filter]);

  useEffect(() => {
    loadTasks();
  }, [loadTasks]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setSaving(true);
    setError("");

    try {
      await createTask(form);
      setForm(INITIAL_FORM);
      await loadTasks();
    } catch (requestError) {
      setError(getErrorMessage(requestError));
    } finally {
      setSaving(false);
    }
  };

  const toggleStatus = async (task) => {
    const status = task.status === "pending" ? "completed" : "pending";
    setError("");

    try {
      await updateTask(task.id, { status });
      await loadTasks();
    } catch (requestError) {
      setError(getErrorMessage(requestError));
    }
  };

  const handleAnalyze = async (taskId) => {
    setAnalyzingId(taskId);
    setError("");

    try {
      await analyzeTask(taskId);
      await loadTasks();
    } catch (requestError) {
      setError(getErrorMessage(requestError));
    } finally {
      setAnalyzingId(null);
    }
  };

  return (
    <main className="app-shell">
      <header className="hero">
        <span className="eyebrow">Django · React · LangChain</span>
        <h1>TaskPilot <span>AI</span></h1>
        <p>Organiza tus tareas y conviértelas en pasos accionables con IA.</p>
      </header>

      <section className="workspace">
        <form className="task-form" onSubmit={handleSubmit}>
          <div className="section-heading">
            <div>
              <span className="section-number">01</span>
              <h2>Nueva tarea</h2>
            </div>
            <span className="status-dot">API conectada</span>
          </div>

          <label htmlFor="title">Título</label>
          <input
            id="title"
            value={form.title}
            onChange={(event) => setForm({ ...form, title: event.target.value })}
            placeholder="Ej. Preparar presentación"
            minLength={3}
            maxLength={150}
            required
          />

          <label htmlFor="description">Descripción</label>
          <textarea
            id="description"
            value={form.description}
            onChange={(event) =>
              setForm({ ...form, description: event.target.value })
            }
            placeholder="Describe el resultado que necesitas conseguir..."
            minLength={5}
            rows={5}
            required
          />

          <button className="primary-button" type="submit" disabled={saving}>
            {saving ? "Guardando..." : "Crear tarea"}
          </button>
        </form>

        <section className="task-panel">
          <div className="section-heading task-heading">
            <div>
              <span className="section-number">02</span>
              <h2>Tus tareas</h2>
            </div>
            <div className="filters" aria-label="Filtrar tareas">
              {[
                ["all", "Todas"],
                ["pending", "Pendientes"],
                ["completed", "Completadas"],
              ].map(([value, label]) => (
                <button
                  className={filter === value ? "active" : ""}
                  key={value}
                  onClick={() => setFilter(value)}
                  type="button"
                >
                  {label}
                </button>
              ))}
            </div>
          </div>

          {error && <div className="error-message" role="alert">{error}</div>}

          {loading ? (
            <p className="empty-state">Cargando tareas...</p>
          ) : tasks.length === 0 ? (
            <p className="empty-state">Todavía no hay tareas en esta vista.</p>
          ) : (
            <div className="task-list">
              {tasks.map((task) => (
                <article
                  className={`task-card ${task.status === "completed" ? "completed" : ""}`}
                  key={task.id}
                >
                  <div className="task-topline">
                    <span className={`category ${task.category}`}>
                      {categoryLabels[task.category]}
                    </span>
                    <button
                      className="status-button"
                      type="button"
                      onClick={() => toggleStatus(task)}
                    >
                      {task.status === "pending" ? "Marcar completada" : "Reabrir"}
                    </button>
                  </div>

                  <h3>{task.title}</h3>
                  <p>{task.description}</p>

                  {task.subtasks.length > 0 && (
                    <ol className="subtask-list">
                      {task.subtasks.map((subtask, index) => (
                        <li key={`${task.id}-${index}`}>{subtask}</li>
                      ))}
                    </ol>
                  )}

                  <button
                    className="ai-button"
                    type="button"
                    disabled={analyzingId === task.id}
                    onClick={() => handleAnalyze(task.id)}
                  >
                    <span>✦</span>
                    {analyzingId === task.id
                      ? "Analizando..."
                      : task.subtasks.length
                        ? "Volver a analizar"
                        : "Analizar con IA"}
                  </button>
                </article>
              ))}
            </div>
          )}
        </section>
      </section>
    </main>
  );
}

