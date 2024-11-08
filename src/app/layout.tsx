import type { Metadata } from "next";
import "./globals.css";  // No need to import Inter if not using it
import Head from 'next/head';  // Import the Head component

export const metadata: Metadata = {
  title: "Recipe Rover-Master the Recipe Art",
  description: "Cooked!",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <Head>
        <link rel="icon" href="/favicon.ico" />  {/* Link to the favicon */}
      </Head>
      <body>{children}</body>
    </html>
  );
}
