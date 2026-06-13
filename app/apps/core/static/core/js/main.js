// Russian Fishing 4 — Frontend helpers

(function () {
  'use strict';

  // Auto-submit filter forms when a select changes
  document.querySelectorAll('.filter-auto-submit').forEach(function (el) {
    el.addEventListener('change', function () {
      this.closest('form').submit();
    });
  });

  // Toggle between kg and g display
  // (used by the weight unit toggle)

  // Highlight the active nav item based on URL
  var navLinks = document.querySelectorAll('.navbar-links a');
  var currentPath = window.location.pathname;
  navLinks.forEach(function (link) {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });

  // Confirm clear-tables action
  var clearBtn = document.getElementById('clear-tables-btn');
  if (clearBtn) {
    clearBtn.addEventListener('click', function (e) {
      if (!confirm('Are you sure you want to clear all data? This cannot be undone.')) {
        e.preventDefault();
      }
    });
  }

  // Tooltip for data age
  var timeElements = document.querySelectorAll('time.relative-time');
  if (timeElements.length) {
    timeElements.forEach(function (el) {
      var datetime = el.getAttribute('datetime');
      if (datetime) {
        var date = new Date(datetime);
        var now = new Date();
        var diff = Math.floor((now - date) / 1000);
        var relative = '';
        if (diff < 60) relative = 'just now';
        else if (diff < 3600) relative = Math.floor(diff / 60) + 'm ago';
        else if (diff < 86400) relative = Math.floor(diff / 3600) + 'h ago';
        else relative = Math.floor(diff / 86400) + 'd ago';
        el.textContent = relative;
      }
    });
  }
})();
