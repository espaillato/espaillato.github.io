/* Field Notes — progressive enhancements. Nothing here is required to read a post. */
(function () {
  "use strict";

  function onReady(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  /* ---- copy button on fenced code blocks ---- */
  function addCopyButtons() {
    document.querySelectorAll(".post-body pre > code").forEach(function (code) {
      var pre = code.parentElement;
      if (!pre || pre.querySelector(".code-copy-button")) return;

      var button = document.createElement("button");
      button.type = "button";
      button.className = "code-copy-button";
      button.textContent = "Copy";
      button.setAttribute("aria-label", "Copy code to clipboard");

      button.addEventListener("click", function () {
        var text = code.innerText;
        var done = function (ok) {
          button.textContent = ok ? "Copied" : "Ctrl+C";
          button.classList.toggle("copied", ok);
          setTimeout(function () {
            button.textContent = "Copy";
            button.classList.remove("copied");
          }, 1400);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(function () { done(true); }, function () { done(false); });
        } else {
          done(false);
        }
      });

      pre.appendChild(button);
    });
  }

  /* ---- turn `> [!human-question]` blockquotes into labelled callouts ---- */
  function decorateCallouts() {
    var RE = /^\s*\[!([a-z][a-z-]*)\]\s*(?:<br\s*\/?>\s*)?/i;
    document.querySelectorAll(".post-body blockquote").forEach(function (bq) {
      var first = bq.firstElementChild;
      if (!first || first.tagName !== "P") return;
      var match = first.innerHTML.match(RE);
      if (!match) return;

      var token = match[1].toLowerCase();          // e.g. "human-question"
      first.innerHTML = first.innerHTML.slice(match[0].length);

      var kind = token.split("-").pop();           // question | comment | answer | ...
      bq.classList.add("callout");
      bq.classList.add(
        kind === "comment" ? "is-comment" :
        kind === "answer"  ? "is-answer"  : "is-question"
      );

      var label = document.createElement("span");
      label.className = "callout-label";
      label.textContent = token.replace(/-/g, " ").replace(/\b\w/g, function (c) { return c.toUpperCase(); });
      bq.insertBefore(label, first);
    });
  }

  /* ---- let wide tables scroll without pushing the page sideways ---- */
  function wrapTables() {
    document.querySelectorAll(".post-body table").forEach(function (table) {
      var parent = table.parentElement;
      if (parent && parent.classList.contains("table-wrap")) return;
      var wrap = document.createElement("div");
      wrap.className = "table-wrap";
      table.parentNode.insertBefore(wrap, table);
      wrap.appendChild(table);
    });
  }

  onReady(function () {
    addCopyButtons();
    decorateCallouts();
    wrapTables();
  });
})();
