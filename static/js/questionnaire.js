(() => {
  "use strict";
  const form = document.querySelector("form.questionnaire");
  if (!form) return;
  const groups = [...form.querySelectorAll("fieldset")];
  if (!groups.length) return;
  const progress = document.createElement("div");
  progress.className = "questionnaire-progress";
  progress.setAttribute("role", "status");
  progress.innerHTML = '<span>پیشرفت پرسش‌نامه</span><progress max="100" value="0"></progress><small></small>';
  form.prepend(progress);
  const bar = progress.querySelector("progress"), label = progress.querySelector("small");
  const update = () => {
    const answered = groups.filter(group => group.querySelector('input[type="radio"]:checked, input[type="checkbox"]:checked, input:not([type="radio"]):not([type="checkbox"]):not([type="hidden"]):not(:placeholder-shown)')).length;
    const pct = Math.round(answered * 100 / groups.length);
    bar.value = pct; label.textContent = `${answered} از ${groups.length} مورد پاسخ داده شده · ${pct}٪`;
  };
  form.addEventListener("change", update); form.addEventListener("input", update); update();
  groups.forEach((group, index) => { group.dataset.questionNumber = String(index + 1); });
})();
