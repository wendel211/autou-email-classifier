import os
import re
import json
from typing import Dict
from .nlp import tokenize, normalize

# Palavras-chave por categoria
PRODUCTIVE_HINTS = {
    'status','atualização','atualizacao','progresso','prazo','prazo?','suporte','erro','falha','bug',
    'chamado','ticket','caso','protocolo','anexo','comprovante','nota','nf','nfe','documento',
    'solicito','solicitação','solicitacao','pedido','urgente','pendente','pendência','pendencia','resolvido',
    'homologação','homologacao','produção','producao','liberação','liberacao','acesso','cadastro','senha'
}
UNPRODUCTIVE_HINTS = {
    'obrigado','agradeço','agradecemos','agradecimento','feliz','natal','parabéns','parabens','boas','festas',
    'bom','dia','boa','tarde','boa','noite','atenciosamente','recebido','ok','valeu','abraços','abç'
}

def rule_based(text: str) -> Dict:
    tokens = set(tokenize(text))
    p = len(tokens & PRODUCTIVE_HINTS)
    u = len(tokens & UNPRODUCTIVE_HINTS)
    if p == 0 and u == 0:
        # fallback: heurística pelo conteúdo
        p = 1 if any(k in normalize(text) for k in ['status','suporte','erro','ticket','protocolo']) else 0
        u = 1 if any(k in normalize(text) for k in ['obrig','parab','feliz','bom dia','boas festas']) else 0
    if p >= u:
        cat = 'Produtivo'
        conf = min(0.5 + p*0.1, 0.95)
    else:
        cat = 'Improdutivo'
        conf = min(0.5 + u*0.1, 0.95)
    return {'category': cat, 'confidence': round(conf, 3), 'strategy': 'rules'}

def openai_available() -> bool:
    key = os.getenv('OPENAI_API_KEY')
    print(">>> DEBUG: OPENAI_API_KEY lido:", key[:8] + "..." if key else "NÃO ENCONTRADO")
    return bool(key)

def openai_classify_and_respond(text: str) -> Dict:
    from openai import OpenAI
    client = OpenAI()

    sys_prompt = (
        "Você é um assistente de triagem de emails corporativos. "
        "Classifique cada email como 'Produtivo' ou 'Improdutivo'. "
        "Responda **somente** em JSON válido, neste formato exato:\n"
        "{\"category\": \"Produtivo ou Improdutivo\", \"response\": \"resposta em pt-BR\"}\n"
        "Não escreva nada além do JSON."
    )

    user_prompt = f"Email:\n\n{text}\n\nResponda APENAS no formato JSON válido pedido."

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
        )
        content = resp.choices[0].message.content.strip()
        print(">>> DEBUG: Resposta bruta da OpenAI:", content)

        # Tenta parsear direto
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            print(">>> DEBUG: JSON inválido, tentando extrair com regex...")
            match = re.search(r"\{.*\}", content, re.S)
            if match:
                data = json.loads(match.group())
            else:
                raise

        cat = data.get('category', 'Produtivo').strip()
        sug = data.get('response', '').strip()

        return {
            'category': cat,
            'confidence': 0.95,
            'strategy': 'openai',
            'response': sug
        }

    except Exception as e:
        print(">>> ERRO OpenAI:", str(e))
        # fallback para regra
        out = rule_based(text)
        return {
            **out,
            'strategy': out.get('strategy', 'rules') + '+fallback',
            'error': str(e)
        }

def classify_email(text: str) -> Dict:
    if openai_available():
        return openai_classify_and_respond(text)
    print(">>> DEBUG: OpenAI indisponível, usando regras.")
    return rule_based(text)
