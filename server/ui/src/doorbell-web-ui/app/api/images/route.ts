import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

export async function GET() {
  const imageDir = path.join(process.cwd(), "public", "images");

  try {
    const files = fs
      .readdirSync(imageDir)
      .filter(f => f.startsWith("face_") && f.toLowerCase().endsWith(".jpg"))
      .sort((a, b) => b.localeCompare(a)); // newest first

    return NextResponse.json({ images: files });
  } catch (e) {
    console.error("Failed to read image directory:", e);
    return NextResponse.json({ images: [] });
  }
}
