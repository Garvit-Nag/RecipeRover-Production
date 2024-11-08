"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Preloader from "../../components/ui/Preloader";

const RecipeRecommendationSearch: React.FC = () => {
  const router = useRouter();
  const [searchQuery, setSearchQuery] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    
    setIsLoading(true);  // Show preloader

    try {
      const response = await fetch(process.env.NEXT_PUBLIC_BACKEND_EXTRACT_URL!, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: searchQuery }),
      });

      if (!response.ok) {
        throw new Error("Failed to submit search");
      }

      const recommendations = await response.json();
      sessionStorage.setItem("recommendations", JSON.stringify(recommendations));
      router.push("/recommendations");
    } catch (error) {
      console.error("Error submitting search:", error);
      setIsLoading(false);  // Hide preloader if there's an error
    }
  };

  return (
    <>
      {isLoading && <Preloader />}
      <div style={{ background: "#0f172a", padding: "20px" }}>
        <h3
          className="text-base text-teal-400 font-semibold tracking wide uppercase"
          style={{ textAlign: "center" }}
        >
          Recipe Search
        </h3>
        <p
          className="mt-2 mb-10 text-3xl leading-8 font-extrabold tracking-tight text-white sm:text-4xl my-5"
          style={{ textAlign: "center" }}
        >
          Find Your Recipe 🍵
        </p>
        <form
          onSubmit={handleSearch}
          className="space-y-6 p-6 rounded-lg shadow-md max-w-lg mx-auto bg-neutral-900"
          style={{ color: "white", border: "2px solid white" }}
        >
          <div>
            <label htmlFor="search" className="block text-sm text-gray-300">
              Search for a recipe
            </label>
            <input
              id="search"
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Enter keywords, ingredients, etc."
              className="mt-2 block w-full border border-gray-500 text-white py-2 px-3 rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-500"
              style={{ background: "#1f2937", borderRadius: "4px", height: "38px" }}
            />
          </div>
          <div className="flex justify-center">
            <button
              type="submit"
              className="w-80 py-2 text-white bg-indigo-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 hover:bg-indigo-500 mx-auto"
            >
              Search
            </button>
          </div>
        </form>
      </div>
    </>
  );
};

export default RecipeRecommendationSearch;