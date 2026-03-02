/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  
  // Environment variables
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
  },
  
  // Image optimization (if needed)
  images: {
    domains: ['localhost'],
  },
  
  // Webpack config
  webpack: (config) => {
    // Add custom webpack configuration here
    return config;
  },
};

module.exports = nextConfig;
