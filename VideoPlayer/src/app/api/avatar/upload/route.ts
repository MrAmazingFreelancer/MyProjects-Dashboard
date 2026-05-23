import { put } from '@vercel/blob';
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const filename = searchParams.get('filename');

    if (!filename) {
      return NextResponse.json({ error: 'filename is required' }, { status: 400 });
    }

    if (!request.body) {
      return NextResponse.json({ error: 'request body is required' }, { status: 400 });
    }

    const blob = await put(filename, request.body, {
      access: 'public',
      addRandomSuffix: true,
      contentType: request.headers.get('content-type') ?? 'application/octet-stream',
    });

    return NextResponse.json(blob);
  } catch (error) {
    console.error('Avatar upload error:', error);
    return NextResponse.json({ error: 'Failed to upload avatar' }, { status: 500 });
  }
}