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

    if (!body.filePath || !body.fileName) {
      return NextResponse.json(
        { error: "filePath and fileName are required" },
        { status: 400 }
      );
    }
    
    const video: Video = {
      id: body.id || uuidv4(),
      title: body.title || "Untitled Video",
      description: body.description || "",
      filePath: body.filePath,
      fileName: body.fileName,
      thumbnailPath: body.thumbnailPath || "",
      duration: body.duration,
      createdAt: body.createdAt || new Date().toISOString(),
      subtitles: body.subtitles || [],
      watermark: body.watermark,
    };

    const savedVideo = saveVideo(video);
    return NextResponse.json({ video: savedVideo }, { status: 201 });
  } catch (error) {
    console.error("Error creating video:", error);
    const message = error instanceof Error ? error.message : "Failed to create video";
    return NextResponse.json(
      { error: message },
      { status: 500 }
    );
  }
}
