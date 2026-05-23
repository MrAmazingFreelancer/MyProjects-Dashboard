"use client";

import { useEffect, useMemo, useState } from "react";
import { Video as VideoType } from "@/types/video";

interface SimplePlayerProps {
  video: VideoType;
  urlEndpoint: string;
}

function normalizeEndpoint(endpoint: string): string {
  return endpoint.endsWith("/") ? endpoint.slice(0, -1) : endpoint;
}

function getEndpointCandidates(urlEndpoint: string): string[] {
  const preferred = normalizeEndpoint(
    urlEndpoint || "https://ik.imagekit.io/mramazing/VPData"
  );
  const alternate = preferred.includes("/VPData")
    ? preferred.replace(/\/VPData$/, "")
    : `${preferred}/VPData`;

  return Array.from(new Set([preferred, normalizeEndpoint(alternate)]));
}

function toAbsoluteMediaUrl(urlEndpoint: string, filePath: string): string {
  if (/^https?:\/\//i.test(filePath)) {
    return filePath;
  }

  const base = normalizeEndpoint(urlEndpoint || "https://ik.imagekit.io/mramazing/VPData");
  const path = filePath.startsWith("/") ? filePath : `/${filePath}`;
  return `${base}${path}`;
}

export default function SimplePlayer({ video, urlEndpoint }: SimplePlayerProps) {
  const endpointCandidates = useMemo(
    () => getEndpointCandidates(urlEndpoint),
    [urlEndpoint]
  );

  const src = useMemo(() => {
    const primaryEndpoint = endpointCandidates[0] || urlEndpoint;
    return toAbsoluteMediaUrl(primaryEndpoint, video.filePath);
  }, [endpointCandidates, urlEndpoint, video.filePath]);

  const sourceCandidates = useMemo(() => {
    const path = video.filePath.startsWith("/") ? video.filePath : `/${video.filePath}`;
    const candidates: string[] = [];

    endpointCandidates.forEach((endpoint) => {
      const baseSrc = `${endpoint}${path}`;
      const sep = baseSrc.includes("?") ? "&" : "?";
      candidates.push(baseSrc);
      candidates.push(`${baseSrc}${sep}tr=f-mp4,vc-h264,ac-aac`);
      candidates.push(`${baseSrc}${sep}tr=f-webm,vc-vp9,ac-none`);
    });

    return Array.from(new Set(candidates));
  }, [endpointCandidates, video.filePath]);

  const [sourceIndex, setSourceIndex] = useState(0);
  const activeSrc = sourceCandidates[sourceIndex] || src;
  const poster = useMemo(() => {
    const primaryEndpoint = endpointCandidates[0] || urlEndpoint;
    if (video.thumbnailPath) {
      return toAbsoluteMediaUrl(primaryEndpoint, video.thumbnailPath);
    }
    return `${src}/ik-thumbnail.jpg`;
  }, [endpointCandidates, urlEndpoint, video.thumbnailPath, src]);

  const [sourceError, setSourceError] = useState<string | null>(null);

  // Reset state when src changes (adjusting state during render pattern)
  const [prevSrc, setPrevSrc] = useState(src);
  if (prevSrc !== src) {
    setPrevSrc(src);
    setSourceIndex(0);
    setSourceError(null);
  }

  useEffect(() => {
    let cancelled = false;

    async function checkSource() {
      try {
        const res = await fetch(activeSrc, { method: "HEAD" });
        if (!cancelled && !res.ok) {
          if (sourceIndex < sourceCandidates.length - 1) {
            setSourceIndex((current) =>
              current < sourceCandidates.length - 1 ? current + 1 : current
            );
          } else {
            setSourceError(
              `This video file is unavailable (${res.status}). Re-upload this video to refresh its file path.`
            );
          }
        }
      } catch {
        if (!cancelled) {
          if (sourceIndex < sourceCandidates.length - 1) {
            setSourceIndex((current) =>
              current < sourceCandidates.length - 1 ? current + 1 : current
            );
          } else {
            setSourceError(
              "Unable to verify the video file URL. Please re-upload this video."
            );
          }
        }
      }
    }

    checkSource();

    return () => {
      cancelled = true;
    };
  }, [activeSrc, sourceIndex, sourceCandidates.length]);

  const handlePlaybackError = () => {
    if (sourceIndex < sourceCandidates.length - 1) {
      setSourceIndex((current) =>
        current < sourceCandidates.length - 1 ? current + 1 : current
      );
      return;
    }

    setSourceError(
      "Your browser could not play this video format. Try re-uploading in H.264 (MP4) or VP9 (WebM)."
    );
  };

  if (sourceError) {
    return (
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
        {sourceError}
      </div>
    );
  }

  return (
    <div className="simple-player">
      <video
        key={activeSrc}
        src={activeSrc}
        poster={poster}
        controls
        playsInline
        preload="metadata"
        onError={handlePlaybackError}
        style={{ width: "100%", height: "auto", borderRadius: 12, background: "#000" }}
      >
        {sourceCandidates.map((candidate) => (
          <source
            key={candidate}
            src={candidate}
            type={candidate.includes("f-webm") ? "video/webm" : "video/mp4"}
          />
        ))}
      </video>
    </div>
  );
}

