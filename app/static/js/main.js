// Enhanced JavaScript for Resume Generator with Modern Features

document.addEventListener("DOMContentLoaded", function () {
  // Initialize all components
  initializeBootstrapComponents();
  initializeFormValidation();
  initializeAnimations();
  initializeInteractivity();
  initializeFileHandling();
  initializeFormEnhancements();
  initializeProgressiveFeatures();

  // Auto-hide alerts after 5 seconds with fade animation
  const alerts = document.querySelectorAll(".alert:not(.alert-permanent)");
  alerts.forEach(function (alert) {
    setTimeout(function () {
      alert.style.transition = "opacity 0.5s ease-out, transform 0.5s ease-out";
      alert.style.opacity = "0";
      alert.style.transform = "translateY(-20px)";
      setTimeout(() => {
        const bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
      }, 500);
    }, 5000);
  });
});

// Initialize Bootstrap Components
function initializeBootstrapComponents() {
  // Initialize tooltips with enhanced options
  const tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl, {
      animation: true,
      delay: { show: 500, hide: 100 },
      html: true,
    });
  });

  // Initialize popovers with enhanced styling
  const popoverTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="popover"]')
  );
  const popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl, {
      animation: true,
      html: true,
      trigger: "hover focus",
    });
  });
}

// Enhanced Form Validation
function initializeFormValidation() {
  const forms = document.querySelectorAll(".needs-validation");
  Array.prototype.slice.call(forms).forEach(function (form) {
    form.addEventListener(
      "submit",
      function (event) {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();

          // Smooth scroll to first invalid field
          const firstInvalidField = form.querySelector(":invalid");
          if (firstInvalidField) {
            firstInvalidField.scrollIntoView({
              behavior: "smooth",
              block: "center",
            });
            firstInvalidField.focus();
          }

          showToast("Please fill in all required fields correctly", "warning");
        }
        form.classList.add("was-validated");
      },
      false
    );
  });

  // Real-time validation feedback
  const inputs = document.querySelectorAll(".form-control, .form-select");
  inputs.forEach((input) => {
    input.addEventListener("blur", function () {
      validateField(this);
    });

    input.addEventListener(
      "input",
      debounce(function () {
        if (this.classList.contains("is-invalid")) {
          validateField(this);
        }
      }, 300)
    );
  });
}

// Field validation with enhanced feedback
function validateField(field) {
  const isValid = field.checkValidity();
  const feedbackElement =
    field.parentNode.querySelector(".invalid-feedback") ||
    createFeedbackElement(field);

  if (isValid) {
    field.classList.remove("is-invalid");
    field.classList.add("is-valid");
    feedbackElement.style.display = "none";
  } else {
    field.classList.remove("is-valid");
    field.classList.add("is-invalid");
    feedbackElement.textContent = getValidationMessage(field);
    feedbackElement.style.display = "block";
  }
}

function createFeedbackElement(field) {
  const feedback = document.createElement("div");
  feedback.className = "invalid-feedback";
  field.parentNode.appendChild(feedback);
  return feedback;
}

function getValidationMessage(field) {
  if (field.validity.valueMissing) {
    return `${getFieldLabel(field)} is required.`;
  }
  if (field.validity.typeMismatch) {
    return `Please enter a valid ${field.type}.`;
  }
  if (field.validity.patternMismatch) {
    return `Please match the requested format.`;
  }
  if (field.validity.tooShort) {
    return `Please enter at least ${field.minLength} characters.`;
  }
  if (field.validity.tooLong) {
    return `Please enter no more than ${field.maxLength} characters.`;
  }
  return "Please enter a valid value.";
}

function getFieldLabel(field) {
  const label = document.querySelector(`label[for="${field.id}"]`);
  return label ? label.textContent.replace("*", "").trim() : "This field";
}

// Initialize Animations
function initializeAnimations() {
  // Intersection Observer for scroll animations
  const animationObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("fade-in-up");
          animationObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1 }
  );

  // Observe elements for animation
  document
    .querySelectorAll(".card, .section-header, .feature-icon")
    .forEach((el) => {
      animationObserver.observe(el);
    });

  // Smooth scrolling for anchor links with easing
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        const offset = 80; // Account for fixed navbar
        const elementPosition = target.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - offset;

        window.scrollTo({
          top: offsetPosition,
          behavior: "smooth",
        });
      }
    });
  });
}

// Enhanced Interactivity
function initializeInteractivity() {
  // Enhanced loading states for forms
  const submitButtons = document.querySelectorAll('form button[type="submit"]');
  submitButtons.forEach((button) => {
    const form = button.closest("form");
    if (form) {
      form.addEventListener("submit", function (e) {
        if (form.checkValidity()) {
          showLoadingState(button);

          // Auto re-enable after timeout as fallback
          setTimeout(() => {
            hideLoadingState(button);
          }, 30000);
        }
      });
    }
  });

  // Enhanced hover effects for cards
  const cards = document.querySelectorAll(".card");
  cards.forEach((card) => {
    card.addEventListener("mouseenter", function () {
      this.style.transition = "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)";
    });
  });

  // Template selection enhancements
  const templateInputs = document.querySelectorAll('input[name="template_id"]');
  templateInputs.forEach((input) => {
    input.addEventListener("change", function () {
      // Add selection animation
      const preview = this.parentNode.querySelector(".template-preview");
      if (preview) {
        preview.style.transform = "scale(0.95)";
        setTimeout(() => {
          preview.style.transform = "scale(1)";
        }, 150);
      }
    });
  });
}

function showLoadingState(button) {
  button.disabled = true;
  const originalText = button.innerHTML;
  button.dataset.originalText = originalText;

  button.innerHTML = `
    <span class="spinner-border spinner-border-sm me-2" role="status"></span>
    Processing...
  `;

  // Add loading class for styling
  button.classList.add("btn-loading");
}

function hideLoadingState(button) {
  button.disabled = false;
  button.innerHTML = button.dataset.originalText || button.innerHTML;
  button.classList.remove("btn-loading");
  delete button.dataset.originalText;
}

// Enhanced File Handling
function initializeFileHandling() {
  // Enhanced character counter for textareas
  const textareas = document.querySelectorAll("textarea[maxlength]");
  textareas.forEach((textarea) => {
    const maxLength = parseInt(textarea.getAttribute("maxlength"));
    const counter = document.createElement("div");
    counter.className = "character-counter text-muted mt-1";
    counter.innerHTML = `<small>0/${maxLength} characters</small>`;
    textarea.parentNode.appendChild(counter);

    function updateCounter() {
      const currentLength = textarea.value.length;
      const percentage = (currentLength / maxLength) * 100;

      counter.innerHTML = `<small>${currentLength}/${maxLength} characters</small>`;

      if (percentage > 90) {
        counter.className = "character-counter text-danger mt-1";
      } else if (percentage > 75) {
        counter.className = "character-counter text-warning mt-1";
      } else {
        counter.className = "character-counter text-muted mt-1";
      }
    }

    textarea.addEventListener("input", updateCounter);
    textarea.addEventListener("paste", () => setTimeout(updateCounter, 10));
  });

  // Auto-resize textareas with smooth transitions
  const autoResizeTextareas = document.querySelectorAll("textarea.auto-resize");
  autoResizeTextareas.forEach((textarea) => {
    function resize() {
      textarea.style.height = "auto";
      textarea.style.height = textarea.scrollHeight + "px";
    }

    textarea.addEventListener("input", resize);
    textarea.addEventListener("focus", resize);

    // Initial resize
    resize();
  });

  // Enhanced phone number formatting with international support
  const phoneInputs = document.querySelectorAll('input[type="tel"]');
  phoneInputs.forEach((input) => {
    input.addEventListener("input", function (e) {
      let value = e.target.value.replace(/\D/g, "");
      let formatted = "";

      if (value.length >= 10) {
        // US format: (123) 456-7890
        formatted = value.replace(/(\d{3})(\d{3})(\d{4})/, "($1) $2-$3");
      } else if (value.length >= 6) {
        formatted = value.replace(/(\d{3})(\d{3})/, "($1) $2");
      } else if (value.length >= 3) {
        formatted = value.replace(/(\d{3})/, "($1) ");
      } else {
        formatted = value;
      }

      e.target.value = formatted;
    });
  });

  // Enhanced URL validation and formatting
  const urlInputs = document.querySelectorAll('input[type="url"]');
  urlInputs.forEach((input) => {
    input.addEventListener("blur", function () {
      let url = this.value.trim();
      if (url && !url.startsWith("http://") && !url.startsWith("https://")) {
        this.value = "https://" + url;
      }
    });

    // Real-time URL validation feedback
    input.addEventListener(
      "input",
      debounce(function () {
        const isValid = isValidURL(this.value);
        if (this.value && !isValid) {
          this.setCustomValidity("Please enter a valid URL");
        } else {
          this.setCustomValidity("");
        }
      }, 500)
    );
  });
}

// Enhanced Form Features
function initializeFormEnhancements() {
  // Auto-save functionality with visual feedback
  const autoSaveForms = document.querySelectorAll(".auto-save");
  autoSaveForms.forEach((form) => {
    const formId = form.id || "unnamed-form";
    const saveKey = `form-autosave-${formId}`;
    let saveIndicator = createSaveIndicator(form);

    // Load saved data
    const savedData = loadFromLocalStorage(saveKey);
    if (savedData) {
      Object.keys(savedData).forEach((name) => {
        const field = form.querySelector(`[name="${name}"]`);
        if (field) {
          field.value = savedData[name];
          // Trigger change event to update any dependent UI
          field.dispatchEvent(new Event("change", { bubbles: true }));
        }
      });
      showToast("Form data restored from auto-save", "info");
    }

    // Enhanced auto-save with debouncing
    const debouncedSave = debounce(() => {
      const formData = new FormData(form);
      const data = {};
      for (let [key, value] of formData.entries()) {
        data[key] = value;
      }

      if (saveToLocalStorage(saveKey, data)) {
        showSaveIndicator(saveIndicator, "saved");
      } else {
        showSaveIndicator(saveIndicator, "error");
      }
    }, 2000);

    form.addEventListener("input", () => {
      showSaveIndicator(saveIndicator, "saving");
      debouncedSave();
    });

    // Clear on successful submit
    form.addEventListener("submit", function () {
      localStorage.removeItem(saveKey);
      hideSaveIndicator(saveIndicator);
    });
  });

  // Enhanced skills input with tag-like interface
  const skillsInput = document.getElementById("skills");
  if (skillsInput) {
    enhanceSkillsInput(skillsInput);
  }
}

function createSaveIndicator(form) {
  const indicator = document.createElement("div");
  indicator.className = "save-indicator position-fixed";
  indicator.style.cssText = `
    top: 20px;
    right: 20px;
    z-index: 1050;
    opacity: 0;
    transition: opacity 0.3s ease;
  `;
  document.body.appendChild(indicator);
  return indicator;
}

function showSaveIndicator(indicator, status) {
  const icons = {
    saving: '<i class="fas fa-spinner fa-spin text-info"></i> Saving...',
    saved: '<i class="fas fa-check text-success"></i> Saved',
    error:
      '<i class="fas fa-exclamation-triangle text-warning"></i> Save failed',
  };

  indicator.innerHTML = `<small class="badge bg-light text-dark p-2">${icons[status]}</small>`;
  indicator.style.opacity = "1";

  if (status === "saved") {
    setTimeout(() => hideSaveIndicator(indicator), 2000);
  }
}

function hideSaveIndicator(indicator) {
  indicator.style.opacity = "0";
}

function enhanceSkillsInput(input) {
  const container = document.createElement("div");
  container.className = "skills-container mb-2";

  const tagsContainer = document.createElement("div");
  tagsContainer.className = "skills-tags d-flex flex-wrap gap-2 mb-2";

  input.parentNode.insertBefore(container, input);
  container.appendChild(tagsContainer);
  container.appendChild(input);

  input.style.display = "none";

  const skillInput = document.createElement("input");
  skillInput.type = "text";
  skillInput.className = "form-control";
  skillInput.placeholder = "Add skills (press Enter or comma to add)";
  container.appendChild(skillInput);

  let skills = input.value
    ? input.value
        .split(",")
        .map((s) => s.trim())
        .filter((s) => s)
    : [];

  function updateSkillsDisplay() {
    tagsContainer.innerHTML = "";
    skills.forEach((skill, index) => {
      const tag = document.createElement("span");
      tag.className = "badge bg-primary";
      tag.innerHTML = `
        ${skill}
        <button type="button" class="btn-close btn-close-white btn-sm ms-1" 
                onclick="removeSkill(${index})" aria-label="Remove skill"></button>
      `;
      tagsContainer.appendChild(tag);
    });
    input.value = skills.join(", ");
  }

  function addSkill(skill) {
    skill = skill.trim();
    if (skill && !skills.includes(skill)) {
      skills.push(skill);
      updateSkillsDisplay();
      skillInput.value = "";
    }
  }

  window.removeSkill = function (index) {
    skills.splice(index, 1);
    updateSkillsDisplay();
  };

  skillInput.addEventListener("keydown", function (e) {
    if (e.key === "Enter" || e.key === ",") {
      e.preventDefault();
      addSkill(this.value);
    }
  });

  skillInput.addEventListener("blur", function () {
    if (this.value.trim()) {
      addSkill(this.value);
    }
  });

  updateSkillsDisplay();
}

// Progressive Web App and Modern Features
function initializeProgressiveFeatures() {
  // Service Worker registration
  if ("serviceWorker" in navigator) {
    navigator.serviceWorker
      .register("/sw.js")
      .then((registration) => {
        console.log("SW registered: ", registration);
      })
      .catch((registrationError) => {
        console.log("SW registration failed: ", registrationError);
      });
  }

  // Enhanced keyboard shortcuts
  document.addEventListener("keydown", function (e) {
    // Ctrl+S to save (prevent default and trigger form submit)
    if (e.ctrlKey && e.key === "s") {
      e.preventDefault();
      const form = document.querySelector("form");
      if (form) {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn && !submitBtn.disabled) {
          submitBtn.click();
        }
      }
      showToast("Form saved", "success");
    }

    // Ctrl+N for new resume
    if (e.ctrlKey && e.key === "n") {
      e.preventDefault();
      window.location.href = "/raw-data";
    }

    // Escape to close modals and reset forms
    if (e.key === "Escape") {
      const modals = document.querySelectorAll(".modal.show");
      modals.forEach((modal) => {
        const bsModal = bootstrap.Modal.getInstance(modal);
        if (bsModal) bsModal.hide();
      });
    }
  });

  // Enhanced lazy loading for images
  if ("IntersectionObserver" in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.classList.remove("lazy");
          img.classList.add("fade-in");
          imageObserver.unobserve(img);
        }
      });
    });

    document.querySelectorAll("img[data-src]").forEach((img) => {
      imageObserver.observe(img);
    });
  }

  // Network status monitoring
  window.addEventListener("online", () => {
    showToast("Connection restored", "success");
  });

  window.addEventListener("offline", () => {
    showToast("You are currently offline", "warning");
  });
}

// Utility Functions
window.copyToClipboard = function (text) {
  if (navigator.clipboard) {
    navigator.clipboard
      .writeText(text)
      .then(() => showToast("Copied to clipboard!", "success"))
      .catch((err) => {
        console.error("Could not copy text: ", err);
        fallbackCopyToClipboard(text);
      });
  } else {
    fallbackCopyToClipboard(text);
  }
};

function fallbackCopyToClipboard(text) {
  const textArea = document.createElement("textarea");
  textArea.value = text;
  textArea.style.position = "fixed";
  textArea.style.left = "-999999px";
  textArea.style.top = "-999999px";
  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();

  try {
    document.execCommand("copy");
    showToast("Copied to clipboard!", "success");
  } catch (err) {
    showToast("Failed to copy to clipboard", "error");
  }

  document.body.removeChild(textArea);
}

// Enhanced Toast System
window.showToast = function (message, type = "info", duration = 5000) {
  const toastContainer =
    document.getElementById("toast-container") || createToastContainer();

  const toastId = "toast-" + Date.now();
  const bgClass = type === "error" ? "danger" : type;
  const iconClass =
    {
      success: "fa-check-circle",
      error: "fa-exclamation-circle",
      warning: "fa-exclamation-triangle",
      info: "fa-info-circle",
    }[type] || "fa-info-circle";

  const toast = document.createElement("div");
  toast.id = toastId;
  toast.className = `toast align-items-center text-white bg-${bgClass} border-0`;
  toast.setAttribute("role", "alert");
  toast.innerHTML = `
    <div class="d-flex">
      <div class="toast-body">
        <i class="fas ${iconClass} me-2"></i>${message}
      </div>
      <button type="button" class="btn-close btn-close-white me-2 m-auto" 
              data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
  `;

  toastContainer.appendChild(toast);
  const bsToast = new bootstrap.Toast(toast, { delay: duration });
  bsToast.show();

  toast.addEventListener("hidden.bs.toast", function () {
    toast.remove();
  });

  return toast;
};

function createToastContainer() {
  const container = document.createElement("div");
  container.id = "toast-container";
  container.className = "toast-container position-fixed top-0 end-0 p-3";
  container.style.zIndex = "9999";
  document.body.appendChild(container);
  return container;
}

// Enhanced Debounce Function
window.debounce = function (func, wait, immediate) {
  let timeout;
  return function executedFunction() {
    const context = this;
    const args = arguments;
    const later = function () {
      timeout = null;
      if (!immediate) func.apply(context, args);
    };
    const callNow = immediate && !timeout;
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    if (callNow) func.apply(context, args);
  };
};

// Enhanced Local Storage Helpers
window.saveToLocalStorage = function (key, data) {
  try {
    const serializedData = JSON.stringify(data);
    localStorage.setItem(key, serializedData);
    return true;
  } catch (e) {
    console.warn("Could not save to localStorage:", e);
    if (e.name === "QuotaExceededError") {
      showToast(
        "Storage quota exceeded. Some data may not be saved.",
        "warning"
      );
    }
    return false;
  }
};

window.loadFromLocalStorage = function (key) {
  try {
    const data = localStorage.getItem(key);
    return data ? JSON.parse(data) : null;
  } catch (e) {
    console.warn("Could not load from localStorage:", e);
    return null;
  }
};

// Enhanced API Helper Functions
window.apiCall = async function (url, options = {}) {
  const defaultOptions = {
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(url, defaultOptions);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const contentType = response.headers.get("content-type");
    if (contentType && contentType.includes("application/json")) {
      return await response.json();
    } else {
      return await response.text();
    }
  } catch (error) {
    handleAjaxError(error);
    throw error;
  }
};

window.handleAjaxError = function (error, userMessage = "An error occurred") {
  console.error("AJAX Error:", error);

  let message = userMessage;
  if (error.name === "TypeError" && error.message.includes("fetch")) {
    message = "Network error. Please check your connection.";
  } else if (error.message.includes("404")) {
    message = "The requested resource was not found.";
  } else if (error.message.includes("500")) {
    message = "Server error. Please try again later.";
  }

  showToast(message, "error");
};

// Enhanced Resume Application Object
window.ResumeApp = {
  // Save resume draft with timestamp
  saveDraft: function (formData) {
    const draftKey = "resume-draft";
    const draftData = {
      ...formData,
      timestamp: new Date().toISOString(),
      version: "1.0",
    };

    if (saveToLocalStorage(draftKey, draftData)) {
      showToast("Draft saved successfully", "success");
    }
  },

  // Load resume draft with version check
  loadDraft: function () {
    const draftKey = "resume-draft";
    const draft = loadFromLocalStorage(draftKey);

    if (draft && draft.timestamp) {
      const draftAge = Date.now() - new Date(draft.timestamp).getTime();
      const maxAge = 7 * 24 * 60 * 60 * 1000; // 7 days

      if (draftAge > maxAge) {
        this.clearDraft();
        return null;
      }
    }

    return draft;
  },

  // Clear resume draft
  clearDraft: function () {
    localStorage.removeItem("resume-draft");
  },

  // Enhanced validation with detailed feedback
  validateResumeData: function (data) {
    const errors = [];
    const warnings = [];

    // Required field validation
    if (!data.full_name || data.full_name.trim() === "") {
      errors.push("Full name is required");
    }

    if (!data.email || data.email.trim() === "") {
      errors.push("Email is required");
    } else if (!this.isValidEmail(data.email)) {
      errors.push("Please enter a valid email address");
    }

    // Optional field warnings
    if (!data.phone || data.phone.trim() === "") {
      warnings.push(
        "Consider adding a phone number for better contact options"
      );
    }

    if (!data.summary || data.summary.trim() === "") {
      warnings.push(
        "A professional summary can make your resume more compelling"
      );
    }

    return { errors, warnings };
  },

  // Enhanced email validation
  isValidEmail: function (email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  },

  // Enhanced phone number formatting with international support
  formatPhoneNumber: function (phoneNumber) {
    const cleaned = phoneNumber.replace(/\D/g, "");

    if (cleaned.length === 10) {
      return `(${cleaned.slice(0, 3)}) ${cleaned.slice(3, 6)}-${cleaned.slice(
        6
      )}`;
    } else if (cleaned.length === 11 && cleaned[0] === "1") {
      return `+1 (${cleaned.slice(1, 4)}) ${cleaned.slice(
        4,
        7
      )}-${cleaned.slice(7)}`;
    }

    return phoneNumber;
  },

  // Generate resume preview
  previewResume: function (resumeData) {
    console.log("Generating resume preview:", resumeData);
    // This would integrate with the backend preview generation
  },

  // Analytics tracking
  trackEvent: function (eventName, properties = {}) {
    console.log("Event tracked:", eventName, properties);
    // Integration with analytics service would go here
  },
};

// Utility Functions
window.formatFileSize = function (bytes, decimals = 2) {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ["Bytes", "KB", "MB", "GB", "TB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i];
};

window.printElement = function (elementId) {
  const element = document.getElementById(elementId);
  if (!element) {
    showToast("Print element not found", "error");
    return;
  }

  const printWindow = window.open("", "", "height=600,width=800");
  const printContent = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>Resume</title>
      <link rel="stylesheet" href="/static/css/style.css">
      <style>
        @media print {
          body { background: white !important; }
          * { -webkit-print-color-adjust: exact !important; }
        }
      </style>
    </head>
    <body onload="window.print();window.close();">
      ${element.innerHTML}
    </body>
    </html>
  `;

  printWindow.document.write(printContent);
  printWindow.document.close();
};

function isValidURL(string) {
  try {
    new URL(string);
    return true;
  } catch (_) {
    return false;
  }
}

// Component initialization for dynamic content
function initializeComponents() {
  // Re-initialize components when content is dynamically added
  const cards = document.querySelectorAll(".card");
  cards.forEach((card) => {
    card.addEventListener("mouseenter", function () {
      this.style.transition =
        "transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease";
    });
  });
}

// Export for module systems
if (typeof module !== "undefined" && module.exports) {
  module.exports = { ResumeApp, showToast, debounce };
}
