
'use client';
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import ContactPage from '@/components/contact';

export default function Recommendations() {
  return (
    <main className="min-h-screen antialiased">
      <Navbar />
      <ContactPage />
      <Footer />
    </main>
  );
}