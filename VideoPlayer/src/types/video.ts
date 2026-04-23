export interface Video {
  id: string;
  title: string;
  description: string;
  filePath: string;
  fileName: string;
  thumbnailPath?: string;
  duration?: number;
  createdAt: string;
  subtitles?: SubtitleTrack[];
  watermark?: WatermarkConfig;
  // ImageKit optimization settings
  quality?: number; // 1-100, default 50
  format?: "auto" | "mp4" | "webm";
}

export interface SubtitleTrack {
  label: string;
  language: string;
  filePath: string;
}

export interface WatermarkConfig {
  imagePath: string;
  position: "top_left" | "top_right" | "bottom_left" | "bottom_right" | "center";
  opacity?: number;
  width?: number;
}
