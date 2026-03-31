// assets/tabs.js

document.addEventListener("DOMContentLoaded", () => {
    console.log("tabs.js: DOMContentLoaded, wiring tabs...");

    const tabs = document.querySelectorAll(".sheet-tab");
    const panels = document.querySelectorAll(".tab-panel");

    console.log("tabs.js: found tabs =", tabs.length, "panels =", panels.length);

    tabs.forEach(tab => {
        tab.addEventListener("click", () => {
            console.log("tabs.js: clicked tab", tab.dataset.tab);

            // Remove active from all tabs
            tabs.forEach(t => t.classList.remove("active"));
            tab.classList.add("active");

            // Hide all panels
            panels.forEach(p => p.classList.remove("active"));

            // Show the correct panel
            const target = tab.dataset.tab;
            const panel = document.getElementById(`tab-${target}`);
            console.log("tabs.js: target panel id =", `tab-${target}`, "found =", !!panel);
            if (panel) panel.classList.add("active");
        });
    });
});