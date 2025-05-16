import { NextRequest, NextResponse } from "next/server";
import fs from "fs/promises";

// Update the path to match the Docker mount
const CONFIG_PATH = "/app/settings/settings.json";

export async function POST(req: NextRequest) {
  const data = await req.json();
  await fs.writeFile(CONFIG_PATH, JSON.stringify(data, null, 2), "utf-8");
  return NextResponse.json({ success: true });
}

export async function GET() {
  try {
    const content = await fs.readFile(CONFIG_PATH, "utf-8");
    return NextResponse.json(JSON.parse(content));
  } catch {
    return NextResponse.json({}, { status: 200 });
  }
}