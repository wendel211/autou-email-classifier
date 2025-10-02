from openai import OpenAI
import os

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ ERRO: OPENAI_API_KEY não está definida no ambiente.")
        return

    print("✅ Chave encontrada, testando chamada...")

    try:
        client = OpenAI()

        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Responda APENAS este JSON: {\"category\": \"Produtivo\", \"response\": \"ok\"}"},
                {"role": "user", "content": "teste"}
            ],
            temperature=0.2
        )

        print(">>> Resposta crua da API:")
        print(resp.choices[0].message.content)

    except Exception as e:
        print("❌ Erro na chamada OpenAI:", str(e))

if __name__ == "__main__":
    main()
