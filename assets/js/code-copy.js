document.addEventListener("DOMContentLoaded", () => {
  const blocks = document.querySelectorAll("pre > code");
  blocks.forEach((code) => {
    const pre = code.parentElement;
    if (!pre || pre.querySelector(".code-copy-button")) return;

    const button = document.createElement("button");
    button.type = "button";
    button.className = "code-copy-button";
    button.textContent = "Copy";

    button.addEventListener("click", async () => {
      const text = code.innerText;
      try {
        await navigator.clipboard.writeText(text);
        button.textContent = "Copied";
        button.classList.add("copied");
        setTimeout(() => {
          button.textContent = "Copy";
          button.classList.remove("copied");
        }, 1200);
      } catch (_err) {
        button.textContent = "Press Ctrl+C";
        setTimeout(() => {
          button.textContent = "Copy";
        }, 1200);
      }
    });

    pre.appendChild(button);
  });
});
