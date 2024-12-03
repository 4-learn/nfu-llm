import os
import json
import paho.mqtt.client as mqtt
from openai import OpenAI

MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_TOPIC = os.getenv("MQTT_TOPIC")

def control_led(r: int, g: int, b: int):
    try:
        color = {"r": r, "g": g, "b": b}
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        message = json.dumps(color)
        client.publish(MQTT_TOPIC, message)
        client.disconnect()
        return f"成功設置 LED 顏色: R={r}, G={g}, B={b}"
    except Exception as e:
        return f"LED 控制失敗: {str(e)}"

def analyze_emotion(prompt):
    try:
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system", 
                    "content": """你是一個情感分析助手，負責將文字轉換為相應的RGB顏色。
請依照以下規則回覆：
1. 回覆必須是三個介於0-255之間的數字
2. 數字之間用逗號分隔
3. 不要加入任何其他文字或符號
4. 舉例：若要表達溫暖的紅色，回覆應為：255,102,102"""
                },
                {"role": "user", "content": prompt}
            ]
        )
        
        result = response.choices[0].message.content.strip()
        r, g, b = map(int, result.split(","))
        
        # 驗證 RGB 值範圍
        if not all(0 <= x <= 255 for x in (r, g, b)):
            raise ValueError("RGB 值超出範圍")
            
        return r, g, b
    except Exception as e:
        print(f"情感分析失敗: {str(e)}")
        return 255, 255, 255  # 預設白色

def main():
    print("智能助理已啟動！(輸入 'exit' 結束程式)")
    print("您可以輸入情感相關的描述，我將根據您的描述控制 LED 的顏色。")
    
    while True:
        user_input = input("\n請輸入情感描述: ").strip()
        
        if user_input.lower() == 'exit':
            print("程式已結束")
            break
            
        try:
            r, g, b = analyze_emotion(user_input)
            result = control_led(r, g, b)
            print(result)
        except Exception as e:
            print(f"\n錯誤：{str(e)}")

if __name__ == "__main__":
    main()