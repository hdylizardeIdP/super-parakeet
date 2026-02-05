import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import { Property } from "../types/property";
import "leaflet/dist/leaflet.css";

// Fix default marker icon issue with bundlers
const defaultIcon = L.icon({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  iconRetinaUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

interface Props {
  properties: Property[];
  onSelect: (property: Property) => void;
}

function formatPrice(price: number): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(price);
}

export default function PropertyMap({ properties, onSelect }: Props) {
  const geoProperties = properties.filter(
    (p) => p.latitude != null && p.longitude != null
  );

  const center: [number, number] =
    geoProperties.length > 0
      ? [geoProperties[0].latitude!, geoProperties[0].longitude!]
      : [39.8283, -98.5795]; // center of US

  return (
    <MapContainer
      center={center}
      zoom={4}
      className="property-map"
      scrollWheelZoom={true}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {geoProperties.map((property) => (
        <Marker
          key={property.id}
          position={[property.latitude!, property.longitude!]}
          icon={defaultIcon}
          eventHandlers={{ click: () => onSelect(property) }}
        >
          <Popup>
            <strong>{property.title}</strong>
            <br />
            {formatPrice(property.price)}
            <br />
            {property.city}, {property.state}
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}
