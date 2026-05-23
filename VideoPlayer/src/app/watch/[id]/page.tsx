import { getVideoById } from "@/lib/video-storage";
import VideoPlayer from "@/components/video/VideoPlayer";
import Link from "next/link";
import { Video } from "@/types/video";
import "@/styles/watch.css";

interface Props {
  params: Promise<{ id: string }>;
  searchParams: Promise<{
    title?: string;
    description?: string;
    filePath?: string;
    fileName?: string;
    thumbnailPath?: string;
  }>;
}

export const dynamic = "force-dynamic";

export default async function WatchPage({ params, searchParams }: Props) {
  const { id } = await params;
  const query = await searchParams;
  let video = getVideoById(id);

  if (!video && query.filePath) {
    video = {
      id,
      title: query.title || "Uploaded Video",
      description: query.description || "",
      filePath: query.filePath,
      fileName: query.fileName || "uploaded-video",
      thumbnailPath: query.thumbnailPath || "",
      createdAt: new Date().toISOString(),
      subtitles: [],
    } as Video;
  }

  if (!video) {
    return (
      <div>
        <Link href="/VideoPlayer" className="back-link">
          ← Back to Library
        </Link>
        <div className="video-container">
          <div
            style={{
              padding: "12px 14px",
              borderRadius: "12px",
              border: "1px solid rgba(239, 68, 68, 0.45)",
              background: "rgba(127, 29, 29, 0.22)",
              color: "#fecaca",
              fontWeight: 600,
            }}
          >
            Video not found for this link. Open it from the Library again to
            refresh metadata.
          </div>
        </div>
      </div>
    );
  }

  return (
    <div>
      <Link href="/VideoPlayer" className="back-link">
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
