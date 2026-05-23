import { Video } from '@/types/video';
import fs from 'fs';
import os from 'os';
import path from 'path';

const LOCAL_DATA_FILE = path.join(process.cwd(), 'data', 'videos.json');
const VERCEL_DATA_FILE = path.join(os.tmpdir(), 'videos.json');

function getDataFilePath(): string {
  if (process.env.VERCEL) {
    return VERCEL_DATA_FILE;
  }

  return LOCAL_DATA_FILE;
}

function ensureDataFile(): void {
  const DATA_FILE = getDataFilePath();
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
  const DATA_FILE = getDataFilePath();
  const data = JSON.parse(fs.readFileSync(DATA_FILE, 'utf-8'));
  return data.videos || [];
}

export function getVideoById(id: string): Video | undefined {
  const videos = getAllVideos();
  return videos.find(v => v.id === id);
}

export function saveVideo(video: Video): Video {
  ensureDataFile();
  const DATA_FILE = getDataFilePath();
  const data = JSON.parse(fs.readFileSync(DATA_FILE, 'utf-8'));
  data.videos.push(video);
  fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
  return video;
}
