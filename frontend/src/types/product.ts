export interface Product {
  id: string;
  name: string;
  price: number;
  image: string;
  category: string;
  similarity: number;
  url: string;
  condition: string;
  location: string;
  shippingCost: number;
  sellerRating: number;
}

export interface SearchSession {
  original_prompt: string;
  parsed_spec: {
    category: string;
    dimensions: Record<string, number>;
    materials: string[];
    style_keywords: string[];
    hard_requirements: string[];
  };
  refinements: string[];
  products: Product[];
}
