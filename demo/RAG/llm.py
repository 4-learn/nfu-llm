import os
from phi.agent import Agent
from phi.model.openai import OpenAIChat
# import paho.mqtt.client as mqtt
from weather import fetch_weather_data

# OpenAI API 設定 (請替換為您的 API Key)
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

def introduce_self():
    """自我介紹"""
    return """
    大家好！我是一個智能助理，我可以：
    1. 自我介紹
    2. 搜尋新聞
    
    您可以對我說「搜尋一下 LLM 目前的新聞」或類似的指令，我會幫您完成操作！
    """

intro_agent = Agent(
    name="Introduction Agent",
    role="進行自我介紹",
    instructions=[
        "1. 使用 introduce_self 工具進行自我介紹",
        "2. 提供友善且專業的介紹"
    ],
    tools=[introduce_self]
)

def get_weather():
    """取得台北市的天氣資訊"""
    return fetch_weather_data("台北市")


weather_agent = Agent(
    name="Get Taipei weather Agent",
    role="取得台北市的天氣資訊",
    instructions=[
        "1. 使用 get_weather 取得台北市的天氣資訊",
        "2. 返回天氣資訊"
    ],
    tools=[get_weather]
)

# 創建 agent 團隊
agent_team = Agent(
    model=OpenAIChat(id="gpt-4o"),
    name="智能助理團隊",
    team=[weather_agent, intro_agent],
    instructions=[
        "1. 識別用戶需求選擇合適的 agent",
        "2. 立即執行相應操作",
        "3. 返回操作結果"
    ],
    show_tool_calls=True
)

def main():
    print("智能助理已啟動！(輸入 'exit' 結束程式)")
    print("您可以：")
    print("1. 查看台北市天氣 (輸入：'台北市今天的溫度範圍？')")
    
    while True:
        user_input = input("\n請輸入指令: ").strip()
        
        if user_input.lower() == 'exit':
            print("程式已結束")
            break
            
        try:
            response = agent_team.run(user_input, stream=False)
            
            for message in response.messages:
                if message.role == "assistant" and message.content:
                    print("\n助理回應:", message.content.strip())
                    
        except Exception as e:
            print(f"\n錯誤：{str(e)}")

if __name__ == "__main__":
    main()
