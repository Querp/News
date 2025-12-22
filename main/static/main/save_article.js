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

    const iconE = e.target.querySelector('.icon')

    if (result.status === "saved") {
        // iconE.textContent = "Saved ✓";
        iconE.textContent = "check_box";
        e.target.disabled = true;
    } else {
        iconE.textContent = "save";
        // iconE.textContent = "Already saved";
        e.target.disabled = true;
    }
});

function getCSRFToken() {
    return document.querySelector("[name=csrfmiddlewaretoken]").value;
}