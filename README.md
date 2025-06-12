# Raspberry Pi - Telegram Doorbell

## System Architecture

```mermaid
graph TD
    subgraph RaspberryPi
        Doorbell[Button]
        Pi[MQTT Publisher]
        Speaker[Play Sound]
        Visitor[Visitor Event]
        FaceRecognition

        Doorbell -->|Button Press| Visitor & Speaker
        FaceRecognition -->|Recognized| Visitor

        Visitor --> Pi

    end

    subgraph Server[Server]
        subgraph docker
            MQTT[MQTT Broker]
            Notifier[Telegram Service]
            UI[UI]
        end

        FileShare[File Store]
    end

    subgraph Phone
        Pushbullet
    end

    Phone[Smartphone with Pushbullet]


    Pi -->|Send Message| MQTT
    Notifier -->|Subscribe| MQTT
    MQTT -->|Notify| Notifier

    Visitor -->|Store Image| FileShare
    Notifier -->|Access Image| FileShare

    Notifier -->|Send Message| Pushbullet

    MQTT -->|Notify| UI
    UI -->|Subscribe| MQTT
    UI -->|Access| FileShare
    UI -->|Configure| Notifier
```

## Responsibilities

| Task/Component                        | Ziyan Wang        | Assel Massaurova  | Florian Schwarzmayr |
| :------------------------------------ | ----------------- | ----------------- | ------------------- |
| **Sensor \+ Actuator Combo**          | Camera \+ Speaker | Button \+ Speaker | Trigger \+ MQTT/FS  |
| Face Detection Logic                  | ✅                |                   |                     |
| GPIO Button Logic                     |                   | ✅                |                     |
| Sound Playback (shared logic)         | ✅                | ✅                |                     |
| Snapshot Capture                      | ✅                |                   |                     |
| Image Upload to Shared FS             |                   |                   | ✅ done             |
| MQTT Publisher                        |                   |                   | ✅ done             |
| MQTT Broker Setup (Docker)            |                   |                   | ✅ done             |
| Pushbullet Notification (Upload & Notify)    | ✅                  | ✅                | ✅ done             |
| Web UI – Image & History Display      | ✅                |                   |                     |
| Web UI – MQTT Subscription            |                   | ✅                |                     |
| Web UI – Config Panel                 |                   |                   | ✅ done             |
| Notification Preferences & Thresholds |                   |                   | ✅ done             |
| System Testing                        | ✅                | ✅                | ✅                  |
| Bugfixing                             | ✅                | ✅                | ✅                  |
| Documentation & Presentation          | ✅                | ✅                |                     |

## Schedule

```mermaid
gantt
    title Smart Doorbell Project Timeline
    dateFormat  YYYY-MM-DD
    axisFormat  %d.%m

    section Raspberry Pi
    Hardware Setup              :a1, 2025-04-21, 7d
    Camera & Face Recognition   :a2, after a1, 10d
    MQTT Publishing             :a3, after a2, 5d
    Image Upload Logic          :a4, after a2, 5d

    section Server (MQTT + Notifier)
    MQTT Broker Setup           :b1, 2025-04-21, 3d
    File Share Setup            :b2, after b1, 5d
    Telegram Bot Integration    :b3, after b2, 9d
    Configuration Interface        :b4, after b3, 5d

    section UI & Config Platform
    UI Design & Setup           :c1, 2025-04-21, 7d
    MQTT Subscriptions          :c2, after c1, 5d
    Visitor Image Display       :c3, after c2, 3d
    Configuration Interface     :c4, after c3, 7d

    section Final Testing & Adjustments
    Testing                     :d1, 2025-05-13, 7d
    Bugfixing                   :d2, after d1, 5d
    Docs & Presentation         :d3, after d2, 3d
```
