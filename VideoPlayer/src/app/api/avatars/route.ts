import { NextRequest, NextResponse } from 'next/server';
import { v4 as uuidv4 } from 'uuid';
import { getAllAvatars, saveAvatar } from '@/lib/avatar-storage';
import { AvatarRecord } from '@/types/avatar';

export async function GET() {
  try {
    const avatars = getAllAvatars();
    return NextResponse.json({ avatars });
  } catch (error) {
    console.error('Error fetching avatars:', error);
    return NextResponse.json({ error: 'Failed to fetch avatars' }, { status: 500 });
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    if (!body.filePath || !body.fileName || !body.url) {
      return NextResponse.json({ error: 'filePath, fileName and url are required' }, { status: 400 });
    }

    const avatar: AvatarRecord = {
      id: uuidv4(),
      filePath: body.filePath,
      fileName: body.fileName,
      url: body.url,
      createdAt: new Date().toISOString(),
    };

    const savedAvatar = saveAvatar(avatar);
    return NextResponse.json({ avatar: savedAvatar }, { status: 201 });
  } catch (error) {
    console.error('Error creating avatar record:', error);
    const message = error instanceof Error ? error.message : 'Failed to save avatar';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
