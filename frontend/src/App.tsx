import { useEffect, useState } from "react";
import type { Property, PropertyFilters } from "./types/property";
import { fetchProperties } from "./api/client";
import FilterBar from "./components/FilterBar";
import PropertyCard from "./components/PropertyCard";
import PropertyDetail from "./components/PropertyDetail";
import PropertyMap from "./components/PropertyMap";
import "./App.css";

type ViewMode = "grid" | "map";

function App() {
  const [properties, setProperties] = useState<Property[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selected, setSelected] = useState<Property | null>(null);
  const [viewMode, setViewMode] = useState<ViewMode>("grid");

  async function loadProperties(filters: PropertyFilters = {}) {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchProperties(filters);
      setProperties(data);
    } catch {
      setError("Failed to load properties. Is the backend running?");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadProperties();
  }, []);

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>Premier Properties</h1>
          <p>Find your dream home today</p>
        </div>
      </header>

      <main className="app-main">
        <FilterBar onFilter={loadProperties} />

        <div className="view-toggle">
          <button
            className={`btn ${viewMode === "grid" ? "btn-primary" : "btn-secondary"}`}
            onClick={() => setViewMode("grid")}
          >
            Grid View
          </button>
          <button
            className={`btn ${viewMode === "map" ? "btn-primary" : "btn-secondary"}`}
            onClick={() => setViewMode("map")}
          >
            Map View
          </button>
          <span className="result-count">
            {properties.length}{" "}
            {properties.length === 1 ? "property" : "properties"} found
          </span>
        </div>

        {loading && <div className="loading">Loading properties...</div>}
        {error && <div className="error-message">{error}</div>}

        {!loading && !error && viewMode === "grid" && (
          <div className="property-grid">
            {properties.map((p) => (
              <PropertyCard key={p.id} property={p} onClick={setSelected} />
            ))}
            {properties.length === 0 && (
              <p className="no-results">
                No properties match your filters. Try adjusting your search.
              </p>
            )}
          </div>
        )}

        {!loading && !error && viewMode === "map" && (
          <PropertyMap properties={properties} onSelect={setSelected} />
        )}
      </main>

      <footer className="app-footer">
        <p>&copy; 2026 Premier Properties. All rights reserved.</p>
      </footer>

      {selected && (
        <PropertyDetail
          property={selected}
          onClose={() => setSelected(null)}
        />
      )}
    </div>
  );
}

export default App;
