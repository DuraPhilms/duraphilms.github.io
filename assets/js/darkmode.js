const setTheme = (theme) => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
}
const toggleDarkMode = () => {
    theme = localStorage.getItem("theme");
    if (theme === "light") {
        setTheme("dark");
    } else {
        setTheme("light");
    }
}

let theme = localStorage.getItem("theme");
if (theme === "light" || theme === "dark") {
    document.documentElement.setAttribute("data-theme", theme);
} else {
    // unknown theme
    document.documentElement.setAttribute("data-theme", "light");
}
