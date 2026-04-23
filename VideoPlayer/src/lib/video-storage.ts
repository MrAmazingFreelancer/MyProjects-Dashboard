import { Video } from '@/types/video';
import fs from 'fs';
import path from 'path';

const DATA_FILE = path.join(process.cwd(), 'data', 'videos.json');

function ensureDataFile(): void {
  const dataDir = path.dirname(DATA_FILE);
  if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true });
  }
  if (!fs.existsSync(DATA_FILE)) {
    fs.writeFileSync(DATA_FILE, JSON.stringify({ videos: [] }, null, 2));
  }
}

export function getAllVideos(): Video[] {
  ensureDataFile();
  const data = JSON.parse(fs.readFileSync(DATA_FILE, 'utf-8'));
  return data.videos || [];
}

export function getVideoById(id: string): Video | undefined {
  const videos = getAllVideos();
  return videos.find(v => v.id === id);
}

export function saveVideo(video: Video): Video {
  ensureDataFile();
  const data = JSON.parse(fs.readFileSync(DATA_FILE, 'utf-8'));
  data.videos.push(video);
  fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
  return video;
}
