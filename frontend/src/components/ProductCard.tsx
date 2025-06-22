import React from 'react';
import { Product } from '../types/product';
import { Card } from './ui/card';
import { Badge } from './ui/badge';

interface ProductCardProps {
  product: Product;
}

export const ProductCard: React.FC<ProductCardProps> = ({
  product,
}) => {
  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0
    }).format(price);
  };

  return (
    <Card 
      className={`group cursor-pointer transition-all duration-300 hover:shadow-xl hover:-translate-y-1 border-2 border-transparent hover:border-border flex flex-col`}
      onClick={() => window.open(product.url, '_blank', 'noopener,noreferrer')}
    >
      <div className="p-0 flex-grow flex flex-col">
        <div className="relative overflow-hidden rounded-t-lg">
          <img
            src={product.image}
            alt={product.name}
            className="w-full aspect-square object-cover group-hover:scale-105 transition-transform duration-300"
          />
          <div className="absolute top-3 right-3">
            <Badge 
              variant="secondary" 
              className="bg-card/90 text-card-foreground font-semibold"
            >
              {Math.round(product.similarity * 100)}% match
            </Badge>
          </div>
        </div>
        
        <div className="p-4 space-y-3 flex-grow flex flex-col">
          <h3 className="font-bold text-base text-primary leading-tight group-hover:text-accent transition-colors truncate">
            {product.name}
          </h3>
          
          <div className="flex items-center justify-between text-sm">
            <span className="font-medium text-muted-foreground">{product.condition}</span>
            <span className="font-bold text-lg text-primary">{formatPrice(product.price)}</span>
          </div>

          <div className="space-y-2 pt-3 mt-auto border-t border-border/70">
            <div className="text-xs text-muted-foreground">
              <span className="font-semibold text-foreground/80">Location:</span> {product.location}
            </div>
            <div className="text-xs text-muted-foreground">
              <span className="font-semibold text-foreground/80">Shipping:</span> {formatPrice(product.shippingCost)}
            </div>
            <div className="text-xs text-muted-foreground">
              <span className="font-semibold text-foreground/80">Seller Rating:</span> {product.sellerRating}%
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
};
