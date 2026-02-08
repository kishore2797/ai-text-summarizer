/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true
  },
  assetPrefix: process.env.NODE_ENV === 'production' ? '/ai-text-summarizer' : undefined,
  basePath: process.env.NODE_ENV === 'production' ? '/ai-text-summarizer' : undefined,
}

module.exports = nextConfig
