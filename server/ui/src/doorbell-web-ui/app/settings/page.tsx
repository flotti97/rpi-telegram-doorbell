"use client";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { useState, useEffect } from "react";

export default function SettingsPage() {

  const [form, setForm] = useState({
    mqttBrokerIp: "",
    mqttBrokerPort: "",
    mqttTopic: "",
    pushbulletToken: "",
    pushbulletChannelTag: "",
    doorbellName: "",
    notificationFrequency: 10,
  });
  const [status, setStatus] = useState("");

  // Load settings on mount
  useEffect(() => {
    const fetchSettings = async () => {
      setStatus("Loading...");
      try {
        const res = await fetch("/api/settings");
        if (res.ok) {
          const data = await res.json();
          setForm({
            mqttBrokerIp: data.mqttBrokerIp || "",
            mqttBrokerPort: data.mqttBrokerPort || "",
            mqttTopic: data.mqttTopic || "",
            pushbulletToken: data.pushbulletToken || "",
            pushbulletChannelTag: data.pushbulletChannelTag || "",
            doorbellName: data.doorbellName || "",
            notificationFrequency: data.notificationFrequency ?? 10,
          });
          setStatus("");
        } else {
          setStatus("Failed to load settings");
        }
      } catch {
        setStatus("Failed to load settings");
      }
    };
    fetchSettings();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { id, value, type } = e.target;
    setForm({ ...form, [id]: type === "number" ? Number(value) : value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus("Saving...");
    const res = await fetch("/api/settings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });
    setStatus(res.ok ? "Saved!" : "Error saving settings");
  };

  const handleMqttConnect = async () => {
    setStatus("Connecting to MQTT...");
    const res = await fetch("http://localhost:8000/mqtt/connect", { method: "POST" });
    const data = await res.json();
    setStatus(data.status || "Connect request sent");
  };

  const handleMqttDisconnect = async () => {
    setStatus("Disconnecting from MQTT...");
    const res = await fetch("http://localhost:8000/mqtt/disconnect", { method: "POST" });
    const data = await res.json();
    setStatus(data.status || "Disconnect request sent");
  };

  return (
    <div className="p-8 max-w-xl mx-auto">
      <h2 className="text-2xl font-bold mb-6">Settings</h2>

      <div className="flex gap-4 mb-6">
        <Button type="button" onClick={handleMqttConnect}>
          Connect MQTT
        </Button>
        <Button type="button" onClick={handleMqttDisconnect}>
          Disconnect MQTT
        </Button>
      </div>
      
      <form className="space-y-8" onSubmit={handleSubmit}>
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
                value={form.mqttBrokerIp} onChange={handleChange}
              />
            </div>
            <div>
              <Label htmlFor="mqttBrokerPort">MQTT Broker Port</Label>
              <Input
                id="mqttBrokerPort"
                type="number"
                className="mt-1"
                placeholder="e.g. 1883"
                value={form.mqttBrokerPort} onChange={handleChange}
              />
            </div>
            <div>
              <Label htmlFor="mqttTopic">MQTT Topic</Label>
              <Input
                id="mqttTopic"
                type="text"
                className="mt-1"
                placeholder="e.g. visitor"
                value={form.mqttTopic} onChange={handleChange}
              />
            </div>
          </div>
        </section>

        {/* Pushbullet Section */}
        <section>
          <h3 className="text-lg font-semibold mb-2">Pushbullet</h3>
          <div className="space-y-4">
            <div>
              <Label htmlFor="pushbulletToken">Pushbullet Token</Label>
              <Input
                id="pushbulletToken"
                type="text"
                className="mt-1"
                placeholder="Enter your Pushbullet Access Token"
                value={form.pushbulletToken} onChange={handleChange}
              />
            </div>
            <div>
              <Label htmlFor="pushbulletChannelTag">Pushbullet Channel Tag</Label>
              <Input
                id="pushbulletChannelTag"
                type="text"
                className="mt-1"
                placeholder="Enter your Pushbullet Channel Tag"
                value={form.pushbulletChannelTag} onChange={handleChange}
              />
            </div>
          </div>
        </section>

        {/* Doorbell Section */}
        <section>
          <h3 className="text-lg font-semibold mb-2">Doorbell</h3>
          <div className="space-y-4">
            <div>
              <Label htmlFor="doorbellName">Doorbell Name</Label>
              <Input
                id="doorbellName"
                type="text"
                className="mt-1"
                placeholder="e.g. Main Doorbell"
                value={form.doorbellName} onChange={handleChange}
              />
            </div>
            <div>
              <Label htmlFor="notificationFrequency">Notification Frequency (seconds)</Label>
              <Input
                id="notificationFrequency"
                type="number"
                className="mt-1"
                placeholder="e.g. 10"
                value={form.notificationFrequency} onChange={handleChange}
                min={1}
              />
            </div>
          </div>
        </section>

        <Button type="submit" className="w-full">Save</Button>
        {status && <div className="mt-2 text-center">{status}</div>}
      </form>
    </div>
  );
}