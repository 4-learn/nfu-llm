import os
import json
from phi.agent import Agent
from phi.model.openai import OpenAIChat
import paho.mqtt.client as mqtt

# led_intensity_control.py
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_TOPIC = os.getenv("MQTT_TOPIC")

def control_led_intensity(intensity: int):
    try:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        message = json.dumps({"intensity": intensity})
        client.publish(MQTT_TOPIC, message)
        client.disconnect()
        return f"成功設置 LED 強度為 {intensity}%"
    except Exception as e:
        print(f"Debug - MQTT Error: {str(e)}")
        return f"LED 控制失敗: {str(e)}"

led_agent = Agent(
    name="LED Intensity Agent",
    role="控制 LED 亮度",
    instructions=[
        "負責解析用戶對 LED 亮度的設定指令",
        "強度範圍：0-100%",
        "收到具體數字時使用該數字，否則根據描述判斷：",
        "- 微弱：20%以下",
        "- 適中：20-70%",
        "- 明亮：70%以上"
    ],
    tools=[control_led_intensity],
    model=OpenAIChat(id="gpt-4")
)

def main():
    print("LED 亮度控制助理 (輸入 'exit' 結束)")
    print("設定範例：'設定亮度 50%' 或 '調暗一點'")
    
    while True:
        user_input = input("\n指令: ").strip()
        if user_input.lower() == 'exit':
            break
        try:
            response = led_agent.run(user_input, stream=False)
            for message in response.messages:
                if message.role == "assistant" and message.content:
                    print("\n回應:", message.content.strip())
        except Exception as e:
            print(f"\n錯誤：{str(e)}")

if __name__ == "__main__":
    main()