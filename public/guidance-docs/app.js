(function () {
  let allDocs = [];
  let filtered = [];
  let currentPage = 1;
  let sortField = "issueDate";
  let sortDir = -1; // -1 = desc
  const TOPIC_PRIORITY = [
    "Medical Devices",
    "Premarket",
    "510(k)",
    "Digital Health",
    "Current Good Manufacturing Practice (CGMP)",
    "Postmarket",
    "Clinical Trials",
    "Labeling",
    "Bioequivalence",
    "IVDs (In Vitro Diagnostic Devices)",
    "Premarket Approval (PMA)",
    "HUD/HDE",
    "Investigational Device Exemption (IDE)",
    "Cybersecurity",
    "Artificial Intelligence",
    "Software",
    "Combination Products",
    "Adverse Event Reporting",
    "UDI",
    "Radiation-Emitting Products",
  ];
  const KEY_TOPICS = new Set([
    "Medical Devices",
    "Premarket",
    "510(k)",
    "Digital Health",
    "Current Good Manufacturing Practice (CGMP)",
    "Postmarket",
    "Clinical Trials",
    "Labeling",
    "IVDs (In Vitro Diagnostic Devices)",
    "Premarket Approval (PMA)",
    "HUD/HDE",
    "Investigational Device Exemption (IDE)",
    "Combination Products",
    "Adverse Event Reporting",
    "UDI",
    "Radiation-Emitting Products",
    "Cardiovascular",
    "Dental",
    "Ophthalmic",
    "Orthopedic",
    "Neurological",
    "Gastroenterology-Urology",
    "Anesthesiology",
    "Hematology & Pathology",
    "Radiology",
    "General Hospital & Personal Use",
    "Biologics",
    "Investigation & Enforcement",
    "Compliance",
    "Administrative / Procedural",
    "International",
    "Inspection",
    "Real World Data / Real World Evidence (RWD/RWE)",
    "Artificial Intelligence",
    "Electronic Submissions",
    "Advisory Committees",
    "CLIA (Clinical Laboratory Improvement Amendments)",
    "Immunology & Microbiology",
    "Obstetrical & Gynecological",
    "General & Plastic Surgery",
    "Physical Medicine",
  ]);

  // Load data
  fetch("guidance-data.json")
    .then(function (r) {
      return r.json();
    })
    .then(function (data) {
      allDocs = data;
      // Parse dates for sorting
      allDocs.forEach(function (d) {
        var parts = d.issueDate.split("/");
        d._dateNum =
          parts.length === 3 ? parseInt(parts[2] + parts[0] + parts[1]) : 0;
      });
      populateTopicFilter();
      applyFilters();
      document.getElementById("loading").style.display = "none";
      document.getElementById("resultsArea").style.display = "";
    })
    .catch(function () {
      document.getElementById("loading").innerHTML =
        '<p style="color:#ef4444">Failed to load guidance documents data.</p>';
    });

  function populateTopicFilter() {
    var counts = {};
    allDocs.forEach(function (d) {
      d.topic.split(",").forEach(function (t) {
        t = t.trim();
        if (t && KEY_TOPICS.has(t)) {
          counts[t] = (counts[t] || 0) + 1;
        }
      });
    });
    var sorted = Object.entries(counts).sort(function (a, b) {
      var ai = TOPIC_PRIORITY.indexOf(a[0]);
      var bi = TOPIC_PRIORITY.indexOf(b[0]);
      if (ai >= 0 && bi >= 0) return ai - bi;
      if (ai >= 0) return -1;
      if (bi >= 0) return 1;
      return b[1] - a[1];
    });
    var sel = document.getElementById("topicFilter");
    sorted.forEach(function (entry) {
      var topic = entry[0],
        count = entry[1];
      var opt = document.createElement("option");
      opt.value = topic;
      opt.textContent = topic + " (" + count + ")";
      sel.appendChild(opt);
    });
  }

  function applyFilters() {
    var q = document.getElementById("searchInput").value.trim().toLowerCase();
    var topic = document.getElementById("topicFilter").value;
    var status = document.getElementById("statusFilter").value;
    var yFrom = parseInt(document.getElementById("yearFrom").value) || 0;
    var yTo = parseInt(document.getElementById("yearTo").value) || 9999;

    filtered = allDocs.filter(function (d) {
      if (q) {
        var haystack = (
          d.title +
          " " +
          d.topic +
          " " +
          d.docketNumber
        ).toLowerCase();
        var terms = q.split(/\s+/);
        if (
          !terms.every(function (t) {
            return haystack.includes(t);
          })
        )
          return false;
      }
      if (
        topic &&
        !d.topic
          .split(",")
          .map(function (t) {
            return t.trim();
          })
          .includes(topic)
      )
        return false;
      if (status && d.status !== status) return false;
      if (yFrom || yTo < 9999) {
        var parts = d.issueDate.split("/");
        var yr = parts.length === 3 ? parseInt(parts[2]) : 0;
        if (yr < yFrom || yr > yTo) return false;
      }
      return true;
    });

    // Sort
    filtered.sort(function (a, b) {
      var va, vb;
      if (sortField === "issueDate") {
        va = a._dateNum;
        vb = b._dateNum;
      } else if (sortField === "title") {
        va = a.title.toLowerCase();
        vb = b.title.toLowerCase();
      } else if (sortField === "topic") {
        va = a.topic.toLowerCase();
        vb = b.topic.toLowerCase();
      } else if (sortField === "status") {
        va = a.status;
        vb = b.status;
      } else {
        va = a[sortField];
        vb = b[sortField];
      }
      if (va < vb) return -1 * sortDir;
      if (va > vb) return 1 * sortDir;
      return 0;
    });

    currentPage = 1;
    renderResults();
  }

  function renderResults() {
    var body = document.getElementById("resultsBody");
    var perPage = parseInt(document.getElementById("perPage").value) || 0;
    var total = filtered.length;
    var pages = perPage > 0 ? Math.ceil(total / perPage) : 1;
    if (currentPage > pages) currentPage = pages || 1;

    document.getElementById("resultCount").textContent = total;
    document.getElementById("noResults").style.display =
      total === 0 ? "" : "none";
    document.getElementById("resultsArea").style.display =
      total === 0 ? "none" : "";

    var start = perPage > 0 ? (currentPage - 1) * perPage : 0;
    var end = perPage > 0 ? Math.min(start + perPage, total) : total;
    var slice = filtered.slice(start, end);

    document.getElementById("pageInfo").textContent =
      perPage > 0
        ? "Showing " + (start + 1) + "\u2013" + end + " of " + total
        : "Showing all " + total;

    body.innerHTML = "";
    slice.forEach(function (d) {
      var tr = document.createElement("tr");

      // Title
      var tdTitle = document.createElement("td");
      tdTitle.className = "title-cell";
      var a = document.createElement("a");
      a.href = d.pageUrl;
      a.target = "_blank";
      a.rel = "noopener noreferrer";
      a.textContent = d.title;
      tdTitle.appendChild(a);
      tr.appendChild(tdTitle);

      // Date
      var tdDate = document.createElement("td");
      tdDate.className = "date-cell";
      tdDate.textContent = d.issueDate;
      tr.appendChild(tdDate);

      // Topic
      var tdTopic = document.createElement("td");
      tdTopic.className = "topic-cell";
      var topics = d.topic
        .split(",")
        .map(function (t) {
          return t.trim();
        })
        .filter(Boolean);
      topics.forEach(function (t) {
        var span = document.createElement("span");
        span.className = "topic-tag";
        span.textContent = t;
        tdTopic.appendChild(span);
      });
      tr.appendChild(tdTopic);

      // Status
      var tdStatus = document.createElement("td");
      var badge = document.createElement("span");
      badge.className =
        "status-badge " +
        (d.status === "Final" ? "status-final" : "status-draft");
      badge.textContent = d.status;
      tdStatus.appendChild(badge);
      tr.appendChild(tdStatus);

      // PDF
      var tdPdf = document.createElement("td");
      if (d.pdfUrl) {
        var pdfA = document.createElement("a");
        pdfA.href = d.pdfUrl;
        pdfA.target = "_blank";
        pdfA.rel = "noopener noreferrer";
        pdfA.className = "pdf-link";
        pdfA.innerHTML = '<span class="pdf-icon">\uD83D\uDCC4</span> PDF';
        tdPdf.appendChild(pdfA);
      }
      tr.appendChild(tdPdf);

      body.appendChild(tr);
    });

    renderPagination(pages);
    updateSortArrows();
  }

  function renderPagination(pages) {
    var container = document.getElementById("pagination");
    container.innerHTML = "";
    if (pages <= 1) return;

    function addBtn(label, page, disabled) {
      var btn = document.createElement("button");
      btn.className = "page-btn" + (page === currentPage ? " active" : "");
      btn.textContent = label;
      btn.disabled = disabled;
      if (!disabled)
        btn.onclick = function () {
          currentPage = page;
          renderResults();
          window.scrollTo(0, 0);
        };
      container.appendChild(btn);
    }

    addBtn("\u2039", currentPage - 1, currentPage <= 1);
    var startP = Math.max(1, currentPage - 3);
    var endP = Math.min(pages, startP + 6);
    if (endP - startP < 6) startP = Math.max(1, endP - 6);
    if (startP > 1) {
      addBtn("1", 1, false);
      if (startP > 2) {
        var el = document.createElement("span");
        el.textContent = "\u2026";
        el.style.color = "#6b7280";
        container.appendChild(el);
      }
    }
    for (var i = startP; i <= endP; i++) addBtn(String(i), i, false);
    if (endP < pages) {
      if (endP < pages - 1) {
        var el2 = document.createElement("span");
        el2.textContent = "\u2026";
        el2.style.color = "#6b7280";
        container.appendChild(el2);
      }
      addBtn(String(pages), pages, false);
    }
    addBtn("\u203A", currentPage + 1, currentPage >= pages);
  }

  function updateSortArrows() {
    document.querySelectorAll("thead th[data-sort]").forEach(function (th) {
      var arrow = th.querySelector(".sort-arrow");
      if (th.dataset.sort === sortField) {
        arrow.textContent = sortDir > 0 ? "\u25B2" : "\u25BC";
      } else {
        arrow.textContent = "";
      }
    });
  }

  // Event listeners
  document.getElementById("searchBtn").onclick = function () {
    applyFilters();
  };
  document
    .getElementById("searchInput")
    .addEventListener("keydown", function (e) {
      if (e.key === "Enter") applyFilters();
    });
  document.getElementById("topicFilter").onchange = function () {
    applyFilters();
  };
  document.getElementById("statusFilter").onchange = function () {
    applyFilters();
  };
  document.getElementById("yearFrom").onchange = function () {
    applyFilters();
  };
  document.getElementById("yearTo").onchange = function () {
    applyFilters();
  };
  document.getElementById("perPage").onchange = function () {
    currentPage = 1;
    renderResults();
  };

  // Sorting
  document.querySelectorAll("thead th[data-sort]").forEach(function (th) {
    th.onclick = function () {
      var field = th.dataset.sort;
      if (sortField === field) sortDir *= -1;
      else {
        sortField = field;
        sortDir = field === "issueDate" ? -1 : 1;
      }
      renderResults();
    };
  });

  // Listen for parent iframe messages
  window.addEventListener("message", function (e) {
    if (e.data && e.data.type === "setLang") {
      // Future: could support i18n
    }
  });
})();
