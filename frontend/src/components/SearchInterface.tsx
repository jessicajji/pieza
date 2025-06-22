
import React, { useState } from 'react';
import { Search, Sparkles, RotateCcw, ChevronDown, ChevronUp } from 'lucide-react';
import { Button } from './ui/button';

interface SearchInterfaceProps {
  onSearch: (prompt: string) => void;
  onRefine: (prompt: string) => void;
  onStartOver: () => void;
  isSearching: boolean;
  hasResults: boolean;
  searchHistory: string[];
}

export const SearchInterface: React.FC<SearchInterfaceProps> = ({
  onSearch,
  onRefine,
  onStartOver,
  isSearching,
  hasResults,
  searchHistory,
}) => {
  const [prompt, setPrompt] = useState('');
  const [isHistoryVisible, setIsHistoryVisible] = useState(false);

  const handleAction = () => {
    if (prompt.trim() && !isSearching) {
      if (hasResults) {
        onRefine(prompt.trim());
      } else {
        onSearch(prompt.trim());
      }
      setPrompt('');
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    handleAction();
  };
  
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleAction();
    }
  };

  const quickRefinements = [
    "Make it more modern",
    "I prefer darker colors",
    "Something more affordable",
    "Larger dimensions",
    "Different material"
  ];
  
  const examplePrompts = [
    "A curved velvet sofa with wooden legs for my living room",
    "Modern dining chair with clean lines and comfortable padding",
    "Rustic coffee table with natural wood finish"
  ];

  return (
    <div className="transition-all duration-500 w-full h-full flex flex-col">
      <form onSubmit={handleSubmit} className="space-y-2">
        {hasResults && (
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-primary">
              Refine your search
            </h3>
            <Button variant="ghost" size="sm" onClick={() => { onStartOver(); setPrompt(''); }} className="text-xs text-muted-foreground gap-1 hover:text-primary">
              <RotateCcw className="w-3 h-3" />
              Start Over
            </Button>
          </div>
        )}
        <div className="relative">
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={1}
            placeholder={
              hasResults 
                ? "e.g., 'more curved edges' or 'higher seat height'"
                : "What are you looking for?"
            }
            className="w-full pl-4 pr-36 py-4 text-base border-2 border-border rounded-xl focus:border-accent focus:ring-0 resize-none bg-background/80 placeholder-muted-foreground min-h-[60px] transition-all duration-200 flex items-center"
            disabled={isSearching}
          />
          <div className="absolute top-1/2 right-4 transform -translate-y-1/2">
            <Button
              type="submit"
              disabled={!prompt.trim() || isSearching}
              className="bg-accent hover:bg-accent/90 text-accent-foreground px-6 py-2 rounded-lg transition-all duration-200 disabled:opacity-50 h-auto"
            >
              {isSearching ? (
                <div className="flex items-center space-x-2">
                  <Sparkles className="w-4 h-4 animate-spin" />
                  <span>{hasResults ? "Refining..." : "Searching..."}</span>
                </div>
              ) : (
                <div className="flex items-center space-x-2">
                  <Search className="w-4 h-4" />
                  <span>{hasResults ? "Refine" : "Find furniture"}</span>
                </div>
              )}
            </Button>
          </div>
        </div>
      </form>

      {hasResults && (
        <div className="mt-4 space-y-4">
          <div>
            <p className="text-xs text-muted-foreground mb-2">Quick refinements:</p>
            <div className="flex gap-2 overflow-x-auto pb-2">
              {quickRefinements.map((quick, index) => (
                <button
                  key={index}
                  onClick={() => setPrompt(quick)}
                  className="text-xs px-3 py-1 bg-secondary border border-border rounded-full hover:border-accent hover:bg-accent/10 transition-colors whitespace-nowrap"
                  disabled={isSearching}
                >
                  {quick}
                </button>
              ))}
            </div>
          </div>

          {searchHistory.length > 1 && (
            <div className="space-y-2 pt-2 border-t border-border/50">
              <button className="flex items-center gap-1 text-xs text-muted-foreground font-medium hover:text-primary w-full" onClick={() => setIsHistoryVisible(prev => !prev)}>
                Search history
                {isHistoryVisible ? <ChevronUp className="w-3 h-3"/> : <ChevronDown className="w-3 h-3"/>}
              </button>
              {isHistoryVisible && (
                <div className="pt-2">
                  <div className="space-y-1">
                    {searchHistory.slice(-3).reverse().map((search, index) => (
                      <div key={index} className="text-xs text-muted-foreground bg-secondary/50 p-2 rounded">
                        "{search}"
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {!hasResults && (
        <div className="mt-8">
          <p className="text-sm font-medium text-secondary-foreground mb-4">Try these examples:</p>
          <div className="grid gap-3">
            {examplePrompts.map((example, index) => (
              <button
                key={index}
                onClick={() => setPrompt(example)}
                className="text-left p-4 rounded-lg bg-secondary hover:bg-secondary/80 transition-colors duration-200 text-secondary-foreground text-sm"
                disabled={isSearching}
              >
                "{example}"
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
