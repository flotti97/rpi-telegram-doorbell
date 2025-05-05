import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";

export default function SettingsPage() {
  return (
    <div className="p-8 max-w-xl mx-auto">
      <h2 className="text-2xl font-bold mb-6">Settings</h2>
      <form className="space-y-8">
        {/* Telegram Section */}
        <section>
          <h3 className="text-lg font-semibold mb-2">Telegram</h3>
          <div className="space-y-4">
            <div>
              <Label htmlFor="botToken">Telegram Token</Label>
              <Input
                id="botToken"
                type="text"
                className="mt-1"
                placeholder="Enter your Telegram Bot Token"
              />
            </div>
            <div>
              <Label htmlFor="chatIds">Telegram Chat Ids</Label>
              <Textarea
                id="chatIds"
                className="mt-1"
                placeholder="Enter one or more Chat IDs, separated by commas"
                rows={2}
              />
            </div>
          </div>
        </section>

        {/* MQTT Section */}
        <section>
          <h3 className="text-lg font-semibold mb-2">MQTT</h3>
          <div className="space-y-4">
            <div>
              <Label htmlFor="mqttBrokerIp">MQTT Broker IP</Label>
              <Input
                id="mqttBrokerIp"
                type="text"
                className="mt-1"
                placeholder="e.g. 192.168.1.10"
              />
            </div>
            <div>
              <Label htmlFor="mqttBrokerPort">MQTT Broker Port</Label>
              <Input
                id="mqttBrokerPort"
                type="number"
                className="mt-1"
                placeholder="e.g. 1883"
              />
            </div>
            <div>
              <Label htmlFor="mqttTopic">MQTT Topic</Label>
              <Input
                id="mqttTopic"
                type="text"
                className="mt-1"
                placeholder="e.g. visitor"
              />
            </div>
          </div>
        </section>

        {/* Doorbell Section */}
        <section>
          <h3 className="text-lg font-semibold mb-2">Doorbell</h3>
          <div>
            <Label htmlFor="faceRecognition">Face Recognition configuration</Label>
            <Textarea
              id="faceRecognition"
              className="mt-1"
              placeholder="Paste your face recognition configuration here"
              rows={3}
            />
          </div>
        </section>

        <Button type="submit" className="w-full">
          Save
        </Button>
      </form>
    </div>
  );
}