const body = document.body;
const sideBar = document.querySelector(".sideBar");
const withSub = document.querySelectorAll(".withSub .nav-link");
const sidebarOpen = document.querySelector(".sidebarOpen");
const logo = document.querySelector(".logo");
const darkLight = document.querySelector(".darkLight");
const notification = document.querySelector(".notification");
const notifications = document.querySelector(".notifications");

const resetNavStates = () => {
  withSub.forEach((menu) => {
    menu.classList.remove("openSubMenu");
  });
  notifications?.classList.remove("open");
};

const toggleSidebar = () => {
  if (!sideBar) return;
  sideBar.classList.toggle("close");
  resetNavStates();
};

if (sidebarOpen) {
  sidebarOpen.addEventListener("click", toggleSidebar);
}

if (logo && logo !== sidebarOpen) {
  logo.addEventListener("click", toggleSidebar);
}

if (darkLight) {
  darkLight.addEventListener("click", () => {
    body.classList.toggle("dark");
  });
}

withSub.forEach((menu) => {
  menu.addEventListener("click", () => {
    menu.classList.toggle("openSubMenu");
    sideBar?.classList.remove("close");
    notifications?.classList.remove("open");
  });
});

if (notification && notifications) {
  notification.addEventListener("click", () => {
    notifications.classList.toggle("open");
  });
}
