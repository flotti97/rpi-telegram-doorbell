import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[70vh]">
      <Card className="w-full max-w-lg shadow-lg">
        <CardHeader>
          <CardTitle className="text-3xl">Welcome to the RPi Doorbell Notifier</CardTitle>
          <CardDescription>
            Manage your smart doorbell notifications and settings from this dashboard.
          </CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col gap-6 items-center">
          <div className="text-center text-muted-foreground">
            <p>
              Use the navigation above to view visitor history or configure your Telegram and MQTT settings.
            </p>
          </div>
          <div className="flex gap-4">
            <Button asChild>
              <Link href="/history">View History</Link>
            </Button>
            <Button variant="outline" asChild>
              <Link href="/settings">Settings</Link>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}