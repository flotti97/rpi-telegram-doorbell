
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