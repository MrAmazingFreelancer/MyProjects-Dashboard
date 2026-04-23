"use client";

import { Video } from "@/types/video";
import VideoThumbnail from "./VideoThumbnail";
import Link from "next/link";
import "@/styles/library.css";

interface Props {
  videos: Video[];
}

export default function VideoLibrary({ videos }: Props) {
  const urlEndpoint = process.env.NEXT_PUBLIC_IMAGEKIT_URL_ENDPOINT || "";

  if (videos.length === 0) {
    return (
      <div className="library-empty">
        <p className="library-empty-text">No videos yet</p>
        <Link href="/upload" className="library-upload-button">
          Upload Video
        </Link>
      </div>
    );
  }

  return (
    <div className="library-grid">
      {videos.map((video) => (
        <VideoThumbnail key={video.id} video={video} urlEndpoint={urlEndpoint} />
      ))}
    </div>
  );
}
