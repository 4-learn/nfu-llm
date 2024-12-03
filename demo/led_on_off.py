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

def control_led(action: bool):
    try:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        message = json.dumps({"action": "on" if action else "off"})
        client.publish(MQTT_TOPIC, message)
        client.disconnect()
        return f"成功{'打開' if action else '關閉'} LED"
    except Exception as e:
        print(f"Debug - MQTT Error: {str(e)}")
        print(f"Debug - MQTT Settings: Broker={MQTT_BROKER}, Port={MQTT_PORT}")
        return f"LED 控制失敗: {str(e)}"

led_agent = Agent(
    name="LED Control Agent",
    role="控制 LED 開關",
    instructions=[
        "你是一個 LED 控制助手，負責解析用戶的開關燈指令。",
        "當用戶要求打開 LED 時，呼叫 control_led(True)",
        "當用戶要求關閉 LED 時，呼叫 control_led(False)",
        "對於不明確的指令，請詢問用戶具體需求"
    ],
    tools=[control_led],
    model=OpenAIChat(id="gpt-4")
)

def main():
    print("智能助理已啟動！(輸入 'exit' 結束程式)")
    print("您可以：")
    print("1. 控制 LED 開關 (例如：'請打開 LED' 或 '關燈')")
    
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