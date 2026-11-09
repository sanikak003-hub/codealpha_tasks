// Small client-side enhancement: dismiss status messages after a short delay.
document.addEventListener("DOMContentLoaded", () => {
    const messages = document.querySelectorAll(".message");
    messages.forEach((message) => {
        window.setTimeout(() => {
            message.style.transition = "opacity 300ms ease";
            message.style.opacity = "0";
            window.setTimeout(() => message.remove(), 350);
        }, 4500);
    });
});
