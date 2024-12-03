import os
import json
from phi.agent import Agent
from phi.model.openai import OpenAIChat
import paho.mqtt.client as mqtt

MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_TOPIC = os.getenv("MQTT_TOPIC")

def emotion(r: int, g: int, b: int):
    try:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        message = json.dumps({"r": r, "g": g, "b": b})
        client.publish(MQTT_TOPIC, message)
        client.disconnect()
        return f"成功設置 LED 顏色: R={r}, G={g}, B={b}"
    except Exception as e:
        print(f"Debug - MQTT Error: {str(e)}")
        return f"LED 控制失敗: {str(e)}"

emotion_agent = Agent(
    name="Emotion LED Agent",
    role="情感顏色分析與控制",
    instructions=[
        "你是一個情感分析助手，負責將文字轉換為相應的RGB顏色。",
        "請依照以下規則執行:",
        "1. 解析用戶輸入的情感描述",
        "2. 將情感轉換為RGB值 (0-255)",
        "3. 呼叫 emotion 函數設定顏色",
        "4. 若要表達溫暖的紅色，使用: emotion(255, 102, 102)"
    ],
    tools=[emotion],
    model=OpenAIChat(id="gpt-4o")
)

def main():
    print("智能助理已啟動！(輸入 'exit' 結束程式)")
    print("您可以輸入情感相關的描述，我將根據您的描述控制 LED 的顏色。")
    
    while True:
        user_input = input("\n請輸入情感描述: ").strip()
        if user_input.lower() == 'exit':
            break
        try:
            response = emotion_agent.run(user_input, stream=False)
            for message in response.messages:
                if message.role == "assistant" and message.content:
                    print("\n回應:", message.content.strip())
        except Exception as e:
            print(f"\n錯誤：{str(e)}")

if __name__ == "__main__":
    main()