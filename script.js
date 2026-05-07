const domainNameElement = document.getElementById("domain-name");

if (domainNameElement) {
  const preferredDomain = "shellsentry.com";
  domainNameElement.textContent = preferredDomain;
}

const revealElements = document.querySelectorAll(".reveal");

if ("IntersectionObserver" in window && revealElements.length > 0) {
  const observer = new IntersectionObserver(
    (entries, observerRef) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observerRef.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15 }
  );

  revealElements.forEach((element) => observer.observe(element));
} else {
  revealElements.forEach((element) => element.classList.add("is-visible"));
}

const stepperItems = document.querySelectorAll(".stepper li");
if ("IntersectionObserver" in window && stepperItems.length > 0) {
  const stepperObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-active");
        }
      });
    },
    { threshold: 0.35 }
  );

  stepperItems.forEach((item) => stepperObserver.observe(item));
}

const backTopButton = document.querySelector(".back-top");
if (backTopButton) {
  backTopButton.addEventListener("click", (event) => {
    event.preventDefault();
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
}
