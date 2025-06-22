export interface EbayItem {
  item_id: string;
  title: string;
  price: number;
  currency: string;
  condition: string;
  location: string;
  image_url: string;
  item_url: string;
  shipping_cost?: number;
  seller_rating: number;
} 