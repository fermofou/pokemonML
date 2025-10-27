import "./globals.css";

export const metadata = {
  title: "pokefolio.fm",
  description: "A portfolio for bad entrepeneurs",
  icons: {
    icon: "/favicon.ico",
  },
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
