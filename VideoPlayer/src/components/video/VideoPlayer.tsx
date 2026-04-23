"use client";

import { Video } from "@/types/video";
import SimplePlayer from "./player/SimplePlayer";

interface VideoPlayerProps {
  video: Video;
}

export default function VideoPlayer({ video }: VideoPlayerProps) {
  const urlEndpoint = process.env.NEXT_PUBLIC_IMAGEKIT_URL_ENDPOINT || "";

  return (
    <div className="video-player-wrapper">
      <SimplePlayer video={video} urlEndpoint={urlEndpoint} />
    </div>
  );
}
