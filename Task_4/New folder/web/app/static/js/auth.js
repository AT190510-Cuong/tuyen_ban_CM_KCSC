document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("auth-form");

    form.addEventListener("submit", function (event) {
        const authType = document.querySelector('input[name="authType"]:checked').value;
        if (authType === "register") {
            form.action = "/register";
        } else {
            form.action = "/login";
        }
    });

    if (window.location.search.includes("error")) {
        const errorParams = new URLSearchParams(window.location.search);
        const errorMessage = errorParams.get("error");
        if (errorMessage) {
            const errorElement = document.createElement("p");
            errorElement.className = "error-message";
            errorElement.textContent = decodeURIComponent(errorMessage);
            form.appendChild(errorElement);
        }
    }
});
