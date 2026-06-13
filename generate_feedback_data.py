
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_feedback_data(num_records=100):
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)

    channels = ['Aplicativo', 'Telefone', 'Chatbot', 'Agência', 'Internet Banking']
    products = ['Aplicativo bancário', 'PIX', 'Cartão de crédito', 'Empréstimos', 'Atendimento humano', 'Chatbots', 'Internet Banking', 'Segurança e autenticação', 'Processos de contestação', 'Abertura de contas']
    satisfaction_scores = [1, 2, 3, 4, 5]
    service_types = ['Suporte Técnico', 'Financeiro', 'Informações', 'Reclamação', 'Elogio']
    regions = ['Sudeste', 'Sul', 'Centro-Oeste', 'Nordeste', 'Norte']
    statuses = ['Resolvido', 'Em Andamento', 'Pendente', 'Cancelado']

    feedback_templates = {
        'Aplicativo bancário': [
            'O aplicativo está muito lento e trava constantemente.',
            'Não consigo acessar minha conta pelo app, sempre dá erro.',
            'Adorei a nova interface do aplicativo, ficou muito mais fácil de usar.',
            'A função de pagamento de contas no app é excelente!',
            'Falta a opção de [funcionalidade] no aplicativo.',
            'O app consumiu muitos dados do meu celular.',
            'Atualização do app resolveu vários problemas de lentidão.',
            'Poderia ter um dark mode no aplicativo.',
            'Não consigo fazer PIX pelo aplicativo, dá erro 500.',
            'O aplicativo é intuitivo e rápido, parabéns!'
        ],
        'PIX': [
            'Meu PIX não caiu na conta, preciso de ajuda urgente!',
            'A transação PIX foi estornada sem motivo.',
            'PIX funciona perfeitamente, muito rápido e prático.',
            'Tive problemas para cadastrar a chave PIX.',
            'A segurança do PIX é ótima, me sinto seguro.',
            'Demora para o PIX ser processado em alguns momentos.',
            'Não consigo ver o comprovante do PIX no histórico.',
            'PIX é a melhor coisa que inventaram para transferências.',
            'Cai em um golpe de PIX, o banco pode ajudar?',
            'A opção de agendamento de PIX é muito útil.'
        ],
        'Cartão de crédito': [
            'Minha fatura do cartão de crédito veio com cobranças indevidas.',
            'Não consigo aumentar o limite do meu cartão.',
            'O programa de pontos do cartão é muito bom.',
            'Atendimento sobre o cartão foi demorado e ineficaz.',
            'Bloqueei meu cartão e o desbloqueio foi rápido.',
            'Anuidade do cartão é muito alta.',
            'Recebi um cartão que não solicitei.',
            'O cartão virtual é uma mão na roda para compras online.',
            'Fui clonado e o banco não me ajudou com o estorno.',
            'O aplicativo para gerenciar o cartão é excelente.'
        ],
        'Empréstimos': [
            'Aprovação do empréstimo demorou demais.',
            'As taxas de juros do empréstimo são abusivas.',
            'Consegui um empréstimo com ótimas condições.',
            'Não consigo simular empréstimo pelo site.',
            'O processo de contratação de empréstimo é muito burocrático.',
            'Atendimento sobre empréstimo foi muito claro e objetivo.',
            'Recebi uma oferta de empréstimo que não me interessa.',
            'O simulador de empréstimos é fácil de usar.',
            'Preciso renegociar meu empréstimo, as parcelas estão pesadas.',
            'O banco me ajudou a conseguir o empréstimo que eu precisava.'
        ],
        'Atendimento humano': [
            'Fui muito bem atendido pela gerente da agência.',
            'O tempo de espera no telefone é inaceitável.',
            'O atendente não resolveu meu problema, tive que ligar de novo.',
            'Atendimento humano sempre prestativo e eficiente.',
            'Falta treinamento para os atendentes, são despreparados.',
            'Consegui resolver tudo com o atendimento via chat.',
            'O atendimento presencial é o melhor, resolvem tudo na hora.',
            'A fila para atendimento na agência é enorme.',
            'O atendente foi muito educado e paciente.',
            'Não consigo falar com um atendente, só robô.'
        ],
        'Chatbots': [
            'O chatbot não entende minhas perguntas, é inútil.',
            'Consegui resolver meu problema rapidamente com o chatbot.',
            'O chatbot só me joga para o atendimento humano.',
            'O chatbot é muito inteligente e me ajudou muito.',
            'As opções do chatbot são limitadas.',
            'O chatbot me deu informações erradas.',
            'Chatbot é prático para dúvidas simples.',
            'Poderia ter mais opções de autoatendimento no chatbot.',
            'O chatbot é confuso e não me leva a lugar nenhum.',
            'Gostei da agilidade do chatbot para resolver meu problema.'
        ],
        'Internet Banking': [
            'O Internet Banking é muito seguro e fácil de usar.',
            'Não consigo fazer transferências pelo Internet Banking.',
            'O site do banco está fora do ar com frequência.',
            'Adorei a nova funcionalidade de investimentos no Internet Banking.',
            'A interface do Internet Banking é antiga e pouco intuitiva.',
            'Tive problemas para acessar o Internet Banking com a senha.',
            'O Internet Banking é completo e atende todas as minhas necessidades.',
            'Falta um chat de suporte no Internet Banking.',
            'O site é lento e trava muito.',
            'Consegui pagar minhas contas rapidamente pelo Internet Banking.'
        ],
        'Segurança e autenticação': [
            'Minha conta foi invadida, preciso de ajuda urgente com a segurança!',
            'O sistema de autenticação de dois fatores é muito seguro.',
            'Tive problemas para validar minha identidade no aplicativo.',
            'A segurança do banco é excelente, me sinto protegido.',
            'Recebi um SMS falso do banco, cuidado com golpes.',
            'O reconhecimento facial para login é muito prático.',
            'Demora para receber o código de segurança por SMS.',
            'Acho que a segurança do banco precisa ser melhorada.',
            'Fui vítima de fraude, o banco pode me ajudar?',
            'As dicas de segurança do banco são muito úteis.'
        ],
        'Processos de contestação': [
            'Meu processo de contestação está parado há semanas.',
            'Consegui contestar uma compra indevida rapidamente.',
            'O processo de contestação é muito burocrático e demorado.',
            'Atendimento sobre contestação foi muito atencioso.',
            'Não consigo acompanhar o status da minha contestação.',
            'O banco resolveu minha contestação em poucos dias.',
            'Falta clareza sobre os documentos necessários para contestação.',
            'O processo de contestação online é muito prático.',
            'Tive que ir na agência para resolver a contestação.',
            'O banco não me deu retorno sobre minha contestação.'
        ],
        'Abertura de contas': [
            'Abertura de conta online foi muito rápida e fácil.',
            'Tive problemas para enviar os documentos na abertura de conta.',
            'O processo de abertura de conta é muito demorado.',
            'Atendimento para abertura de conta foi excelente.',
            'Não consigo finalizar a abertura da minha conta.',
            'A abertura de conta digital é muito prática.',
            'Falta clareza sobre os requisitos para abrir uma conta.',
            'O banco me ajudou a abrir a conta que eu precisava.',
            'Recebi um email de confirmação de abertura de conta que não fiz.',
            'O processo de abertura de conta é muito intuitivo.'
        ]
    }

    data = []
    for _ in range(num_records):
        date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        channel = random.choice(channels)
        product = random.choice(products)
        
        # Ensure feedback text is relevant to the product
        comment = random.choice(feedback_templates.get(product, ['Comentário genérico sobre o banco.']))

        satisfaction = random.choice(satisfaction_scores)
        service_type = random.choice(service_types)
        region = random.choice(regions)
        status = random.choice(statuses)

        data.append([
            date.strftime('%Y-%m-%d'),
            channel,
            comment,
            product,
            satisfaction,
            service_type,
            region,
            status
        ])

    df = pd.DataFrame(data, columns=[
        'Data do feedback',
        'Canal de origem',
        'Texto do comentário',
        'Produto ou serviço citado',
        'Nota de satisfação (1 a 5)',
        'Tipo de atendimento',
        'Região',
        'Status da solicitação'
    ])
    return df

if __name__ == '__main__':
    df = generate_feedback_data(num_records=200) # Generate 200 records
    df.to_csv('banking_feedback.csv', index=False)
    print('Generated banking_feedback.csv with 200 records.')
