import os
import json
import time
from phi.agent import Agent
from phi.model.openai import OpenAIChat
import paho.mqtt.client as mqtt

MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_TOPIC = os.getenv("MQTT_TOPIC")

def control_led_speed(sleep_time: float):
    try:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        
        message = json.dumps({"sleep": sleep_time})
        client.publish(MQTT_TOPIC, message)
        client.disconnect()
        return f"成功設置 LED 閃爍間隔為 {sleep_time} 秒"
    except Exception as e:
        print(f"Debug - MQTT Error: {str(e)}")
        print(f"Debug - MQTT Settings: Broker={MQTT_BROKER}, Port={MQTT_PORT}")
        return f"LED 控制失敗: {str(e)}"

led_agent = Agent(
    name="LED Control Agent",
    role="控制 LED 閃爍速度",
    instructions=[
        "你是一個 LED 控制助手，負責解析用戶對 LED 閃爍速度的設定指令",
        "數值範圍為 0.1 到 5 秒",
        "收到的指令包含具體數字時使用該數字，否則根據快慢描述判斷：",
        "- 快：0.1-0.5秒",
        "- 中：0.5-2秒",
        "- 慢：2-5秒"
    ],
    tools=[control_led_speed],
    model=OpenAIChat(id="gpt-4")
)

def main():
    print("智能助理已啟動！(輸入 'exit' 結束程式)")
    print("您可以：")
    print("1. 設定 LED 閃爍速度 (例如：'設定閃爍 0.5 秒' 或 '快速閃爍')")
    
    while True:
        user_input = input("\n請輸入指令: ").strip()
        
        if user_input.lower() == 'exit':
            print("程式已結束")
            break
            
        try:
            response = led_agent.run(user_input, stream=False)
            
            for message in response.messages:
                if message.role == "assistant" and message.content:
                    print("\n助理回應:", message.content.strip())
                    
        except Exception as e:
            print(f"\n錯誤：{str(e)}")

if __name__ == "__main__":
    main()