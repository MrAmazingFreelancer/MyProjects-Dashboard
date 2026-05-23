import { head } from '@vercel/blob';
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    const url = request.nextUrl.searchParams.get('url');

    if (!url) {
      return NextResponse.json({ error: 'Missing url parameter' }, { status: 400 });
    }

    const metadata = await head(url);
    if (!metadata) {
      return new NextResponse('Not found', { status: 404 });
    }

    // Redirect to the blob's download URL
    return NextResponse.redirect(metadata.url);
  } catch (error) {
    console.error('Avatar view error:', error);
    return NextResponse.json({ error: 'Failed to fetch avatar' }, { status: 500 });
  }
}