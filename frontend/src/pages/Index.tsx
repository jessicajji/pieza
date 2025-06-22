import React, { useState } from 'react';
import { ProductGrid } from '../components/ProductGrid';
import { ProductCard } from '../components/ProductCard';
import { Product } from '../types/product';
import { SearchInterface } from '../components/SearchInterface';
import { searchItems } from '../lib/api';
import { EbayItem } from '../types/ebay';

const Index = () => {
  const [searchResults, setSearchResults] = useState<Product[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [searchHistory, setSearchHistory] = useState<string[]>([]);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async (prompt: string) => {
    setIsSearching(true);
    setHasSearched(true);
    setSearchHistory(prev => [...prev, prompt]);
    
    try {
      const response = await searchItems(prompt);
      // Convert EbayItems to Products
      const products: Product[] = response.items.map(item => ({
        id: item.item_id,
        name: item.title,
        price: item.price,
        image: item.image_url,
        category: 'furniture', // You might want to extract this from the title
        similarity: 1.0, // The API doesn't provide similarity scores yet
        url: item.item_url,
        condition: item.condition,
        location: item.location,
        shippingCost: item.shipping_cost,
        sellerRating: item.seller_rating
      }));
      
      setSearchResults(products);
    } catch (error) {
      console.error('Search failed:', error);
      // You might want to show an error message to the user
    } finally {
      setIsSearching(false);
    }
  };

  const handleRefinement = async (refinement: string) => {
    setIsSearching(true);
    setHasSearched(true);
    setSearchHistory(prev => [...prev, refinement]);
    
    try {
      const response = await searchItems(refinement);
      // Convert EbayItems to Products
      const products: Product[] = response.items.map(item => ({
        id: item.item_id,
        name: item.title,
        price: item.price,
        image: item.image_url,
        category: 'furniture',
        similarity: 1.0,
        url: item.item_url,
        condition: item.condition,
        location: item.location,
        shippingCost: item.shipping_cost,
        sellerRating: item.seller_rating
      }));
      
      setSearchResults(products);
    } catch (error) {
      console.error('Refinement failed:', error);
    } finally {
      setIsSearching(false);
    }
  };

  const handleStartOver = () => {
    setSearchResults([]);
    setSearchHistory([]);
    setHasSearched(false);
  };

  const hasResults = searchResults.length > 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-secondary to-background w-full">
      <header className="sticky top-0 z-50 bg-muted/80 backdrop-blur-sm py-4">
        <div className="container mx-auto px-4">
          <div className="flex items-center">
            <button
              onClick={handleStartOver}
              className="flex items-center gap-1 focus:outline-none"
            >
              <img src="/lovable-uploads/0ef1edb3-16b0-460e-8b53-e7460dd0a7e5.png" alt="Pieza Logo" className="h-12 w-auto" />
              <span
                className="font-bold tracking-tight text-3xl text-primary"
              >
                Pieza
              </span>
            </button>
          </div>
        </div>
      </header>

      <div className={`container mx-auto px-4 pb-8 transition-all duration-500 ${hasResults ? 'pt-6' : 'pt-12'}`}>
        <div className="max-w-3xl mx-auto mb-12">
          {!hasResults && (
            <div className="text-center mb-12">
              <h1 className="text-5xl font-serif font-normal tracking-tight text-primary">Discover furniture that perfectly matches your vision</h1>
            </div>
          )}
          <SearchInterface
            onSearch={handleSearch}
            onRefine={handleRefinement}
            onStartOver={handleStartOver}
            isSearching={isSearching}
            hasResults={hasResults}
            searchHistory={searchHistory}
          />
        </div>

        {(isSearching || hasResults || hasSearched) && (
          <div className="mb-12">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-semibold text-primary">
                {hasResults ? `Top matches (${searchResults.length})` : hasSearched && !isSearching ? 'No matches found' : ''}
              </h2>
              {hasResults && (
                <div className="text-sm text-muted-foreground">
                  Sorted by visual similarity
                </div>
              )}
            </div>
            {hasSearched && !isSearching && searchResults.length === 0 && (
              <div className="text-center py-12">
                <p className="text-lg text-muted-foreground mb-4">
                  No furniture matches your search criteria.
                </p>
                <p className="text-sm text-muted-foreground">
                  Try adjusting your search terms or try a different description.
                </p>
              </div>
            )}
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
              {searchResults.map((product) => (
                <ProductCard
                  key={product.id}
                  product={product}
                />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Index;
