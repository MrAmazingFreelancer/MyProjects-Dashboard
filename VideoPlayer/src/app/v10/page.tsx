export default function V10LabPage() {
  return (
    <div className="page-shell">
      <section className="hero-panel">
        <div className="hero-copy">
          <span className="hero-kicker">v10 exploration</span>
          <h1 className="page-title">v10 Lab</h1>
          <p className="hero-description">
            This area is for trying new player ideas, controls, and visual patterns before they
            move into the main 7ink VideoPlayer experience.
          </p>
          <div className="hero-actions">
            <a href="/VideoPlayer" className="hero-primary-action">
              Back to VideoPlayer
            </a>
            <a href="https://videojs.org/" className="hero-secondary-action" target="_blank" rel="noreferrer">
              Open Video.js docs
            </a>
          </div>
        </div>

        <div className="hero-metrics">
          <div className="metric-card">
            <span className="metric-label">Status</span>
            <strong className="metric-value">Local Lab</strong>
          </div>
          <div className="metric-card">
            <span className="metric-label">Purpose</span>
            <strong className="metric-value metric-value--small">
              Prototype before production
            </strong>
          </div>
          <div className="metric-card">
            <span className="metric-label">Next</span>
            <strong className="metric-value metric-value--small">
              Share design ideas and iterate
            </strong>
          </div>
        </div>
      </section>
    </div>
  );
}
