document.addEventListener("click", async e => {
    if (!e.target.matches(".save-button")) return;
    const articleId = e.target.id.slice(12);
    const scriptE = document.querySelector(`#article-data-${articleId} script`);
    const data = JSON.parse(scriptE.textContent);

 // Send to Django
    const response = await fetch("/save/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify(data),
    });

    const result = await response.json();

    if (result.status === "saved") {
        e.target.textContent = "Saved ✓";
        e.target.disabled = true;
    } else {
        e.target.textContent = "Already saved";
        e.target.disabled = true;
    }
});

function getCSRFToken() {
    return document.querySelector("[name=csrfmiddlewaretoken]").value;
}