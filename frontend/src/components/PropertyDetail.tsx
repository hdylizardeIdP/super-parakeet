import { useState } from "react";
import type { Property } from "../types/property";
import ContactForm from "./ContactForm";

interface Props {
  property: Property;
  onClose: () => void;
}

function formatPrice(price: number): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(price);
}

export default function PropertyDetail({ property, onClose }: Props) {
  const [currentPhoto, setCurrentPhoto] = useState(0);
  const [showContact, setShowContact] = useState(false);

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>
          &times;
        </button>

        <div className="detail-gallery">
          {property.photos.length > 0 ? (
            <>
              <img
                src={property.photos[currentPhoto]}
                alt={property.title}
                className="detail-main-photo"
              />
              {property.photos.length > 1 && (
                <div className="detail-thumbnails">
                  {property.photos.map((photo, i) => (
                    <img
                      key={i}
                      src={photo}
                      alt={`${property.title} ${i + 1}`}
                      className={i === currentPhoto ? "thumb-active" : ""}
                      onClick={() => setCurrentPhoto(i)}
                    />
                  ))}
                </div>
              )}
            </>
          ) : (
            <div className="detail-no-photo">No photos available</div>
          )}
        </div>

        <div className="detail-info">
          <div className="detail-header">
            <h2>{property.title}</h2>
            <span className={`status-badge status-${property.listing_status.toLowerCase()}`}>
              {property.listing_status}
            </span>
          </div>
          <p className="detail-price">{formatPrice(property.price)}</p>
          <p className="detail-address">
            {property.address}, {property.city}, {property.state}{" "}
            {property.zip_code}
          </p>

          <div className="detail-stats">
            {property.bedrooms > 0 && (
              <div className="stat">
                <strong>{property.bedrooms}</strong>
                <span>Bedrooms</span>
              </div>
            )}
            {property.bathrooms > 0 && (
              <div className="stat">
                <strong>{property.bathrooms}</strong>
                <span>Bathrooms</span>
              </div>
            )}
            <div className="stat">
              <strong>{property.square_footage.toLocaleString()}</strong>
              <span>Sq Ft</span>
            </div>
            <div className="stat">
              <strong>{property.property_type}</strong>
              <span>Type</span>
            </div>
          </div>

          <div className="detail-description">
            <h3>Description</h3>
            <p>{property.description}</p>
          </div>

          {!showContact ? (
            <button
              className="btn btn-primary btn-full"
              onClick={() => setShowContact(true)}
            >
              Contact Agent About This Property
            </button>
          ) : (
            <ContactForm
              propertyId={property.id}
              onClose={() => setShowContact(false)}
            />
          )}
        </div>
      </div>
    </div>
  );
}
