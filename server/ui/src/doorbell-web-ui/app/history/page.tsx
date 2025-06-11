<<<<<<< HEAD

  export default function HistoryPage() {
    return (
      <div className="p-8 max-w-2xl mx-auto">
        <h2 className="text-2xl font-bold mb-4">History</h2>
        <ul className="space-y-2">
          <li className="border rounded px-4 py-2">
            <span className="font-semibold">2024-06-06 02:48:</span> Visitor detected
          </li>
          <li className="border rounded px-4 py-2">
            <span className="font-semibold">2024-06-06 2:54:</span> Visitor detected
          </li>
          <li className="border rounded px-4 py-2">
            <span className="font-semibold">2024-06-06 03:01:</span> Visitor detected
          </li>
        </ul>
      </div>
    );
  }
=======
'use client';

import { useEffect, useState } from "react";

function formatTimestamp(filename: string): string {
  const match = filename.match(/face_(\d+)\.jpg/i);
  if (!match) return filename;
  const ts = parseInt(match[1]) * 1000;
  return new Date(ts).toLocaleString();
}

export default function HistoryPage() {
  const [images, setImages] = useState<string[]>([]);

  const fetchImages = async () => {
    try {
      const res = await fetch("/api/images");
      const data = await res.json();
      setImages(data.images);
    } catch (e) {
      console.error("❌ Failed to load images:", e);
    }
  };

  useEffect(() => {
    fetchImages(); // initial load
    const interval = setInterval(fetchImages, 5000); // refresh every 5s
    return () => clearInterval(interval);
  }, []);

  return (
    <main className="p-6">
      <h1 className="text-2xl font-bold mb-4">📸 Visitor History</h1>
      {images.length === 0 ? (
        <p className="text-gray-500">No visitor images found.</p>
      ) : (
        <div className="space-y-4">
          {images.map((img, idx) => (
            <div key={idx} className="border rounded shadow p-2">
              <p className="text-sm text-gray-700 mb-1">{formatTimestamp(img)}</p>
              <img
                src={`http://localhost:8080/${img}?t=${Date.now()}`}
                alt="Visitor"
                className="rounded w-full max-w-md object-cover"
                onError={(e) => {
                  (e.target as HTMLImageElement).style.display = "none";
                }}
              />
            </div>
          ))}
        </div>
      )}
    </main>
  );
}
>>>>>>> master
