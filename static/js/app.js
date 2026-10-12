(() => {
  "use strict";
  const csrf = () => {
    const cookie = document.cookie.split(";").map(x => x.trim()).find(x => x.startsWith("csrftoken="));
    const hidden = document.querySelector("input[name=csrfmiddlewaretoken]");
    return cookie ? decodeURIComponent(cookie.slice("csrftoken=".length)) : hidden?.value || "";
  };
  document.querySelectorAll(".feedback-check[data-url]").forEach((control) => {
    control.addEventListener("change", async () => {
      const status = control.closest(".plan-item")?.querySelector(".feedback-status");
      control.disabled = true;
      if (status) status.textContent = "در حال ثبت…";
      try {
        const response = await fetch(control.dataset.url, {
          method: "POST", credentials: "same-origin",
          headers: {"Content-Type": "application/json", "X-CSRFToken": csrf(), "X-Requested-With": "XMLHttpRequest"},
          body: JSON.stringify({completed: control.checked, completion_percent: control.checked ? 100 : 0})
        });
        const data = await response.json();
        if (!response.ok || !data.ok) throw new Error(data.error || "ثبت بازخورد ناموفق بود.");
        if (status) status.textContent = data.completed ? "انجام‌شده" : "در انتظار";
      } catch (error) {
        control.checked = !control.checked;
        if (status) status.textContent = error.message || "خطا در اتصال";
      } finally { control.disabled = false; }
    });
  });
})();
