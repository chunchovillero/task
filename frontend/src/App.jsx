import { useEffect, useState } from "react";

import { analyzeTask, createTask, getTasks } from "./api/tasks.js";

const INITIAL_FORM = { title: "", description: "" };

export default function App() {
  const [form, setForm] = useState(INITIAL_FORM);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [analyzingId, setAnalyzingId] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;

    getTasks()
      .then((storedTasks) => {
        if (active) setTasks(storedTasks);
      })
      .catch((requestError) => {
        if (active) setError(requestError.message);
      })
      .finally(() => {
        if (active) setLoading(false);
      });

    return () => {
      active = false;
    };
  }, []);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((currentForm) => ({ ...currentForm, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setSaving(true);
    setError("");

    try {
      const newTask = await createTask({
        title: form.title.trim(),
        description: form.description.trim(),
      });
      setTasks((currentTasks) => [newTask, ...currentTasks]);
      setForm(INITIAL_FORM);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setSaving(false);
    }
  };

  const handleAnalyze = async (taskId) => {
    setAnalyzingId(taskId);
    setError("");

    try {
      const analyzedTask = await analyzeTask(taskId);
      setTasks((currentTasks) =>
        currentTasks.map((task) => task.id === taskId ? analyzedTask : task),
      );
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setAnalyzingId(null);
    }
  };

  return (
    <main className="page-shell">
      <header className="hero">
        <span className="eyebrow">Organización personal</span>
        <h1>Mis tareas</h1>
        <p>Crea y organiza las actividades que necesitas completar.</p>
      </header>

      <div className="workspace">
        <section className="panel form-panel">
          <div className="section-heading">
            <div><span className="step-number">01</span><h2>Nueva tarea</h2></div>
            <p>Completa los datos principales.</p>
          </div>

          <form onSubmit={handleSubmit}>
            <div className="field">
              <label htmlFor="title">Título</label>
              <input id="title" name="title" type="text" value={form.title}
                onChange={handleChange} placeholder="Ej. Preparar presentación"
                minLength={3} maxLength={150} required />
              <span className="field-help">Entre 3 y 150 caracteres</span>
            </div>

            <div className="field">
              <label htmlFor="description">Descripción</label>
              <textarea id="description" name="description" value={form.description}
                onChange={handleChange} placeholder="Describe qué necesitas conseguir..."
                minLength={5} rows={6} required />
              <span className="field-help">Agrega el contexto necesario</span>
            </div>

            {error && <p className="error-message" role="alert">{error}</p>}

            <button className="primary-button" type="submit" disabled={saving}>
              {saving ? "Guardando..." : "Crear tarea"}
            </button>
          </form>
        </section>

        <section className="panel tasks-panel">
          <div className="section-heading tasks-heading">
            <div><span className="step-number">02</span><h2>Tareas creadas</h2></div>
            <span className="task-count">{tasks.length} tareas</span>
          </div>

          {loading ? (
            <p className="loading-state">Cargando tareas...</p>
          ) : tasks.length === 0 ? (
            <div className="empty-state">
              <span aria-hidden="true">✓</span>
              <h3>Todo está al día</h3>
              <p>Las tareas que agregues aparecerán en este espacio.</p>
            </div>
          ) : (
            <div className="task-list">
              {tasks.map((task) => (
                <article className="task-card" key={task.id}>
                  <div className="task-card-header">
                    <span className="status-badge">{task.status}</span>
                    <span className="task-id">#{String(task.id).padStart(4, "0")}</span>
                  </div>
                  <h3>{task.title}</h3>
                  <p>{task.description}</p>
                  <div className="task-actions">
                    <span className={`category-badge ${task.category}`}>
                      {task.category === "urgente"
                        ? "Urgente"
                        : task.category === "no_urgente"
                          ? "No urgente"
                          : "Sin clasificar"}
                    </span>
                    <button
                      className="ai-button"
                      type="button"
                      disabled={analyzingId === task.id}
                      onClick={() => handleAnalyze(task.id)}
                    >
                      {analyzingId === task.id ? "Analizando..." : "Analizar urgencia"}
                    </button>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
