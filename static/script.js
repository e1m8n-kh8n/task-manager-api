
const API_URL = "/tasks";

const taskInput = document.getElementById("taskInput");
const addButton = document.getElementById("addButton");
const taskList = document.getElementById("taskList");

// Load saved tasks from the API
async function loadTasks() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) throw new Error("Could not load tasks");

        const tasks = await response.json();
        taskList.innerHTML = "";

        tasks.forEach(task => {
            const li = document.createElement("li");
            if (task.completed) li.classList.add("completed");

            const checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.checked = task.completed;

            checkbox.addEventListener("change", async () => {
                await updateTask(task, checkbox.checked);
            });

            const title = document.createElement("span");
            title.textContent = task.title;

            const deleteButton = document.createElement("button");
            deleteButton.textContent = "Delete";
            deleteButton.className = "delete-btn";

            deleteButton.addEventListener("click", async () => {
                await deleteTask(task.id);
            });

            li.append(checkbox, title, deleteButton);
            taskList.appendChild(li);
        });
    } catch (error) {
        alert("Could not load tasks: " + error.message);
    }
}

// Create a task
async function addTask() {
    const title = taskInput.value.trim();
    if (!title) return;

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({title, completed: false})
        });

        if (!response.ok) throw new Error("Could not create task");

        taskInput.value = "";
        await loadTasks();
    } catch (error) {
        alert(error.message);
    }
}

// Update completion status
async function updateTask(task, completed) {
    try {
        const response = await fetch(`${API_URL}/${task.id}`, {
            method: "PUT",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({title: task.title, completed})
        });

        if (!response.ok) throw new Error("Could not update task");
        await loadTasks();
    } catch (error) {
        alert(error.message);
        await loadTasks();
    }
}

// Delete a task
async function deleteTask(id) {
    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: "DELETE"
        });

        if (!response.ok) throw new Error("Could not delete task");
        await loadTasks();
    } catch (error) {
        alert(error.message);
    }
}

addButton.addEventListener("click", addTask);

taskInput.addEventListener("keydown", event => {
    if (event.key === "Enter") addTask();
});

loadTasks();
