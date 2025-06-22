
import { Product } from '../types/product';

export const mockProducts: Product[] = [
  {
    id: 'sofa-001',
    title: 'Modern Curved Velvet Sofa',
    vendor: 'Article',
    price: 1299,
    image_url: 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=600&h=400&fit=crop',
    category: 'sofa',
    description: 'A luxurious curved sofa with deep seating and rich velvet upholstery',
    dimensions: { width: 84, height: 32, depth: 36 },
    materials: ['velvet', 'oak legs'],
    style_tags: ['modern', 'curved', 'luxury'],
    similarity: 0.95,
    vendor_url: 'https://article.com/product/example'
  },
  {
    id: 'sofa-002',
    title: 'Minimalist Linen Sectional',
    vendor: 'West Elm',
    price: 1899,
    image_url: 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=600&h=400&fit=crop',
    category: 'sofa',
    description: 'Clean lines meet comfort in this versatile sectional sofa',
    dimensions: { width: 96, height: 30, depth: 38 },
    materials: ['linen', 'walnut'],
    style_tags: ['minimalist', 'sectional', 'neutral'],
    similarity: 0.87,
    vendor_url: 'https://westelm.com/product/example'
  },
  {
    id: 'chair-001',
    title: 'Mid-Century Leather Accent Chair',
    vendor: 'CB2',
    price: 699,
    image_url: 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=600&h=400&fit=crop',
    category: 'chair',
    description: 'Iconic mid-century design with premium leather upholstery',
    dimensions: { width: 28, height: 30, depth: 32 },
    materials: ['leather', 'walnut'],
    style_tags: ['mid-century', 'accent', 'leather'],
    similarity: 0.82,
    vendor_url: 'https://cb2.com/product/example'
  },
  {
    id: 'table-001',
    title: 'Live Edge Dining Table',
    vendor: 'Wayfair',
    price: 1499,
    image_url: 'https://images.unsplash.com/photo-1549497538-303791108f95?w=600&h=400&fit=crop',
    category: 'table',
    description: 'Stunning live edge wood table with natural variations',
    dimensions: { width: 72, height: 30, depth: 36 },
    materials: ['walnut', 'steel'],
    style_tags: ['rustic', 'natural', 'dining'],
    similarity: 0.78,
    vendor_url: 'https://wayfair.com/product/example'
  },
  {
    id: 'sofa-003',
    title: 'Tufted Chesterfield Sofa',
    vendor: 'Pottery Barn',
    price: 2199,
    image_url: 'https://images.unsplash.com/photo-1506439773649-6e0eb8cfb237?w=600&h=400&fit=crop',
    category: 'sofa',
    description: 'Classic button-tufted design with rolled arms',
    dimensions: { width: 78, height: 32, depth: 37 },
    materials: ['leather', 'mahogany'],
    style_tags: ['traditional', 'tufted', 'classic'],
    similarity: 0.74,
    vendor_url: 'https://potterybarn.com/product/example'
  }
];
