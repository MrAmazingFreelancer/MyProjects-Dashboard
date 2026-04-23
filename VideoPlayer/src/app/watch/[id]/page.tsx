import { notFound } from "next/navigation";
import { getVideoById } from "@/lib/video-storage";
import VideoPlayer from "@/components/video/VideoPlayer";
import Link from "next/link";
import "@/styles/watch.css";

interface Props {
  params: Promise<{ id: string }>;
}

export const dynamic = "force-dynamic";

export default async function WatchPage({ params }: Props) {
  const { id } = await params;
  const video = getVideoById(id);

  if (!video) {
    notFound();
  }

  return (
    <div>
      <Link href="/" className="back-link">
        ← Back to Library
      </Link>
      <div className="video-container">
        <VideoPlayer video={video} />
      </div>
      <h1 className="video-title">{video.title}</h1>
      {video.description && (
        <p className="video-description">{video.description}</p>
      )}
    </div>
  );
}
