(function () {
  if (window.__wkAuthGateLoaded) {
    return;
  }
  window.__wkAuthGateLoaded = true;

  var USERS_KEY = "wk_users_v1";
  var SESSION_KEY = "wk_current_user_v1";

  function readUsers() {
    try {
      return JSON.parse(localStorage.getItem(USERS_KEY) || "[]");
    } catch (e) {
      return [];
    }
  }

  function writeUsers(users) {
    localStorage.setItem(USERS_KEY, JSON.stringify(users));
  }

  function getSessionUser() {
    return localStorage.getItem(SESSION_KEY) || "";
  }

  function setSessionUser(email) {
    localStorage.setItem(SESSION_KEY, email);
  }

  function clearSessionUser() {
    localStorage.removeItem(SESSION_KEY);
  }

  function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  function injectStyle() {
    var style = document.createElement("style");
    style.textContent = ""
      + ".wk-auth-overlay{position:fixed;inset:0;background:rgba(3,6,16,.64);backdrop-filter:blur(3px);z-index:10000;display:none}"
      + ".wk-auth-overlay.show{display:block}"
      + ".wk-auth-modal{position:fixed;left:50%;top:50%;transform:translate(-50%,-50%);width:min(94vw,420px);background:#0b1120;border:1px solid rgba(255,255,255,.12);border-radius:16px;box-shadow:0 20px 45px rgba(0,0,0,.5);z-index:10001;display:none;color:#fff;font-family:Roboto,system-ui,-apple-system,Segoe UI,sans-serif}"
      + ".wk-auth-modal.show{display:block}"
      + ".wk-auth-head{padding:15px 16px 12px;border-bottom:1px solid rgba(255,255,255,.08);display:flex;justify-content:space-between;align-items:center}"
      + ".wk-auth-title{font-size:18px;font-weight:700;margin:0}"
      + ".wk-auth-close{background:none;border:none;color:#d1d5db;font-size:22px;line-height:1;cursor:pointer;padding:2px 6px}"
      + ".wk-auth-tabs{display:flex;gap:8px;padding:12px 16px 0}"
      + ".wk-auth-tab{flex:1;border:1px solid rgba(255,255,255,.16);background:#11182f;color:#d1d5db;border-radius:10px;padding:9px 10px;cursor:pointer;font-weight:600}"
      + ".wk-auth-tab.active{background:linear-gradient(90deg,#7c3aed,#8b5cf6,#9333ea);border-color:transparent;color:#fff}"
      + ".wk-auth-body{padding:12px 16px 16px}"
      + ".wk-auth-field{width:100%;border:1px solid rgba(255,255,255,.16);background:#11182f;color:#fff;border-radius:10px;padding:10px 12px;font-size:14px;outline:none;margin-top:10px}"
      + ".wk-auth-field:focus{border-color:#8b5cf6;box-shadow:0 0 0 3px rgba(139,92,246,.2)}"
      + ".wk-auth-submit{margin-top:12px;width:100%;border:none;border-radius:11px;padding:10px 12px;font-size:14px;font-weight:700;color:#fff;cursor:pointer;background:linear-gradient(90deg,#7c3aed,#8b5cf6,#9333ea)}"
      + ".wk-auth-note{font-size:12px;color:rgba(255,255,255,.68);margin-top:10px;line-height:1.45}"
      + ".wk-auth-msg{min-height:20px;margin-top:10px;font-size:13px}"
      + ".wk-auth-msg.error{color:#fca5a5}"
      + ".wk-auth-msg.ok{color:#86efac}"
      + ".wk-auth-user{position:fixed;right:20px;bottom:90px;z-index:9998;background:#0e1630;border:1px solid rgba(255,255,255,.15);color:#fff;padding:7px 12px;border-radius:999px;font-size:12px;display:none;gap:8px;align-items:center}"
      + ".wk-auth-user.show{display:flex}"
      + ".wk-auth-logout{border:none;background:none;color:#a78bfa;cursor:pointer;font-weight:700;font-size:12px;padding:0}"
      + ".wk-auth-lock{display:inline-block;margin-right:6px;color:#a78bfa;font-weight:700}";
    document.head.appendChild(style);
  }

  function buildModal() {
    var overlay = document.createElement("div");
    overlay.className = "wk-auth-overlay";

    var modal = document.createElement("div");
    modal.className = "wk-auth-modal";
    modal.innerHTML = ""
      + "<div class=\"wk-auth-head\">"
      + "<h3 class=\"wk-auth-title\">Account Access</h3>"
      + "<button class=\"wk-auth-close\" aria-label=\"Close\">&times;</button>"
      + "</div>"
      + "<div class=\"wk-auth-tabs\">"
      + "<button class=\"wk-auth-tab active\" data-tab=\"login\">Log In</button>"
      + "<button class=\"wk-auth-tab\" data-tab=\"signup\">Sign Up</button>"
      + "</div>"
      + "<div class=\"wk-auth-body\">"
      + "<input class=\"wk-auth-field\" id=\"wk-auth-email\" type=\"email\" placeholder=\"Email\"/>"
      + "<input class=\"wk-auth-field\" id=\"wk-auth-password\" type=\"password\" placeholder=\"Password\"/>"
      + "<button class=\"wk-auth-submit\" id=\"wk-auth-submit\">Log In</button>"
      + "<div class=\"wk-auth-msg\" id=\"wk-auth-msg\"></div>"
      + "<p class=\"wk-auth-note\">Create an account or log in to unlock protected downloads.</p>"
      + "</div>";

    var userChip = document.createElement("div");
    userChip.className = "wk-auth-user";
    userChip.innerHTML = "<span id=\"wk-auth-user-label\"></span><button class=\"wk-auth-logout\" id=\"wk-auth-logout\">Log out</button>";

    document.body.appendChild(overlay);
    document.body.appendChild(modal);
    document.body.appendChild(userChip);

    return { overlay: overlay, modal: modal, userChip: userChip };
  }

  function init() {
    injectStyle();
    var ui = buildModal();
    var pendingUrl = "";
    var currentTab = "login";

    var tabs = ui.modal.querySelectorAll(".wk-auth-tab");
    var closeBtn = ui.modal.querySelector(".wk-auth-close");
    var submitBtn = ui.modal.querySelector("#wk-auth-submit");
    var msg = ui.modal.querySelector("#wk-auth-msg");
    var emailInput = ui.modal.querySelector("#wk-auth-email");
    var passwordInput = ui.modal.querySelector("#wk-auth-password");
    var userLabel = ui.userChip.querySelector("#wk-auth-user-label");
    var logoutBtn = ui.userChip.querySelector("#wk-auth-logout");

    function setMsg(text, isError) {
      msg.textContent = text || "";
      msg.className = "wk-auth-msg " + (text ? (isError ? "error" : "ok") : "");
    }

    function setTab(nextTab) {
      currentTab = nextTab;
      tabs.forEach(function (tab) {
        tab.classList.toggle("active", tab.getAttribute("data-tab") === nextTab);
      });
      submitBtn.textContent = nextTab === "signup" ? "Create Account" : "Log In";
      setMsg("", false);
    }

    function openModal(downloadUrl) {
      pendingUrl = downloadUrl || "";
      ui.overlay.classList.add("show");
      ui.modal.classList.add("show");
      emailInput.focus();
    }

    function closeModal() {
      ui.overlay.classList.remove("show");
      ui.modal.classList.remove("show");
    }

    function refreshUserChip() {
      var currentUser = getSessionUser();
      if (currentUser) {
        userLabel.textContent = currentUser;
        ui.userChip.classList.add("show");
      } else {
        ui.userChip.classList.remove("show");
      }
    }

    tabs.forEach(function (tab) {
      tab.addEventListener("click", function () {
        setTab(tab.getAttribute("data-tab"));
      });
    });

    closeBtn.addEventListener("click", closeModal);
    ui.overlay.addEventListener("click", closeModal);

    submitBtn.addEventListener("click", function () {
      var email = emailInput.value.trim().toLowerCase();
      var password = passwordInput.value;

      if (!isValidEmail(email)) {
        setMsg("Enter a valid email address.", true);
        return;
      }
      if (password.length < 6) {
        setMsg("Password must be at least 6 characters.", true);
        return;
      }

      var users = readUsers();
      var existing = users.find(function (user) { return user.email === email; });

      if (currentTab === "signup") {
        if (existing) {
          setMsg("Account already exists. Please log in.", true);
          setTab("login");
          return;
        }
        users.push({ email: email, password: password, createdAt: Date.now() });
        writeUsers(users);
        setSessionUser(email);
        setMsg("Account created. Download unlocked.", false);
      } else {
        if (!existing || existing.password !== password) {
          setMsg("Email or password is incorrect.", true);
          return;
        }
        setSessionUser(email);
        setMsg("Login successful.", false);
      }

      refreshUserChip();

      if (pendingUrl) {
        var url = pendingUrl;
        pendingUrl = "";
        setTimeout(function () {
          closeModal();
          window.location.href = url;
        }, 200);
      } else {
        setTimeout(closeModal, 250);
      }
    });

    logoutBtn.addEventListener("click", function () {
      clearSessionUser();
      refreshUserChip();
    });

    document.querySelectorAll("[data-protected-download]").forEach(function (el) {
      var targetUrl = el.getAttribute("href") || el.getAttribute("data-download-url") || "";
      if (el.tagName === "A" && !el.hasAttribute("download")) {
        el.setAttribute("download", "");
      }

      var label = el.textContent.trim();
      if (label && !/^\s*\uD83D\uDD12/.test(label)) {
        el.innerHTML = "<span class=\"wk-auth-lock\">\uD83D\uDD12</span>" + el.innerHTML;
      }

      el.addEventListener("click", function (event) {
        if (getSessionUser()) {
          return;
        }
        event.preventDefault();
        openModal(targetUrl);
      });
    });

    document.querySelectorAll(".wk-open-auth").forEach(function (el) {
      el.addEventListener("click", function (event) {
        event.preventDefault();
        openModal("");
      });
    });

    refreshUserChip();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
