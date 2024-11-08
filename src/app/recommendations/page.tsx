// app/recommendations/page.tsx
import RecommendationsPage from '@/components/RecommendationsPage';
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

export default function Recommendations() {
  return (
    <main className="min-h-screen antialiased">
      <Navbar />
      <RecommendationsPage />
      <Footer />
    </main>
  );
}