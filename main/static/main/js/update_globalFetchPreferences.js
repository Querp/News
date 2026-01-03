const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const settingSelectorsE = document.getElementById('setting-selectors');
settingSelectorsE.addEventListener('change', clickSelector);

function clickSelector(e) {
    const input = e.target.closest('input');
    if (!input || !settingSelectorsE.contains(input)) return;

    const type = input.dataset.type;
    const value = input.dataset.value;
    if (!type || !value) return;

    const isValueToBeAdded = input.checked;

    // console.log(type, value, isValueToBeAdded);
    updateDatabase(type, value, isValueToBeAdded );
};


function updateDatabase(type, value, isValueToBeAdded) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch("/update-preferences/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        },
        body: JSON.stringify({
            type: type,
            value: value,
            add: isValueToBeAdded
        }),
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            console.log(value, isValueToBeAdded ? "added" : "removed");
        } else {
            console.error("Failed to update:", data.error);
        }
    })
    .catch(err => console.error("Error updating preferences:", err));
}
