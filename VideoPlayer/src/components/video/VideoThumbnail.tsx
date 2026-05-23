"use client";

import { Image } from "@imagekit/next";
import { Video } from "@/types/video";
import Link from "next/link";
import "@/styles/thumbnail.css";

interface Props {
  video: Video;
  urlEndpoint: string;
}

export default function VideoThumbnail({ video, urlEndpoint }: Props) {
  const watchHref = {
    pathname: `/watch/${video.id}`,
    query: {
      title: video.title,
      description: video.description,
      filePath: video.filePath,
      fileName: video.fileName,
      thumbnailPath: video.thumbnailPath || "",
    },
  };

  return (
    <Link href={watchHref}>
      <div className="thumbnail-card">
        <Image
          urlEndpoint={urlEndpoint}
          src={video.thumbnailPath || `${video.filePath}/ik-thumbnail.jpg`}
          alt={video.title}
          width={320}
          height={180}
          className="thumbnail-image"
          transformation={[{ width: 320, height: 180 }]}
        />
        <div className="thumbnail-info">
          <h3 className="thumbnail-title">{video.title}</h3>
          <p className="thumbnail-date">
            {new Date(video.createdAt).toISOString().split('T')[0]}
          </p>
        </div>
      </div>
    </Link>
  );
}
