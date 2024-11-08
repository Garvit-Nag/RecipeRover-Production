import React from 'react';
import { Github, Linkedin, Mail, MapPin } from 'lucide-react';

const Footer = () => {
  const developers = [
    {
      name: "Garvit Nag",
      github: "https://github.com/Garvit-Nag",
      linkedin: "https://www.linkedin.com/in/garvit-nag/",
      email: "garvit1505@gmail.com"
    },
    {
      name: "Gurmehar Singh",
      github: "https://github.com/GURSV",
      linkedin: "https://www.linkedin.com/in/gurmehar-singh-b5864a23a/",
      email: "gurmeharsinghv@gmail.com"
    }
  ];

  return (
    <footer className="bg-black text-gray-400">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-12">
          {/* About Section */}
          <div>
            <h3 className="text-white text-lg font-semibold mb-4">About Us</h3>
            <p className="text-gray-400 hover:text-gray-300 transition-colors duration-200">
              We believe in making cooking accessible, enjoyable, and creative for everyone through 
              the power of AI and community.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-white text-lg font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              {[
                { name: 'Home', path: '/' },
                { name: 'About', path: '/about' },
                { name: 'Search Recipes', path: '/form' },
                { name: 'Contact', path: '/contact' }
              ].map((link) => (
                <li key={link.name}>
                  <a
                    href={link.path}
                    className="hover:text-white transition-colors duration-200 block transform hover:translate-x-1"
                  >
                    {link.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Features */}
          <div>
            <h3 className="text-white text-lg font-semibold mb-4">Features</h3>
            <ul className="space-y-2">
              <li className="hover:text-white transition-colors duration-200">AI-Powered Search</li>
              <li className="hover:text-white transition-colors duration-200">Image Recognition</li>
              <li className="hover:text-white transition-colors duration-200">Personalized Experience</li>
              <li className="hover:text-white transition-colors duration-200">Recipe Collections</li>
            </ul>
          </div>

          {/* Developers */}
          <div>
            <h3 className="text-white text-lg font-semibold mb-4">Our Developers</h3>
            <div className="space-y-4">
              {developers.map((dev) => (
                <div key={dev.name} className="space-y-2">
                  <p className="text-white">{dev.name}</p>
                  <div className="flex gap-3">
                    <a
                      href={dev.github}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="hover:text-white transition-colors duration-200"
                    >
                      <Github className="w-5 h-5" />
                    </a>
                    <a
                      href={dev.linkedin}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="hover:text-white transition-colors duration-200"
                    >
                      <Linkedin className="w-5 h-5" />
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Contact Info */}
          <div>
            <h3 className="text-white text-lg font-semibold mb-4">Contact Us</h3>
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <MapPin className="w-5 h-5 flex-shrink-0" />
                <p>Mohali 160055, Punjab, India</p>
              </div>
              <div className="flex flex-nowrap items-center gap-2">
                <Mail className="w-5 h-5 flex-shrink-0" />
                <a 
                  href="mailto:gurmeharsinghv@gmail.com"
                  className="hover:text-white transition-colors duration-200 break-all"
                >
                  gurmeharsinghv@gmail.com
                </a>
              </div>
              <div className="flex flex-nowrap items-center gap-2">
                <Mail className="w-5 h-5 flex-shrink-0" />
                <a 
                  href="mailto:garvit1505@gmail.com"
                  className="hover:text-white transition-colors duration-200 break-all"
                >
                  garvit1505@gmail.com
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="border-t border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <p className="text-center text-sm">
            © {new Date().getFullYear()} RecipeRover. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;