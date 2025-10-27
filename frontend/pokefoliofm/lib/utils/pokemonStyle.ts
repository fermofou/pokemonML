// utils/pokemonStyleMap.ts
export const typeEffects: Record<string, { colors: string[]; effect: string }> =
  {
    Fire: {
      colors: ["#ff5f3d", "#ffb347", "#ffcc70"],
      effect: "fire",
    },
    Water: {
      colors: ["#3d9eff", "#74c2ff", "#a6d9ff"],
      effect: "bubbles",
    },
    Grass: {
      colors: ["#5eff77", "#4ed66a", "#b8ffb2"],
      effect: "leaves",
    },
    Electric: {
      colors: ["#fff700", "#ffeb7a", "#ffd500"],
      effect: "thunder",
    },
    Rock: {
      colors: ["#b39b7a", "#d0c6a1", "#897b64"],
      effect: "rocks",
    },
    Flying: {
      colors: ["#a1e3ff", "#d3f0ff", "#ffffff"],
      effect: "wind",
    },
    Poison: {
      colors: ["#a060c9", "#d28dfc", "#e0aaff"],
      effect: "mist",
    },
    Ice: {
      colors: ["#b3e5fc", "#e1f5fe", "#ffffff"],
      effect: "snow",
    },
    Psychic: {
      colors: ["#ff80ab", "#ea80fc", "#b388ff"],
      effect: "aura",
    },
    Dark: {
      colors: ["#333333", "#555555", "#000000"],
      effect: "darkness",
    },
    Fairy: {
      colors: ["#ffb6c1", "#ffcce7", "#fff0f5"],
      effect: "sparkle",
    },
    Ground: {
      colors: ["#e0c68a", "#b99867", "#7a6043"],
      effect: "dust",
    },
    Fighting: {
      colors: ["#ff7043", "#e64a19", "#bf360c"],
      effect: "punch",
    },
    Ghost: {
      colors: ["#7b62a3", "#a18fd0", "#c4b7f0"],
      effect: "ghost",
    },
    Steel: {
      colors: ["#b0bec5", "#cfd8dc", "#eceff1"],
      effect: "metal",
    },
    Dragon: {
      colors: ["#7038f8", "#a890f0", "#c6afff"],
      effect: "flame",
    },
    Normal: {
      colors: ["#c6c6a7", "#e0e0c0", "#f5f5dc"],
      effect: "none",
    },
  };
