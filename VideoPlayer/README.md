# Next.js Video Player with ImageKit

A video player built with Next.js and ImageKit featuring adaptive streaming, subtitles, watermarks, and quality control.

## Features

- Adaptive Bitrate Streaming (HLS)
- Multi-language Subtitles (SRT, VTT, ASS)
- Dynamic Watermarking
- Quality Control (240p - 1080p)
- Auto-generated Thumbnails
- Video Library with JSON storage

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create `.env.local` from the example:
```bash
cp .env.local.example .env.local
```

3. Add your ImageKit credentials to `.env.local`:
```env
NEXT_PUBLIC_IMAGEKIT_URL_ENDPOINT=https://ik.imagekit.io/your_imagekit_id
IMAGEKIT_PUBLIC_KEY=your_public_key
IMAGEKIT_PRIVATE_KEY=your_private_key
```

4. Run the dev server:
```bash
npm run dev
```

5. Open http://localhost:3000

## ImageKit Features Used

- **HLS Streaming**: `video.mp4/ik-master.m3u8?tr=sr-240_360_480_720_1080`
- **Thumbnails**: `video.mp4/ik-thumbnail.jpg`
- **Subtitle Overlays**: `l-subtitles,i-subtitles.srt`
- **Image Watermarks**: `l-image,i-watermark.png`
- **Quality Control**: `tr=q-70`

## Resources

- [ImageKit Docs](https://imagekit.io/docs)
- [Adaptive Streaming](https://imagekit.io/docs/adaptive-bitrate-streaming)
- [Video Overlays](https://imagekit.io/docs/add-overlays-on-videos)
- [Next.js SDK](https://imagekit.io/docs/integration/nextjs)
