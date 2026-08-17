// ---------------------------------------------------------
// Directory template logic
// Loads listings.json, renders cards, wires up search + filters
// ---------------------------------------------------------

const state = {
  listings: [],
  activeCategory: "all",
  query: "",
};

const grid = document.getElementById("listing-grid");
const chipsWrap = document.getElementById("filter-chips");
const searchInput = document.getElementById("search-input");
const featuredRow = document.getElementById("featured-row");

document.getElementById("year").textContent = new Date().getFullYear();

async function init() {
  try {
    const res = await fetch("listings.json");
    state.listings = await res.json();
  } catch (err) {
    console.error("Could not load listings.json", err);
    state.listings = [];
  }
  renderChips();
  renderFeatured();
  render();
}

function renderChips() {
  const categories = ["all", ...new Set(state.listings.map((l) => l.category))];
  chipsWrap.innerHTML = "";
  categories.forEach((cat) => {
    const btn = document.createElement("button");
    btn.className = "chip";
    btn.type = "button";
    btn.textContent = cat === "all" ? "All" : cat;
    btn.setAttribute("aria-pressed", String(cat === state.activeCategory));
    btn.addEventListener("click", () => {
      state.activeCategory = cat;
      renderChips();
      render();
    });
    chipsWrap.appendChild(btn);
  });
}

function renderFeatured() {
  const featured = state.listings.filter((l) => l.featured);
  featuredRow.innerHTML = "";
  featured.forEach((l) => {
    const img = document.createElement("img");
    img.src = l.logo;
    img.alt = l.name;
    featuredRow.appendChild(img);
  });
}

function render() {
  const filtered = state.listings.filter((l) => {
    const matchesCategory = state.activeCategory === "all" || l.category === state.activeCategory;
    const matchesQuery = l.name.toLowerCase().includes(state.query.toLowerCase());
    return matchesCategory && matchesQuery;
  });

  grid.innerHTML = "";

  if (filtered.length === 0) {
    grid.innerHTML = `<p class="empty-state">No businesses match your search.</p>`;
    return;
  }

  filtered.forEach((listing) => {
    const card = document.createElement("article");
    card.className = "listing-card";
    card.innerHTML = `
      <img class="listing-card__logo" src="${listing.logo}" alt="${listing.name} logo">
      <p class="listing-card__name">${listing.name}</p>
      <span class="listing-card__category">${listing.category}</span>
      <a class="listing-card__link" href="${listing.url}" target="_blank" rel="noopener noreferrer">Visit website</a>
    `;
    grid.appendChild(card);
  });
}

searchInput.addEventListener("input", (e) => {
  state.query = e.target.value;
  render();
});

init();
