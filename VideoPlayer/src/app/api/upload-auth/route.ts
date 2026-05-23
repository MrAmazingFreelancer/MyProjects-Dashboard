import { getUploadAuthParams } from "@imagekit/next/server";
import { NextResponse } from "next/server";

export async function GET() {
  try {
    const privateKey = process.env.IMAGEKIT_PRIVATE_KEY?.trim();
    const publicKey = process.env.IMAGEKIT_PUBLIC_KEY?.trim();

    if (!privateKey) {
      return NextResponse.json(
        { error: "ImageKit private key is not configured" },
        { status: 500 }
      );
    }

    if (!publicKey) {
      return NextResponse.json(
        { error: "ImageKit public key is not configured" },
        { status: 500 }
      );
    }

    const { token, expire, signature } = getUploadAuthParams({
      privateKey,
      publicKey,
    });

    return NextResponse.json({
      token,
      expire,
      signature,
      publicKey,
    });
  } catch (error) {
    console.error("Upload auth error:", error);
    return NextResponse.json(
      { error: "Failed to generate upload credentials" },
      { status: 500 }
    );
  }
}
