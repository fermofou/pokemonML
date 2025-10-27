import React from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Sparkles } from "lucide-react";

const Header = ({ pokemonOfDay, colorTheme }) => {
  return (
    <div>
      <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div
              className="w-10 h-10 rounded-lg flex items-center justify-center"
              style={{ backgroundColor: colorTheme.primary }}
            >
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <span className="text-xl font-bold text-foreground">
              pokeFolio.fm
            </span>
          </div>
          <div className="hidden md:flex items-center gap-3">
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-muted">
              <img
                src={`${pokemonOfDay.normal_url}`}
                alt={pokemonOfDay.name}
                className="w-6 h-6"
              />
              <span className="text-sm font-medium">
                Today: {pokemonOfDay.name}
              </span>
            </div>
            <Link href="/dashboard">
              <Button
                style={{
                  backgroundColor: colorTheme.primary,
                  color: "white",
                }}
              >
                Get Started
              </Button>
            </Link>
          </div>
          <Link href="/dashboard" className="md:hidden">
            <Button
              style={{
                backgroundColor: colorTheme.primary,
                color: "white",
              }}
            >
              Get Started
            </Button>
          </Link>
        </div>
      </header>
    </div>
  );
};

export default Header;
