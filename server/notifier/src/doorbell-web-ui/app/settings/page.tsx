"use client";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { useState } from "react";

export default function SettingsPage() {

  const [form, setForm] = useState({
    botToken: "",
    chatIds: "",
    mqttBrokerIp: "",
    mqttBrokerPort: "",
    mqttTopic: "",
    faceRecognition: "",
  });
  const [status, setStatus] = useState("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setForm({ ...form, [e.target.id]: e.target.value });
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


  return (
    <div className="p-8 max-w-xl mx-auto">
      <h2 className="text-2xl font-bold mb-6">Settings</h2>
      <form className="space-y-8" onSubmit={handleSubmit}>
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
                value={form.botToken} onChange={handleChange}
              />
            </div>
            <div>
              <Label htmlFor="chatIds">Telegram Chat Ids</Label>
              <Textarea
                id="chatIds"
                className="mt-1"
                placeholder="Enter one or more Chat IDs, separated by commas"
                rows={2}
                value={form.chatIds} onChange={handleChange}
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
              value={form.faceRecognition} onChange={handleChange}
            />
          </div>
        </section>

        <Button type="submit" className="w-full">Save</Button>
        {status && <div className="mt-2 text-center">{status}</div>}
      </form>
    </div>
  );
}