'use client';

import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import AboutUs from "@/components/about";

export default function Dashboard() {
  return (
    <main className="min-h-screen antialiased">
      <Navbar />
      <AboutUs />
      <Footer />
    </main>
  );
}