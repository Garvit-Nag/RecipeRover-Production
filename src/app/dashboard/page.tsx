'use client';

import DashboardPage from '@/components/DashboardPage';
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

export default function Dashboard() {
  return (
    <main className="min-h-screen antialiased">
      <Navbar />
      <DashboardPage />
      <Footer />
    </main>
  );
}