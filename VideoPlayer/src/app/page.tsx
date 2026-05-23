import VideoLibrary from "@/components/video/VideoLibrary";
import { getAllVideos } from "@/lib/video-storage";

export const dynamic = "force-dynamic";

export default function HomePage() {
  const videos = getAllVideos();
  const latestVideo = videos[0];

  return (
    <div className="page-shell">
      <section className="hero-panel">
        <div className="hero-copy">
          <span className="hero-kicker">7ink streaming workspace</span>
          <h1 className="page-title">Video that feels curated, not dumped in a folder.</h1>
          <p className="hero-description">
            Build a clean internal media library for demos, product walkthroughs, client previews,
            and future 7ink video experiences.
          </p>
          <div className="hero-actions">
            <a href="/upload" className="hero-primary-action">
              Upload a video
            </a>
            <a href="/VideoPlayer" className="hero-secondary-action">
              Open library view
            </a>
          </div>
        </div>
        <div className="hero-metrics">
          <div className="metric-card">
            <span className="metric-label">Videos</span>
            <strong className="metric-value">{videos.length}</strong>
          </div>
          <div className="metric-card">
            <span className="metric-label">Latest</span>
            <strong className="metric-value metric-value--small">
              {latestVideo ? latestVideo.title : "Ready for first upload"}
            </strong>
          </div>
          <div className="metric-card">
            <span className="metric-label">Mode</span>
            <strong className="metric-value">7ink local</strong>
          </div>
        </div>
      </section>

      <section className="library-section">
        <div className="section-heading">
          <div>
            <span className="section-kicker">Library</span>
            <h2 className="section-title">Current catalogue</h2>
          </div>
          <p className="section-summary">
            Browse what is already uploaded, open an individual watch page, and use this as the
            base for the next design pass.
          </p>
        </div>
        <VideoLibrary videos={videos} />
      </section>
    </div>
  );
}
