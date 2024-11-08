'use client';
import React, { useEffect, useState, useRef } from "react";
import { HoveredLink, Menu, MenuItem } from "./ui/navbar-menu";
import { account, databases } from '@/lib/appwrite'; 
import { Query } from 'appwrite';
import { cn } from "@/components/utils/cn";
import Link from "next/link";
import { useRouter } from "next/navigation";
import Image from "next/image";

function Navbar({ className }: { className?: string }) {
  const [active, setActive] = useState<string | null>(null);
  const [visible, setVisible] = useState(true);
  const [lastScrollY, setLastScrollY] = useState(0);
  const [isOpen, setIsOpen] = useState(false);
  const [currentUser, setCurrentUser] = useState<any>(null);
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const router = useRouter();
  const [bgColor, setBgColor] = useState("transparent");
  const profileRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (profileRef.current && !profileRef.current.contains(event.target)) {
        setIsProfileOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const session = await account.getSession('current');
        if (session) {
          const userDocs = await databases.listDocuments(
            process.env.NEXT_PUBLIC_APPWRITE_DATABASE_ID,
            process.env.NEXT_PUBLIC_APPWRITE_USERS_COLLECTION_ID,
            [Query.equal('userId', session.userId)]
          );

          if (userDocs.documents.length > 0) {
            const user = userDocs.documents[0];
            setCurrentUser({
              name: user.name,
              email: user.email,
              avatar: user.avatar
            });
          }
        }
      } catch (error) {
        console.error('Error fetching user data:', error);
        setCurrentUser(null);
      }
    };

    fetchUserData();
  }, []);

  const handleLogout = async () => {
    try {
      await account.deleteSessions();
      setCurrentUser(null);
      router.push("/");
      setIsProfileOpen(false);
    } catch (error) {
      console.error('Logout error:', error);
      setCurrentUser(null);
      setIsProfileOpen(false);
    }
  };

  const handleScroll = () => {
    const currentScrollY = window.scrollY;
    setVisible(currentScrollY <= lastScrollY || currentScrollY < 10);
    setBgColor(currentScrollY > 0 ? "bg-black/80" : "transparent");
    setLastScrollY(currentScrollY);
  };

  useEffect(() => {
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, [lastScrollY]);

  const NavLink = ({ href, children }) => (
    <div className="relative group py-2">
      <Link href={href} className="inline-block w-full">
        <span className="text-white transition-transform duration-200 group-hover:-translate-y-1">
          {children}
        </span>
        <span className="absolute bottom-0 left-1/2 w-0 h-0.5 bg-white/50 transition-all duration-300 origin-center group-hover:w-full group-hover:left-0"></span>
      </Link>
    </div>
  );

  return (
    <div 
      className={cn(
        "fixed top-0 right-0 w-full z-50 transition-all duration-300",
        visible ? "translate-y-0" : "-translate-y-full",
        bgColor,
        className
      )}
    >
      <Menu setActive={setActive}>
        <div className="flex justify-between items-center w-full px-8 py-4">
          <Link href="/">
            <img src="/logo.png" alt="Logo" className="h-12 transition-transform duration-200 hover:scale-105" />
          </Link>

          <div className="hidden md:flex items-center space-x-14">
            <div className="group">
              <Link href="/" className="relative inline-block py-2">
                <span className="text-white transition-transform duration-200 group-hover:-translate-y-1">
                  Home
                </span>
                <span className="absolute bottom-0 left-1/2 w-0 h-0.5 bg-white/50 transition-all duration-300 origin-center group-hover:w-full group-hover:left-0"></span>
              </Link>
            </div>
            <div className="group">
              <Link href="/about" className="relative inline-block py-2">
                <span className="text-white transition-transform duration-200 group-hover:-translate-y-1">
                  About
                </span>
                <span className="absolute bottom-0 left-1/2 w-0 h-0.5 bg-white/50 transition-all duration-300 origin-center group-hover:w-full group-hover:left-0"></span>
              </Link>
            </div>
            <div className="group">
              <Link href="/form" className="relative inline-block py-2">
                <span className="text-white transition-transform duration-200 group-hover:-translate-y-1">
                  Search
                </span>
                <span className="absolute bottom-0 left-1/2 w-0 h-0.5 bg-white/50 transition-all duration-300 origin-center group-hover:w-full group-hover:left-0"></span>
              </Link>
            </div>
            <div className="group">
              <Link href="/contact" className="relative inline-block py-2">
                <span className="text-white transition-transform duration-200 group-hover:-translate-y-1">
                  Contact Us
                </span>
                <span className="absolute bottom-0 left-1/2 w-0 h-0.5 bg-white/50 transition-all duration-300 origin-center group-hover:w-full group-hover:left-0"></span>
              </Link>
            </div>
          </div>

          <div className="hidden md:flex items-center" ref={profileRef}>
            {currentUser ? (
              <div className="relative profile-menu">
                <button
                  onClick={() => setIsProfileOpen(!isProfileOpen)}
                  className="flex items-center space-x-3 focus:outline-none transition-transform duration-200 hover:scale-105"
                >
                  {currentUser.avatar ? (
                    <Image
                      src={currentUser.avatar}
                      alt="Avatar"
                      width={40}
                      height={40}
                      className="rounded-full border-2 border-white"
                    />
                  ) : (
                    <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white border-2 border-white text-lg">
                      {currentUser.name[0].toUpperCase()}
                    </div>
                  )}
                  <span className="text-white">{currentUser.name}</span>
                </button>

                {isProfileOpen && (
                  <div className="absolute right-0 mt-2 w-48 bg-black/80 backdrop-blur-sm rounded-lg shadow-lg py-1 border border-white/10">
                    <Link href="/dashboard">
                      <div className="relative group px-4 py-2 hover:bg-white/10">
                        <span className="block text-white transition-transform duration-200 group-hover:-translate-y-1">
                          Dashboard
                        </span>
                      </div>
                    </Link>
                    <div className="border-t border-white/10 my-1"></div>
                    <button
                      onClick={handleLogout}
                      className="relative group w-full text-left px-4 py-2 hover:bg-white/10"
                    >
                      <span className="block text-white transition-transform duration-200 group-hover:-translate-y-1">
                        Sign out
                      </span>
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <div className="group">
                <Link href="/auth" className="relative inline-block py-2">
                  <span className="text-white transition-transform duration-200 group-hover:-translate-y-1">
                    Login
                  </span>
                  <span className="absolute bottom-0 left-1/2 w-0 h-0.5 bg-white/50 transition-all duration-300 origin-center group-hover:w-full group-hover:left-0"></span>
                </Link>
              </div>
            )}
          </div>

          <button onClick={() => setIsOpen(!isOpen)} className="md:hidden text-white">
            <svg className="w-6 h-6" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" viewBox="0 0 24 24" stroke="currentColor">
              {isOpen ? (
                <path d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>

        <div className={`md:hidden absolute top-full left-0 w-full bg-black/90 backdrop-blur-sm transform transition-transform duration-300 ${
          isOpen ? "translate-x-0" : "-translate-x-full"
        }`}>
          {currentUser && (
            <>
              <div className="px-8 py-4 flex items-center justify-center space-x-3">
                {currentUser.avatar ? (
                  <Image
                    src={currentUser.avatar}
                    alt="Avatar"
                    width={48}
                    height={48}
                    className="rounded-full border-2 border-white"
                  />
                ) : (
                  <div className="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center text-white border-2 border-white text-xl">
                    {currentUser.name[0].toUpperCase()}
                  </div>
                )}
                <span className="text-white font-medium">{currentUser.name}</span>
              </div>
              <div className="border-t border-white/10"></div>
            </>
          )}
          
          <div className="px-8 py-4 space-y-4 flex flex-col items-center">
            <Link href="/" className="relative group py-2 w-full text-center">
              <span className="inline-block text-white transition-transform duration-200 group-hover:-translate-y-1">
                Home
              </span>
              <span className="absolute bottom-0 left-1/2 w-0 h-0.5 bg-white/50 transition-all duration-300 origin-center group-hover:w-full group-hover:left-0"></span>
            </Link>
            <Link href="/about" className="relative group py-2 w-full text-center">
              <span className="inline-block text-white transition-transform duration-200 group-hover:-translate-y-1">
                About
              </span>
              <span className="absolute bottom-0 left-1/2 w-0 h-0.5 bg-white/50 transition-all duration-300 origin-center group-hover:w-full group-hover:left-0"></span>
            </Link>
            <Link href="/form" className="relative group py-2 w-full text-center">
              <span className="inline-block text-white transition-transform duration-200 group-hover:-translate-y-1">
                Search
              </span>
              <span className="absolute bottom-0 left-1/2 w-0 h-0.5 bg-white/50 transition-all duration-300 origin-center group-hover:w-full group-hover:left-0"></span>
            </Link>
            <Link href="/contact" className="relative group py-2 w-full text-center">
              <span className="inline-block text-white transition-transform duration-200 group-hover:-translate-y-1">
                Contact Us
              </span>
              <span className="absolute bottom-0 left-1/2 w-0 h-0.5 bg-white/50 transition-all duration-300 origin-center group-hover:w-full group-hover:left-0"></span>
            </Link>
          </div>

          {currentUser && (
            <>
              <div className="border-t border-white/10"></div>
              <div className="px-8 py-4 space-y-4 flex flex-col items-center">
                <Link href="/dashboard" className="relative group py-2 w-full text-center">
                  <span className="inline-block text-white transition-transform duration-200 group-hover:-translate-y-1">
                    Dashboard
                  </span>
                  <span className="absolute bottom-0 left-1/2 w-0 h-0.5 bg-white/50 transition-all duration-300 origin-center group-hover:w-full group-hover:left-0"></span>
                </Link>
                <button
                  onClick={handleLogout}
                  className="relative group py-2 w-full text-center"
                >
                  <span className="inline-block text-white transition-transform duration-200 group-hover:-translate-y-1">
                    Sign out
                  </span>
                  <span className="absolute bottom-0 left-1/2 w-0 h-0.5 bg-white/50 transition-all duration-300 origin-center group-hover:w-full group-hover:left-0"></span>
                </button>
              </div>
            </>
          )}
        </div>
      </Menu>
    </div>
  );
}

export default Navbar;