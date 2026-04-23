import { NextRequest, NextResponse } from "next/server";
import { getVideoById } from "@/lib/video-storage";

interface RouteParams {
  params: Promise<{ id: string }>;
}

// GET single video
export async function GET(request: NextRequest, { params }: RouteParams) {
  try {
    const { id } = await params;
    const video = getVideoById(id);

    if (!video) {
      return NextResponse.json({ error: "Video not found" }, { status: 404 });
    }

    return NextResponse.json({ video });
  } catch (error) {
    console.error("Error fetching video:", error);
    return NextResponse.json({ error: "Failed to fetch video" }, { status: 500 });
  }
}
