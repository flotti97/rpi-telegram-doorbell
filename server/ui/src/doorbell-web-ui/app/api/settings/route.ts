import { NextRequest, NextResponse } from "next/server";
import fs from "fs/promises";
import path from "path";

const CONFIG_PATH = path.resolve(process.cwd(), "..\\settings.json");

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