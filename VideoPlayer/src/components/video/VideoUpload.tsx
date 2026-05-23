"use client";

import { useState } from "react";
import { upload } from "@imagekit/next";
import { useRouter } from "next/navigation";
import "@/styles/upload.css";

const LANGUAGES: Record<string, string> = {
  en: "English", es: "Spanish", fr: "French", de: "German",
};

export default function VideoUpload() {
  const router = useRouter();
  const [form, setForm] = useState({ title: "", description: "", subtitleLang: "en" });
  const [files, setFiles] = useState<Record<string, File | null>>({
    video: null, thumbnail: null, subtitle: null, watermark: null,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const toUploadErrorMessage = (err: unknown): string => {
    if (err instanceof Error) {
      const msg = err.message || "Upload failed";
      const lower = msg.toLowerCase();
      if (lower.includes("network error") || lower.includes("failed to fetch")) {
        return "Network error while uploading. Disable ad-blocker/VPN for this site and retry.";
      }
      return msg;
    }

    return "Upload failed";
  };

  const uploadFile = async (file: File, folder: string) => {
    const authRes = await fetch("/api/upload-auth");
    const auth = await authRes.json();

    if (!authRes.ok) {
      throw new Error(auth?.error || "Failed to get upload credentials");
    }

    if (!auth?.publicKey) {
      throw new Error("Upload auth missing public key");
    }

    if (!auth?.token || !auth?.signature || !auth?.expire) {
      throw new Error("Upload auth payload is incomplete");
    }

    let lastError: unknown;
    for (let attempt = 0; attempt < 2; attempt += 1) {
      try {
        return await upload({
          file,
          fileName: file.name,
          folder,
          ...auth,
          publicKey: auth.publicKey,
        });
      } catch (err) {
        lastError = err;
        const message = err instanceof Error ? err.message.toLowerCase() : "";
        const isNetworkError =
          message.includes("network error") || message.includes("failed to fetch");

        if (!isNetworkError || attempt === 1) {
          break;
        }

        await new Promise((resolve) => setTimeout(resolve, 600));
      }
    }

    throw new Error(toUploadErrorMessage(lastError));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!files.video) return;

    setLoading(true);
    setError("");

    try {
      // Upload all files in parallel
      const [videoRes, thumbRes, subRes, wmRes] = await Promise.all([
        uploadFile(files.video, "/videos"),
        files.thumbnail ? uploadFile(files.thumbnail, "/thumbnails") : null,
        files.subtitle ? uploadFile(files.subtitle, "/subtitles") : null,
        files.watermark ? uploadFile(files.watermark, "/watermarks") : null,
      ]);

      // Save video metadata
      const res = await fetch("/api/videos", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: form.title || files.video.name.replace(/\.[^/.]+$/, ""),
          description: form.description,
          filePath: videoRes.filePath || "",
          fileName: videoRes.name || files.video.name,
          thumbnailPath: thumbRes?.filePath || "",
          subtitles: subRes ? [{ label: LANGUAGES[form.subtitleLang], language: form.subtitleLang, filePath: subRes.filePath || "" }] : [],
          watermark: wmRes ? { imagePath: wmRes.filePath || "", position: "bottom_right", opacity: 0.7, width: 120 } : undefined,
        }),
      });

      if (!res.ok) {
        const body = await res.json().catch(() => null);
        throw new Error(body?.error || "Failed to save");
      }
      const { video } = await res.json();
      const params = new URLSearchParams({
        title: video.title || form.title || files.video.name,
        description: video.description || form.description || "",
        filePath: video.filePath || videoRes.filePath || "",
        fileName: video.fileName || videoRes.name || files.video.name,
        thumbnailPath: video.thumbnailPath || thumbRes?.filePath || "",
      });
      router.push(`/watch/${video.id}?${params.toString()}`);
    } catch (err) {
      setError(toUploadErrorMessage(err));
      setLoading(false);
    }
  };

  const setFile = (key: string) => (e: React.ChangeEvent<HTMLInputElement>) => {
    setFiles((f) => ({ ...f, [key]: e.target.files?.[0] || null }));
  };

  return (
    <form onSubmit={handleSubmit} className="upload-form">
      {error && <div className="upload-error">{error}</div>}

      <div className="form-group">
        <label className="form-label">Title</label>
        <input
          type="text"
          value={form.title}
          onChange={(e) => setForm((f) => ({ ...f, title: e.target.value }))}
          className="form-input"
          placeholder="Video title"
        />
      </div>

      <div className="form-group">
        <label className="form-label">Description</label>
        <textarea
          value={form.description}
          onChange={(e) => setForm((f) => ({ ...f, description: e.target.value }))}
          className="form-textarea"
          rows={2}
        />
      </div>

      <div className="form-group">
        <label className="form-label">Video File *</label>
        <input type="file" accept="video/*" onChange={setFile("video")} />
      </div>

      <div className="form-group">
        <label className="form-label">Thumbnail (optional)</label>
        <input type="file" accept="image/*" onChange={setFile("thumbnail")} />
      </div>

      <div className="form-group">
        <div className="form-row">
          <div className="form-row-main">
            <label className="form-label">Subtitles (optional)</label>
            <input type="file" accept=".srt,.vtt,.ass" onChange={setFile("subtitle")} />
          </div>
          <div>
            <label className="form-label">Language</label>
            <select
              value={form.subtitleLang}
              onChange={(e) => setForm((f) => ({ ...f, subtitleLang: e.target.value }))}
              className="form-select"
            >
              {Object.entries(LANGUAGES).map(([code, name]) => (
                <option key={code} value={code}>{name}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      <div className="form-group">
        <label className="form-label">Watermark (optional)</label>
        <input type="file" accept="image/png,image/svg+xml" onChange={setFile("watermark")} />
      </div>

      <button type="submit" disabled={loading || !files.video} className="submit-button">
        {loading ? "Uploading..." : "Upload"}
      </button>
    </form>
  );
}
