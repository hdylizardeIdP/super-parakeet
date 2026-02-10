import type { Property, PropertyFilters, ContactFormData } from "../types/property";

const API_BASE = import.meta.env.VITE_API_URL ?? "";

export async function fetchProperties(
  filters: PropertyFilters = {}
): Promise<Property[]> {
  const params = new URLSearchParams();
  if (filters.min_price) params.set("min_price", String(filters.min_price));
  if (filters.max_price) params.set("max_price", String(filters.max_price));
  if (filters.city) params.set("city", filters.city);
  if (filters.bedrooms) params.set("bedrooms", String(filters.bedrooms));
  if (filters.property_type) params.set("property_type", filters.property_type);
  if (filters.search) params.set("search", filters.search);

  const res = await fetch(`${API_BASE}/api/properties?${params}`);
  if (!res.ok) throw new Error("Failed to fetch properties");
  return res.json();
}

export async function submitContactInquiry(
  data: ContactFormData
): Promise<void> {
  const res = await fetch(`${API_BASE}/api/contact`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to submit inquiry");
}
