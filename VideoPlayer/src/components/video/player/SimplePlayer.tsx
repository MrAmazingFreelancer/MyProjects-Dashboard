"use client";

import { createPlayer } from "@videojs/react";
import { VideoSkin, Video, videoFeatures } from "@videojs/react/video";
import "@videojs/react/video/skin.css";
import { Video as VideoType } from "@/types/video";

interface SimplePlayerProps {
  video: VideoType;
  urlEndpoint: string;
}

const Player = createPlayer({ features: videoFeatures });

export default function SimplePlayer({ video, urlEndpoint }: SimplePlayerProps) {
  const src = `${urlEndpoint}${video.filePath}`;
  const poster = video.thumbnailPath
    ? `${urlEndpoint}${video.thumbnailPath}`
    : `${urlEndpoint}${video.filePath}/ik-thumbnail.jpg`;

  return (
    <div className="simple-player">
      <Player.Provider>
        <VideoSkin poster={poster}>
          <Video src={src} playsInline />
        </VideoSkin>
      </Player.Provider>
    </div>
  );
}

