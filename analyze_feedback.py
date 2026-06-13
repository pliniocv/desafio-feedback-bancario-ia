
import pandas as pd
import re

def classify_feedback(comment, product):
    comment_lower = comment.lower()
    theme = product # Default theme is the product cited
    sentiment = "Neutro"
    urgency = "Baixa"
    impact = "Baixo"

    # Sentiment Classification
    positive_keywords = ["adorei", "excelente", "ótimo", "bom", "rápido", "prático", "seguro", "eficiente", "parabéns", "ajudou", "prestativo", "intuitivo", "melhor", "completo", "fácil"]
    negative_keywords = ["lento", "trava", "erro", "não consigo", "falta", "demora", "problemas", "indevidas", "ineficaz", "abusivas", "burocrático", "inaceitável", "inútil", "limitadas", "antiga", "confuso", "fora do ar", "invadida", "fraude", "golpe", "clonado", "parado", "pesadas"]

    if any(keyword in comment_lower for keyword in positive_keywords):
        sentiment = "Positivo"
    elif any(keyword in comment_lower for keyword in negative_keywords):
        sentiment = "Negativo"

    # Urgency Classification
    urgent_keywords = ["urgente", "preciso", "agora", "imediatamente", "inaceitável", "demora demais", "parado há semanas"]
    if any(keyword in comment_lower for keyword in urgent_keywords):
        urgency = "Alta"
    elif "demora" in comment_lower or "problemas" in comment_lower or "não consigo" in comment_lower:
        urgency = "Média"

    # Impact Classification
    high_impact_keywords = ["invadida", "fraude", "golpe", "clonado", "segurança", "cobranças indevidas", "estornada sem motivo", "não caiu na conta"]
    medium_impact_keywords = ["não consigo acessar", "travando", "lento", "fora do ar", "erro", "burocrático", "demorado"]

    if any(keyword in comment_lower for keyword in high_impact_keywords):
        impact = "Alto"
    elif any(keyword in comment_lower for keyword in medium_impact_keywords):
        impact = "Médio"

    # Refine Theme based on comment content for more specific themes and ensure consistency
    if "app" in comment_lower or "aplicativo" in comment_lower:
        theme = "Aplicativo Bancário"
    elif "pix" in comment_lower:
        theme = "PIX"
    elif "cartão" in comment_lower or "fatura" in comment_lower or "limite" in comment_lower or "anuidade" in comment_lower:
        theme = "Cartão de Crédito"
    elif "empréstimo" in comment_lower or "juros" in comment_lower or "parcelas" in comment_lower:
        theme = "Empréstimos"
    elif "atendimento" in comment_lower or "gerente" in comment_lower or "espera" in comment_lower or "atendente" in comment_lower:
        theme = "Atendimento Humano"
    elif "chatbot" in comment_lower:
        theme = "Chatbots"
    elif "internet banking" in comment_lower or "site" in comment_lower:
        theme = "Internet Banking"
    elif "segurança" in comment_lower or "autenticação" in comment_lower or "senha" in comment_lower or "invasão" in comment_lower or "fraude" in comment_lower:
        theme = "Segurança e Autenticação"
    elif "contestação" in comment_lower:
        theme = "Processos de Contestação"
    elif "abertura de conta" in comment_lower or "conta" in comment_lower:
        theme = "Abertura de Contas"
    
    # Normalize theme names to avoid duplicates due to case or slight variations
    theme = theme.replace("Cartão de crédito", "Cartão de Crédito")

    return theme, sentiment, urgency, impact

def analyze_feedback_data(df):
    df[["Tema principal", "Sentimento", "Urgência", "Impacto potencial"]] = df.apply(
        lambda row: pd.Series(classify_feedback(row["Texto do comentário"], row["Produto ou serviço citado"])), axis=1
    )

    # --- Resumo Executivo ---
    total_feedbacks = len(df)
    positive_count = df[df["Sentimento"] == "Positivo"].shape[0]
    negative_count = df[df["Sentimento"] == "Negativo"].shape[0]
    neutral_count = df[df["Sentimento"] == "Neutro"].shape[0]

    most_frequent_theme = df["Tema principal"].mode()[0]
    
    # Handle cases where there might not be negative or positive feedbacks for a specific theme
    most_frequent_complaint_theme = df[df["Sentimento"] == "Negativo"]["Tema principal"].mode()[0] if not df[df["Sentimento"] == "Negativo"].empty else "Nenhum tema de reclamação predominante"
    most_frequent_praise_theme = df[df["Sentimento"] == "Positivo"]["Tema principal"].mode()[0] if not df[df["Sentimento"] == "Positivo"].empty else "Nenhum tema de elogio predominante"

    executive_summary = f"""
    **Resumo Executivo**

    A análise de {total_feedbacks} feedbacks bancários revela que o sentimento geral dos clientes é predominantemente **{df["Sentimento"].mode()[0].lower()}**. Os principais temas recorrentes incluem **{most_frequent_theme}**, com destaque para **{most_frequent_complaint_theme}** como a principal fonte de reclamações e **{most_frequent_praise_theme}** como o tema mais elogiado. Foram identificados riscos significativos relacionados à segurança e processos burocráticos, enquanto oportunidades de melhoria se concentram na otimização de canais digitais e atendimento. A urgência em resolver questões de segurança e acesso é alta, impactando diretamente a confiança do cliente.
    """

    # --- Tabela de Insights ---
    insights_data = []
    for theme in df["Tema principal"].unique():
        theme_df = df[df["Tema principal"] == theme]
        
        # Get most frequent sentiment, urgency, impact for the theme
        sentiment = theme_df["Sentimento"].mode()[0] if not theme_df.empty else "N/A"
        urgency = theme_df["Urgência"].mode()[0] if not theme_df.empty else "N/A"
        impact = theme_df["Impacto potencial"].mode()[0] if not theme_df.empty else "N/A"

        # Get a representative evidence (e.g., a negative comment if available, else a positive, else any)
        evidence_comment = "Nenhuma evidência clara."
        if not theme_df[theme_df["Sentimento"] == "Negativo"].empty:
            evidence_comment = theme_df[theme_df["Sentimento"] == "Negativo"]["Texto do comentário"].iloc[0]
        elif not theme_df[theme_df["Sentimento"] == "Positivo"].empty:
            evidence_comment = theme_df[theme_df["Sentimento"] == "Positivo"]["Texto do comentário"].iloc[0]
        elif not theme_df.empty:
            evidence_comment = theme_df["Texto do comentário"].iloc[0]

        # More specific action recommendation based on sentiment and impact
        action_recommended = "Revisar processos e comunicação."
        if sentiment == "Negativo" and impact == "Alto":
            action_recommended = "Priorizar correção imediata, investigar causa raiz e comunicar proativamente as ações."
        elif sentiment == "Negativo" and impact == "Médio":
            action_recommended = "Analisar fluxo de jornada, otimizar pontos de contato e treinar equipes."
        elif sentiment == "Positivo" and impact == "Alto":
            action_recommended = "Identificar e replicar melhores práticas, fortalecer campanhas de marketing."
        elif sentiment == "Positivo" and impact == "Médio":
            action_recommended = "Manter a qualidade, buscar inovação contínua e coletar mais feedbacks positivos."
        elif sentiment == "Neutro":
            action_recommended = "Pesquisar mais a fundo para entender a percepção do cliente e identificar oportunidades."

        insights_data.append({"Tema": theme, "Sentimento": sentiment, "Urgência": urgency, "Impacto": impact, "Evidência": evidence_comment, "Ação Recomendada": action_recommended})

    insights_df = pd.DataFrame(insights_data)
    insights_table = insights_df.to_markdown(index=False)

    # --- Ranking de Prioridades ---
    priority_mapping = {"Baixa": 1, "Média": 2, "Alta": 3}
    impact_mapping = {"Baixo": 1, "Médio": 2, "Alto": 3}
    
    # Ensure consistency in theme names before grouping
    df["Tema principal"] = df["Tema principal"].apply(lambda x: x.replace("Cartão de crédito", "Cartão de Crédito"))

    df["Impacto Score"] = df["Impacto potencial"].map(impact_mapping).fillna(0)
    df["Urgência Score"] = df["Urgência"].map(priority_mapping).fillna(0)
    df["Priority Score"] = df["Impacto Score"] + df["Urgência Score"]

    print("\n--- Debugging Priority Scores ---")
    print("df[\"Impacto potencial\"] unique values:", df["Impacto potencial"].unique())
    print("df[\"Urgência\"] unique values:", df["Urgência"].unique())
    print("df[\"Impacto Score\"] head:\n", df[["Impacto potencial", "Impacto Score"]].head())
    print("df[\"Urgência Score\"] head:\n", df[["Urgência", "Urgência Score"]].head())
    print("df[\"Priority Score\"] head:\n", df[["Impacto Score", "Urgência Score", "Priority Score"]].head())
    print("----------------------------------\n")

    # Group by theme and sum scores to get an overall priority for each theme
    theme_priority = df.groupby("Tema principal")["Priority Score"].sum().reset_index()
    theme_priority = theme_priority.sort_values(by="Priority Score", ascending=False).head(5)

    ranking_priorities = "**Ranking de Prioridades**\n\n"
    for index, row in theme_priority.iterrows():
        ranking_priorities += f"- {row["Tema principal"]} (Pontuação de Prioridade: {int(row["Priority Score"])})\n"

    # --- Recomendações Estratégicas ---
    strategic_recommendations = "**Recomendações Estratégicas**\n\n"
    for index, row in theme_priority.iterrows():
        theme = row["Tema principal"]
        # Get representative data for the theme
        theme_df = df[df["Tema principal"] == theme]
        
        # Try to get a negative problem example first, otherwise a general one
        problem_examples = theme_df[theme_df["Sentimento"] == "Negativo"]["Texto do comentário"].head(1).tolist()
        problem_identified = problem_examples[0] if problem_examples else f"Problemas gerais relacionados a {theme}."

        possible_impact = "Redução da satisfação do cliente e possível churn."
        if theme == "Segurança e Autenticação":
            possible_impact = "Perda de confiança, fraudes financeiras e danos à reputação da marca."
        elif theme == "Aplicativo Bancário" or theme == "Internet Banking":
            possible_impact = "Frustração do usuário, abandono de transações, percepção de obsolescência e perda de competitividade."
        elif theme == "Atendimento Humano":
            possible_impact = "Insatisfação com o suporte, retrabalho, sobrecarga de canais e impacto negativo na imagem do banco."
        elif theme == "PIX":
            possible_impact = "Perda de agilidade nas transações, insatisfação e busca por alternativas."
        elif theme == "Cartão de Crédito":
            possible_impact = "Perda de clientes, aumento de contestações e custos operacionais."
        elif theme == "Empréstimos":
            possible_impact = "Perda de oportunidades de negócio, insatisfação e busca por concorrentes."
        elif theme == "Processos de Contestação":
            possible_impact = "Frustração do cliente, perda de confiança e aumento de reclamações em órgãos reguladores."
        elif theme == "Abertura de Contas":
            possible_impact = "Perda de novos clientes, burocracia percebida e impacto na expansão da base."
        elif theme == "Chatbots":
            possible_impact = "Frustração do cliente, percepção de ineficiência e sobrecarga do atendimento humano."

        recommendation = insights_df[insights_df["Tema"] == theme]["Ação Recomendada"].iloc[0]
        benefit_expected = "Melhoria na experiência do cliente e fidelização."
        if theme == "Segurança e Autenticação":
            benefit_expected = "Aumento da confiança, redução de fraudes, fortalecimento da imagem da marca e conformidade regulatória."
        elif theme == "Aplicativo Bancário" or theme == "Internet Banking":
            benefit_expected = "Maior engajamento, satisfação do cliente, agilidade nas transações e diferenciação no mercado."
        elif theme == "Atendimento Humano":
            benefit_expected = "Aumento da satisfação, resolução eficaz de problemas, redução de custos operacionais e fortalecimento do relacionamento."
        elif theme == "PIX":
            benefit_expected = "Agilidade e segurança nas transações, satisfação do cliente e competitividade."
        elif theme == "Cartão de Crédito":
            benefit_expected = "Redução de atritos, aumento da satisfação, retenção de clientes e otimização de custos."
        elif theme == "Empréstimos":
            benefit_expected = "Aumento da captação de clientes, satisfação e crescimento da carteira de crédito."
        elif theme == "Processos de Contestação":
            benefit_expected = "Agilidade na resolução, aumento da confiança e redução de reclamações."
        elif theme == "Abertura de Contas":
            benefit_expected = "Aumento da base de clientes, agilidade no onboarding e melhoria da primeira impressão."
        elif theme == "Chatbots":
            benefit_expected = "Resolução rápida de dúvidas, redução da carga do atendimento humano e melhoria da experiência digital."

        strategic_recommendations += f"**Tema: {theme}**\n"
        strategic_recommendations += f"- **Problema identificado:** {problem_identified}\n"
        strategic_recommendations += f"- **Possível impacto:** {possible_impact}\n"
        strategic_recommendations += f"- **Recomendação:** {recommendation}\n"
        strategic_recommendations += f"- **Benefício esperado:** {benefit_expected}\n\n"

    return executive_summary, insights_table, ranking_priorities, strategic_recommendations

if __name__ == '__main__':
    try:
        df = pd.read_csv('banking_feedback.csv')
        executive_summary, insights_table, ranking_priorities, strategic_recommendations = analyze_feedback_data(df)

        with open('feedback_analysis_report.md', 'w', encoding='utf-8') as f:
            f.write(executive_summary)
            f.write("\n\n")
            f.write("**Tabela de Insights**\n\n")
            f.write(insights_table)
            f.write("\n\n")
            f.write(ranking_priorities)
            f.write("\n\n")
            f.write(strategic_recommendations)
        print("Analysis report generated successfully: feedback_analysis_report.md")

    except FileNotFoundError:
        print("Error: banking_feedback.csv not found. Please ensure the data generation script was run first.")
    except Exception as e:
        print(f"An error occurred during analysis: {e}")
