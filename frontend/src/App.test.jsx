import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it, vi } from "vitest";

import App from "./App";
import * as api from "./api";

vi.mock("./api");

describe("App", () => {
  beforeEach(() => {
    vi.resetAllMocks();
    api.getTasks.mockResolvedValue([]);
    api.createTask.mockResolvedValue({ id: 1 });
  });

  it("creates a task from the form", async () => {
    const user = userEvent.setup();
    render(<App />);

    await waitFor(() => expect(api.getTasks).toHaveBeenCalled());
    await user.type(screen.getByLabelText("Título"), "Preparar entrevista");
    await user.type(
      screen.getByLabelText("Descripción"),
      "Repasar Django y Docker.",
    );
    await user.click(screen.getByRole("button", { name: "Crear tarea" }));

    await waitFor(() =>
      expect(api.createTask).toHaveBeenCalledWith({
        title: "Preparar entrevista",
        description: "Repasar Django y Docker.",
      }),
    );
  });
});

