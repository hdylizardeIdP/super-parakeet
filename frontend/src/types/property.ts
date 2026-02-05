export interface Property {
  id: number;
  title: string;
  description: string;
  price: number;
  address: string;
  city: string;
  state: string;
  zip_code: string;
  bedrooms: number;
  bathrooms: number;
  square_footage: number;
  property_type: string;
  listing_status: string;
  photos: string[];
  latitude: number | null;
  longitude: number | null;
}

export interface PropertyFilters {
  min_price?: number;
  max_price?: number;
  city?: string;
  bedrooms?: number;
  property_type?: string;
  search?: string;
}

export interface ContactFormData {
  property_id: number;
  name: string;
  email: string;
  phone?: string;
  message: string;
}
