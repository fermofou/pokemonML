import React from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Sparkles, TrendingUp, Camera, Shield } from "lucide-react";
import { getPokemonOfDay } from "@/lib/utils/getPokemonToday";
import { colorThemeMap } from "@/lib/utils/colorTheme";
import { getInvestmentMessage } from "@/lib/utils/message";
import Header from "@/components/Header";
export default async function LandingPage() {
  const pokemonOfDay = await getPokemonOfDay();
  const colorTheme = colorThemeMap[pokemonOfDay.color];
  const investmentMessage = getInvestmentMessage();

  return (
    <div
      className="min-h-screen bg-background"
      style={{
        "--pokemon-primary": colorTheme.primary,
        "--pokemon-secondary": colorTheme.secondary,
        "--pokemon-accent": colorTheme.accent,
      }}
    >
      {/* Header */}
      <Header pokemonOfDay={pokemonOfDay} colorTheme={colorTheme} />

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 md:py-32">
        <div className="max-w-4xl mx-auto text-center relative">
          <div className="absolute -top-10 right-0 md:right-10 opacity-20 pointer-events-none">
            <img
              src={`${pokemonOfDay.normal_url}`}
              alt={pokemonOfDay.name}
              className="w-32 h-32 md:w-48 md:h-48 animate-float"
            />
          </div>

          <h1
            className="text-5xl md:text-7xl font-bold text-balance mb-6"
            style={{
              background: `linear-gradient(135deg, ${colorTheme.primary}, ${colorTheme.secondary}, ${colorTheme.accent})`,
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
              backgroundClip: "text",
            }}
          >
            {investmentMessage}
          </h1>
          <p className="text-xl md:text-2xl text-muted-foreground text-balance mb-8 leading-relaxed">
            Track your Pokemon cards, watch their value soar, and pretend you
            planned this all along
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/dashboard">
              <Button
                size="lg"
                className="text-lg px-8"
                style={{
                  backgroundColor: colorTheme.primary,
                  color: "white",
                }}
              >
                Start "Investing"
              </Button>
            </Link>
            <Button
              size="lg"
              variant="outline"
              className="text-lg px-8 bg-transparent"
            >
              Learn More
            </Button>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="container mx-auto px-4 py-20">
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card className="p-6 hover:shadow-lg transition-shadow">
            <div
              className="w-12 h-12 rounded-lg flex items-center justify-center mb-4"
              style={{ backgroundColor: `${colorTheme.primary}20` }}
            >
              <Sparkles
                className="w-6 h-6"
                style={{ color: colorTheme.primary }}
              />
            </div>
            <h3 className="text-xl font-semibold mb-2 text-card-foreground">
              CardsDex
            </h3>
            <p className="text-muted-foreground leading-relaxed">
              View and organize your entire Pokemon card collection in one
              beautiful interface
            </p>
          </Card>

          <Card className="p-6 hover:shadow-lg transition-shadow">
            <div
              className="w-12 h-12 rounded-lg flex items-center justify-center mb-4"
              style={{ backgroundColor: `${colorTheme.secondary}20` }}
            >
              <TrendingUp
                className="w-6 h-6"
                style={{ color: colorTheme.secondary }}
              />
            </div>
            <h3 className="text-xl font-semibold mb-2 text-card-foreground">
              Price Tracking
            </h3>
            <p className="text-muted-foreground leading-relaxed">
              See real-time market values and convince yourself it was worth it
            </p>
          </Card>

          <Card className="p-6 hover:shadow-lg transition-shadow">
            <div
              className="w-12 h-12 rounded-lg flex items-center justify-center mb-4"
              style={{ backgroundColor: `${colorTheme.accent}20` }}
            >
              <Camera
                className="w-6 h-6"
                style={{ color: colorTheme.accent }}
              />
            </div>
            <h3 className="text-xl font-semibold mb-2 text-card-foreground">
              Smart Scanner
            </h3>
            <p className="text-muted-foreground leading-relaxed">
              Use your camera to instantly identify and add cards to your
              collection
            </p>
          </Card>

          <Card className="p-6 hover:shadow-lg transition-shadow">
            <div
              className="w-12 h-12 rounded-lg flex items-center justify-center mb-4"
              style={{ backgroundColor: `${colorTheme.primary}20` }}
            >
              <Shield
                className="w-6 h-6"
                style={{ color: colorTheme.primary }}
              />
            </div>
            <h3 className="text-xl font-semibold mb-2 text-card-foreground">
              Secure Storage
            </h3>
            <p className="text-muted-foreground leading-relaxed">
              Your collection data is safely stored and accessible from any
              device
            </p>
          </Card>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-4 py-20">
        <Card
          className="p-12 border-2"
          style={{
            background: `linear-gradient(135deg, ${colorTheme.primary}10, ${colorTheme.secondary}10, ${colorTheme.accent}10)`,
          }}
        >
          <div className="max-w-2xl mx-auto text-center">
            <h2 className="text-4xl font-bold mb-4 text-balance text-card-foreground">
              Ready to justify your spending?
            </h2>
            <p className="text-xl text-muted-foreground mb-8 text-balance leading-relaxed">
              Join thousands of collectors who are definitely making smart
              financial decisions
            </p>
            <Link href="/dashboard">
              <Button
                size="lg"
                className="text-lg px-8"
                style={{
                  backgroundColor: colorTheme.primary,
                  color: "white",
                }}
              >
                Start Your "Portfolio"
              </Button>
            </Link>
          </div>
        </Card>
      </section>

      {/* Footer */}
      <footer className="border-t border-border mt-20">
        <div className="container mx-auto px-4 py-8">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-2">
              <div
                className="w-8 h-8 rounded-lg flex items-center justify-center"
                style={{ backgroundColor: colorTheme.primary }}
              >
                <Sparkles className="w-5 h-5 text-white" />
              </div>
              <span className="font-semibold text-foreground">
                pokeFolio.fm
              </span>
            </div>
            <p className="text-sm text-muted-foreground">
              © 2025 pokeFolio.fm. Track your collection with confidence.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
