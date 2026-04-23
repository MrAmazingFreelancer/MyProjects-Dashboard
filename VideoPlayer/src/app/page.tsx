import VideoLibrary from "@/components/video/VideoLibrary";
import { getAllVideos } from "@/lib/video-storage";

export const dynamic = "force-dynamic";

export default function HomePage() {
  const videos = getAllVideos();

  return (
    <div>
      <h1 className="page-title">Video Library</h1>
      <VideoLibrary videos={videos} />
    </div>
  );
}
