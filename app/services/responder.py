from .nlp import normalize

def _is_status_request(text: str) -> bool:
    t = normalize(text)
    keys = ['status', 'andamento', 'progresso', 'atualiza', 'prazo', 'previsão', 'previsao', 'quando']
    return any(k in t for k in keys)

def _mentions_attachment(text: str) -> bool:
    t = normalize(text)
    keys = ['anexo', 'segue em anexo', 'arquivo em anexo', 'comprovante', 'nota fiscal', 'nfe','nf']
    return any(k in t for k in keys)

def suggest_response(text: str, category: str) -> str:
    if category.lower().startswith('produt'):
        base = []
        if _is_status_request(text):
            base.append(
                "Olá! Obrigado pela mensagem. Verifiquei seu pedido/solicitação e estamos acompanhando internamente. "
                "O prazo estimado de atualização é de *X dias úteis*. Assim que houver novidade, retornaremos neste mesmo canal."
            )
        else:
            base.append(
                "Olá! Obrigado pelo contato. Encaminhei sua solicitação para a equipe responsável e abrimos o chamado Nº *XXXX*. "
                "Se possível, detalhe o contexto (prints, horários, impacto) para agilizar a análise."
            )
        if _mentions_attachment(text):
            base.append("Observamos o arquivo em anexo e iremos considerá-lo na análise.")
        base.append("Qualquer dúvida, fico à disposição.")
        return "\n\n".join(base)
    else:
        return (
            "Olá! Agradecemos sua mensagem. Registramos seu contato. "
            "Se precisar de algo adicional ou de suporte, pode responder a este email."
        )
