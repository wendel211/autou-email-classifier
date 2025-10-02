from app.services.classifier import rule_based

def test_rule_based_produtivo():
    text = 'Poderia informar o status do chamado? Segue anexo o comprovante.'
    out = rule_based(text)
    assert out['category'] == 'Produtivo'

def test_rule_based_improdutivo():
    text = 'Feliz Natal e boas festas! Obrigado.'
    out = rule_based(text)
    assert out['category'] == 'Improdutivo'
