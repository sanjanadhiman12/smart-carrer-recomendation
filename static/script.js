/* =========================================================
   Smart Career Recommendation System - script.js
   Beginner-friendly vanilla JavaScript (no frameworks)
   ========================================================= */

document.addEventListener("DOMContentLoaded", function () {
  /* ---------- Navbar scroll shadow ---------- */
  const navbar = document.querySelector(".navbar");
  if (navbar) {
    window.addEventListener("scroll", function () {
      if (window.scrollY > 20) {
        navbar.classList.add("scrolled");
      } else {
        navbar.classList.remove("scrolled");
      }
    });
  }

  /* ---------- Mobile nav toggle ---------- */
  const navToggle = document.querySelector(".nav-toggle");
  const navLinks = document.querySelector(".nav-links");

  if (navToggle && navLinks) {
    navToggle.addEventListener("click", function () {
      navLinks.classList.toggle("open");
    });

    // Close the mobile menu whenever a link is clicked
    navLinks.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        navLinks.classList.remove("open");
      });
    });
  }

  /* ---------- Live value display for 1-10 skill sliders ---------- */
  const rangeInputs = document.querySelectorAll('input[type="range"]');
  rangeInputs.forEach(function (input) {
    const output = document.getElementById(input.id + "-value");
    if (!output) return;

    // Set initial value on page load
    output.textContent = input.value;

    input.addEventListener("input", function () {
      output.textContent = input.value;
    });
  });

  /* ---------- Simple client-side form validation feedback ---------- */
  const predictForm = document.getElementById("career-form");
  if (predictForm) {
    predictForm.addEventListener("submit", function (e) {
      const requiredFields = predictForm.querySelectorAll("[required]");
      let isValid = true;

      requiredFields.forEach(function (field) {
        if (!field.value) {
          isValid = false;
          field.style.borderColor = "#ef4444";
        } else {
          field.style.borderColor = "";
        }
      });

      if (!isValid) {
        e.preventDefault();
        alert("Please fill in all required fields before submitting.");
      }
    });
  }

  /* ---------- Animate progress bars on the result page ---------- */
  const progressBars = document.querySelectorAll(".progress-fill");
  if (progressBars.length > 0) {
    progressBars.forEach(function (bar) {
      const targetWidth = bar.getAttribute("data-width") || "0%";
      // Start at 0 then animate to the target width for a nice effect
      bar.style.width = "0%";
      setTimeout(function () {
        bar.style.transition = "width 1s ease";
        bar.style.width = targetWidth;
      }, 150);
    });
  }

  /* ---------- Scroll-reveal animation for cards/sections ---------- */
  const revealTargets = document.querySelectorAll(
    ".feature-card, .result-card, .about-visual, .form-card"
  );

  if ("IntersectionObserver" in window && revealTargets.length > 0) {
    const observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.style.opacity = "1";
            entry.target.style.transform = "translateY(0)";
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15 }
    );

    revealTargets.forEach(function (el) {
      el.style.opacity = "0";
      el.style.transform = "translateY(24px)";
      el.style.transition = "opacity 0.6s ease, transform 0.6s ease";
      observer.observe(el);
    });
  }
});
