(function () {
  if (window.__wkChatWidgetLoaded) {
    return;
  }
  window.__wkChatWidgetLoaded = true;

  var supportEmail = "7InkCoAdmin@7ink.com.au";
  var title = "Chat with White Knight";
  var subtitle = "Ask us anything. We usually reply fast.";

  var style = document.createElement("style");
  style.textContent = ""
    + ".wk-chat-root{position:fixed;right:20px;bottom:20px;z-index:9999;font-family:Roboto,system-ui,-apple-system,Segoe UI,sans-serif}"
    + ".wk-chat-button{width:58px;height:58px;border:none;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;color:#fff;box-shadow:0 12px 30px rgba(124,58,237,.45),0 0 0 1px rgba(255,255,255,.18) inset;background:linear-gradient(135deg,#7c3aed,#8b5cf6 55%,#9333ea);transition:transform .2s ease,box-shadow .2s ease}"
    + ".wk-chat-button:hover{transform:translateY(-2px);box-shadow:0 16px 32px rgba(124,58,237,.55),0 0 0 1px rgba(255,255,255,.22) inset}"
    + ".wk-chat-icon{width:22px;height:22px;display:block}"
    + ".wk-chat-panel{position:absolute;right:0;bottom:72px;width:min(92vw,340px);border-radius:18px;overflow:hidden;background:#0b1020;border:1px solid rgba(255,255,255,.12);box-shadow:0 18px 50px rgba(4,8,20,.6);opacity:0;pointer-events:none;transform:translateY(8px) scale(.98);transform-origin:bottom right;transition:opacity .22s ease,transform .22s ease}"
    + ".wk-chat-root.open .wk-chat-panel{opacity:1;pointer-events:auto;transform:translateY(0) scale(1)}"
    + ".wk-chat-head{padding:14px 16px;background:linear-gradient(130deg,#141e38,#111827 60%,#1f1442);color:#fff}"
    + ".wk-chat-head h4{margin:0;font-size:16px;font-weight:700;line-height:1.25}"
    + ".wk-chat-head p{margin:6px 0 0;color:rgba(255,255,255,.8);font-size:13px;line-height:1.4}"
    + ".wk-chat-body{padding:14px 14px 12px;background:#0b1020}"
    + ".wk-chat-input,.wk-chat-textarea{width:100%;border:1px solid rgba(255,255,255,.16);background:#11182f;color:#fff;border-radius:10px;padding:10px 12px;font-size:14px;outline:none;transition:border-color .2s ease,box-shadow .2s ease}"
    + ".wk-chat-input::placeholder,.wk-chat-textarea::placeholder{color:rgba(255,255,255,.55)}"
    + ".wk-chat-input:focus,.wk-chat-textarea:focus{border-color:#8b5cf6;box-shadow:0 0 0 3px rgba(139,92,246,.2)}"
    + ".wk-chat-textarea{min-height:90px;resize:vertical;margin-top:10px}"
    + ".wk-chat-row{display:flex;gap:8px;margin-top:10px}"
    + ".wk-chat-send{flex:1;border:none;border-radius:11px;padding:10px 12px;font-size:14px;font-weight:700;color:#fff;cursor:pointer;background:linear-gradient(90deg,#7c3aed,#8b5cf6,#9333ea);transition:filter .2s ease,transform .2s ease}"
    + ".wk-chat-send:hover{filter:brightness(1.06);transform:translateY(-1px)}"
    + ".wk-chat-mail{display:inline-flex;align-items:center;justify-content:center;padding:10px 11px;border-radius:11px;border:1px solid rgba(255,255,255,.2);color:#fff;text-decoration:none;background:#121a33}"
    + ".wk-chat-note{margin-top:10px;font-size:12px;line-height:1.4;color:rgba(255,255,255,.65)}"
    + "@media (max-width: 576px){.wk-chat-root{right:14px;bottom:14px}.wk-chat-panel{bottom:68px}}";
  document.head.appendChild(style);

  var root = document.createElement("div");
  root.className = "wk-chat-root";

  var panel = document.createElement("div");
  panel.className = "wk-chat-panel";
  panel.innerHTML = ""
    + "<div class=\"wk-chat-head\">"
    + "<h4>" + title + "</h4>"
    + "<p>" + subtitle + "</p>"
    + "</div>"
    + "<div class=\"wk-chat-body\">"
    + "<input class=\"wk-chat-input\" id=\"wk-chat-name\" type=\"text\" placeholder=\"Your name\"/>"
    + "<textarea class=\"wk-chat-textarea\" id=\"wk-chat-message\" placeholder=\"Type your message...\"></textarea>"
    + "<div class=\"wk-chat-row\">"
    + "<button type=\"button\" class=\"wk-chat-send\" id=\"wk-chat-send\">Send</button>"
    + "<a class=\"wk-chat-mail\" id=\"wk-chat-mail\" title=\"Email us\" href=\"mailto:" + supportEmail + "\" aria-label=\"Email us\">✉</a>"
    + "</div>"
    + "<p class=\"wk-chat-note\">This opens your email app with your message pre-filled.</p>"
    + "</div>";

  var button = document.createElement("button");
  button.className = "wk-chat-button";
  button.setAttribute("aria-label", "Open chat");
  button.innerHTML = ""
    + "<svg class=\"wk-chat-icon\" viewBox=\"0 0 24 24\" fill=\"none\" aria-hidden=\"true\">"
    + "<path d=\"M7 10h10M7 14h7m6-2c0 4.418-3.582 8-8 8-1.173 0-2.287-.252-3.291-.705L4 20l.705-4.709A7.965 7.965 0 0 1 4 12c0-4.418 3.582-8 8-8s8 3.582 8 8Z\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/>"
    + "</svg>";

  root.appendChild(panel);
  root.appendChild(button);
  document.body.appendChild(root);

  button.addEventListener("click", function () {
    root.classList.toggle("open");
  });

  document.addEventListener("click", function (event) {
    if (!root.contains(event.target)) {
      root.classList.remove("open");
    }
  });

  var sendButton = panel.querySelector("#wk-chat-send");
  sendButton.addEventListener("click", function () {
    var name = panel.querySelector("#wk-chat-name").value.trim();
    var message = panel.querySelector("#wk-chat-message").value.trim();

    if (!message) {
      panel.querySelector("#wk-chat-message").focus();
      return;
    }

    var subject = encodeURIComponent("New Website Chat Message");
    var bodyLines = [];
    if (name) {
      bodyLines.push("Name: " + name);
    }
    bodyLines.push("Page: " + window.location.href);
    bodyLines.push("");
    bodyLines.push(message);

    var body = encodeURIComponent(bodyLines.join("\n"));
    window.location.href = "mailto:" + supportEmail + "?subject=" + subject + "&body=" + body;
  });
})();
