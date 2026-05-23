// Test script: exercises the full upload flow against the production deployment
// Uses ImageKit JS SDK (same as the app's client-side upload)
import ImageKit from "@imagekit/javascript";

const BASE_URL = "https://video-player-psi-nine.vercel.app";

async function testUpload() {
  console.log("1. Getting upload auth credentials...");
  const authRes = await fetch(`${BASE_URL}/api/upload-auth`);
  if (!authRes.ok) {
    const err = await authRes.text();
    console.error("   FAILED:", authRes.status, err);
    return;
  }
  const auth = await authRes.json();
  console.log("   OK - got token, signature, expire, publicKey");
  console.log("   Token prefix:", auth.token?.substring(0, 20) + "...");
  console.log("   Expire:", auth.expire);

  console.log("\n2. Uploading sample video to ImageKit...");
  // Use a small public domain video URL
  const sampleUrl = "https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/360/Big_Buck_Bunny_360_10s_1MB.mp4";

  const imagekit = new ImageKit({
    publicKey: auth.publicKey,
    urlEndpoint: "https://ik.imagekit.io/mramazing/VPData",
  });

  const uploadResult = await imagekit.upload({
    file: sampleUrl,
    fileName: "test-sample-video.mp4",
    folder: "/videos",
    token: auth.token,
    signature: auth.signature,
    expire: auth.expire,
  });

  console.log("   OK - uploaded to:", uploadResult.filePath);
  console.log("   URL:", uploadResult.url);

  console.log("\n3. Saving video metadata via API...");
  const saveRes = await fetch(`${BASE_URL}/api/videos`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      title: "Test Upload - Big Buck Bunny",
      description: "Sample video uploaded via test script",
      filePath: uploadResult.filePath,
      fileName: uploadResult.name || "test-sample-video.mp4",
      thumbnailPath: "",
    }),
  });

  if (!saveRes.ok) {
    const err = await saveRes.text();
    console.error("   FAILED:", saveRes.status, err);
    return;
  }
  const { video } = await saveRes.json();
  console.log("   OK - saved with id:", video.id);

  console.log("\n4. Verifying video appears in library...");
  const listRes = await fetch(`${BASE_URL}/api/videos`);
  const { videos } = await listRes.json();
  const found = videos.find((v) => v.id === video.id);
  if (found) {
    console.log("   OK - video found in library");
  } else {
    console.error("   FAILED - video not in library list");
  }

  console.log("\n5. Verifying watch page loads...");
  const watchRes = await fetch(`${BASE_URL}/watch/${video.id}`);
  if (watchRes.ok) {
    console.log("   OK - watch page returns 200");
  } else {
    console.error("   FAILED:", watchRes.status);
  }

  console.log("\n--- TEST COMPLETE ---");
  console.log(`Watch page: ${BASE_URL}/watch/${video.id}`);
  console.log(`Library: ${BASE_URL}/VideoPlayer`);
}

testUpload().catch(console.error);
