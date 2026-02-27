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

darkLight.addEventListener("click", () => {
  body.classList.toggle("dark");
  if (darkLight.classList.contains("fa-moon-o")) {
    darkLight.classList.replace("fa-moon-o", "fa-sun-o");
  } else {
    darkLight.classList.replace("fa-sun-o", "fa-moon-o");
  }
});

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
