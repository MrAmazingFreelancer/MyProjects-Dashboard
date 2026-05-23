import { AvatarRecord } from '@/types/avatar';
import fs from 'fs';
import os from 'os';
import path from 'path';

const LOCAL_DATA_FILE = path.join(process.cwd(), 'data', 'avatars.json');
const VERCEL_DATA_FILE = path.join(os.tmpdir(), 'avatars.json');

function getDataFilePath(): string {
  if (process.env.VERCEL) {
    return VERCEL_DATA_FILE;
  }

  return LOCAL_DATA_FILE;
}

function ensureDataFile(): void {
  const dataFile = getDataFilePath();
  const dataDir = path.dirname(dataFile);

  if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true });
  }

  if (!fs.existsSync(dataFile)) {
    fs.writeFileSync(dataFile, JSON.stringify({ avatars: [] }, null, 2));
  }
}

export function getAllAvatars(): AvatarRecord[] {
  ensureDataFile();
  const dataFile = getDataFilePath();
  const data = JSON.parse(fs.readFileSync(dataFile, 'utf-8'));
  return data.avatars || [];
}

export function saveAvatar(avatar: AvatarRecord): AvatarRecord {
  ensureDataFile();
  const dataFile = getDataFilePath();
  const data = JSON.parse(fs.readFileSync(dataFile, 'utf-8'));
  data.avatars.push(avatar);
  fs.writeFileSync(dataFile, JSON.stringify(data, null, 2));
  return avatar;
}
