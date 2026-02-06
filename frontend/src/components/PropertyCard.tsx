import type { Property } from "../types/property";

interface Props {
  property: Property;
  onClick: (property: Property) => void;
}

function formatPrice(price: number): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(price);
}

export default function PropertyCard({ property, onClick }: Props) {
  return (
    <div className="property-card" onClick={() => onClick(property)}>
      <div className="property-card-image">
        <img
          src={property.photos[0] || "https://via.placeholder.com/400x300?text=No+Photo"}
          alt={property.title}
          loading="lazy"
        />
        <span className={`status-badge status-${property.listing_status.toLowerCase()}`}>
          {property.listing_status}
        </span>
      </div>
      <div className="property-card-body">
        <h3 className="property-price">{formatPrice(property.price)}</h3>
        <p className="property-title">{property.title}</p>
        <p className="property-address">
          {property.address}, {property.city}, {property.state} {property.zip_code}
        </p>
        <div className="property-meta">
          {property.bedrooms > 0 && (
            <span>{property.bedrooms} bd</span>
          )}
          {property.bathrooms > 0 && (
            <span>{property.bathrooms} ba</span>
          )}
          <span>{property.square_footage.toLocaleString()} sqft</span>
          <span className="property-type-tag">{property.property_type}</span>
        </div>
      </div>
    </div>
  );
}
