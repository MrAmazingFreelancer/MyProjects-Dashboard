import { NextRequest, NextResponse } from "next/server";
import { getAllVideos, saveVideo } from "@/lib/video-storage";
import { Video } from "@/types/video";
import { v4 as uuidv4 } from "uuid";

// GET all videos
export async function GET() {
  try {
    const videos = getAllVideos();
    return NextResponse.json({ videos });
  } catch (error) {
    console.error("Error fetching videos:", error);
    return NextResponse.json(
      { error: "Failed to fetch videos" },
      { status: 500 }
    );
  }
}

// POST create new video
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    const video: Video = {
      id: uuidv4(),
      title: body.title || "Untitled Video",
      description: body.description || "",
      filePath: body.filePath,
      fileName: body.fileName,
      thumbnailPath: body.thumbnailPath || "",
      duration: body.duration,
      createdAt: new Date().toISOString(),
      subtitles: body.subtitles || [],
      watermark: body.watermark,
    };

    const savedVideo = saveVideo(video);
    return NextResponse.json({ video: savedVideo }, { status: 201 });
  } catch (error) {
    console.error("Error creating video:", error);
    return NextResponse.json(
      { error: "Failed to create video" },
      { status: 500 }
    );
  }
}
