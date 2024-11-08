import React, { useState, useRef } from "react";
import { Search, Image, X } from "lucide-react";
import { useRouter } from "next/navigation";
import Preloader from "./ui/Preloader";
import { toast, Toast } from '@welcome-ui/toast';

const SearchSection = () => {
  const router = useRouter();
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedImage, setSelectedImage] = useState(null);
  const [isSearching, setIsSearching] = useState(false);
  const [showToast, setShowToast] = useState(false);
  const fileInputRef = useRef(null);

  const handleImageSearch = async (file) => {
    const allowedExtensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp'];
    const fileExtension = file.name.split('.').pop().toLowerCase();

    if (!allowedExtensions.includes(fileExtension)) {
      setShowToast(true);
      return;
    }

    setIsSearching(true);
    const formData = new FormData();
    formData.append('image', file);

    try {
      const response = await fetch(process.env.NEXT_PUBLIC_BACKEND_ANALYZE_URL!, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('Image search failed');
      
      const data = await response.json();
      sessionStorage.setItem('recommendations', JSON.stringify(data));
      router.push('/recommendations');
    } catch (error) {
      console.error('Image search error:', error);
    } finally {
      setIsSearching(false);
    }
  };

  const handleFileSelect = (file) => {
    setSelectedImage(file);
    handleImageSearch(file);
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;
  
    setIsSearching(true);
  
    try {
      const response = await fetch(process.env.NEXT_PUBLIC_BACKEND_EXTRACT_URL!, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: searchQuery }),
      });
  
      if (!response.ok) {
        throw new Error('Search failed');
      }
  
      const data = await response.json();
      sessionStorage.setItem('recommendations', JSON.stringify(data));
      router.push('/recommendations');
    } catch (error) {
      console.error('Search error:', error);
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <div className="relative">
      {isSearching && (
        <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-75 z-50">
          <Preloader />
        </div>
      )}
      {showToast && (
        <Toast
          variant="danger"
          onDismiss={() => setShowToast(false)}
          className="animate__animated animate__fadeInDown animate__faster"
        >
          <Toast.Title>Error</Toast.Title>
          <p>Please upload a valid image file (jpg, jpeg, png, gif, bmp).</p>
        </Toast>
      )}
      <div className="backdrop-blur-lg bg-[#1a1a1a] bg-opacity-90 p-5 rounded-xl shadow-2xl border border-gray-800">
        <form onSubmit={handleSearch}>
          <div className="relative">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-[#2a2a2a] text-white px-4 py-3 pr-24 rounded-lg border border-gray-700 focus:ring-2 focus:ring-green-400 focus:border-transparent transition-all duration-200 animate__animated animate__fadeInDown animate__faster"
              placeholder="Search recipes..."
            />
            <div className="absolute right-3 top-1/2 -translate-y-1/2 flex items-center space-x-2">
              <input
                ref={fileInputRef}
                type="file"
                accept="image/jpeg, image/png, image/gif, image/bmp"
                className="hidden"
                onChange={(e) => e.target.files && handleFileSelect(e.target.files[0])}
              />
              {selectedImage && (
                <button
                  type="button"
                  onClick={() => setSelectedImage(null)}
                  className="text-red-400 hover:text-red-300 p-1 animate__animated animate__fadeInRight animate__faster"
                >
                  <X className="w-4 h-4" />
                </button>
              )}
              <button
                type="button"
                onClick={() => fileInputRef.current?.click()}
                className={`text-gray-400 hover:text-green-400 transition-colors duration-200 p-1 ${
                  selectedImage ? 'text-green-400' : ''
                } animate__animated animate__fadeInRight animate__faster`}
              >
                <Image className="w-5 h-5" />
              </button>
              <button
                type="submit"
                disabled={isSearching}
                className="text-green-400 hover:text-green-300 transition-colors duration-200 disabled:opacity-50 p-1 animate__animated animate__fadeInRight animate__faster"
              >
                <Search className="w-5 h-5" />
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SearchSection;