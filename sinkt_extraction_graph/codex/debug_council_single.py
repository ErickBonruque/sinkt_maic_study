import os
import json
from typing import Literal, Optional, List
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

# --- CONFIGURAÇÃO SIMPLIFICADA ---
# Vamos usar o mesmo modelo para tudo para testar a lógica
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Estruturas de Dados
class AgentVote(BaseModel):
    agent: str
    verdict: Literal['APPROVE', 'REJECT', 'MODIFY', 'ABSTAIN']
    suggested_type: Optional[str] = None
    reason: str

class EdgeState(BaseModel):
    source: str
    target: str
    source_type: str
    target_type: str
    current_type: Optional[str] = "RELATED_TO"
    similarity_score: float
    votes: List[AgentVote] = []

# --- AGENTES (Copiados do Notebook) ---

def run_debug_test(source, target, s_type, t_type):
    print(f"\n{'='*50}")
    print(f"🔎 TESTANDO PAR: {source} -> {target}")
    print(f"{'='*50}")
    
    state = EdgeState(source=source, target=target, source_type=s_type, target_type=t_type, similarity_score=0.95)
    
    # 1. CLEANER
    print("\n--- 1. CLEANER ---")
    prompt_cleaner = ChatPromptTemplate.from_template(
        """Você é o CLEANER. Analise: {source} ({source_type}) -> {target} ({target_type}).
        Vote REJECT se for alucinação ou lixo. Caso contrário, ABSTAIN.
        Responda apenas com o veredito e razão breve."""
    )
    res_cleaner = llm.invoke(prompt_cleaner.format(source=source, source_type=s_type, target=target, target_type=t_type, score=0.9))
    print(f"RAW OUTPUT: {res_cleaner.content}")
    
    verdict_cleaner = 'REJECT' if 'REJECT' in res_cleaner.content.upper() else 'ABSTAIN'
    state.votes.append(AgentVote(agent="Cleaner", verdict=verdict_cleaner, reason=res_cleaner.content))
    
    if verdict_cleaner == 'REJECT':
        print("❌ REJEITADO PELO CLEANER")
        return

    # 2. EXPERT
    print("\n--- 2. EXPERT ---")
    prompt_expert = ChatPromptTemplate.from_template(
        """Você é o ESPECIALISTA. Analise: {source} -> {target}.
        Vote REJECT, APPROVE ou MODIFY (com sugestão PREREQUISITE, USE, PART_OF).
        Explique."""
    )
    res_expert = llm.invoke(prompt_expert.format(source=source, target=target))
    print(f"RAW OUTPUT: {res_expert.content}")
    
    content_ex = res_expert.content.upper()
    v_ex = 'APPROVE'
    s_ex = None
    if 'REJECT' in content_ex: v_ex = 'REJECT'
    elif 'PREREQUISITE' in content_ex: v_ex, s_ex = 'MODIFY', 'PREREQUISITE'
    elif 'USE' in content_ex: v_ex, s_ex = 'MODIFY', 'USE'
    elif 'PART_OF' in content_ex: v_ex, s_ex = 'MODIFY', 'PART_OF'
    
    state.votes.append(AgentVote(agent="Expert", verdict=v_ex, suggested_type=s_ex, reason=res_expert.content))

    # 3. ANALYST
    print("\n--- 3. ANALYST ---")
    prompt_analyst = ChatPromptTemplate.from_template(
        """Você é o ANALISTA. Analise consistência lógica: {source} -> {target}.
        Vote REJECT se for ilógico (ciclo, tipos errados). Senão APPROVE."""
    )
    res_analyst = llm.invoke(prompt_analyst.format(source=source, source_type=s_type, target=target, target_type=t_type))
    print(f"RAW OUTPUT: {res_analyst.content}")
    
    v_an = 'REJECT' if 'REJECT' in res_analyst.content.upper() else 'APPROVE'
    state.votes.append(AgentVote(agent="Analyst", verdict=v_an, reason=res_analyst.content))

    # 4. JUDGE
    print("\n--- 4. JUDGE (O MOMENTO DA VERDADE) ---")
    
    class JudgeVerdict(BaseModel):
        final_action: Literal['KEEP', 'DISCARD']
        final_type: str
        rationale: str

    votes_str = "\n".join([f"- {v.agent}: {v.verdict} ({v.suggested_type or 'N/A'}) -> {v.reason}" for v in state.votes])
    print(f"VOTOS APRESENTADOS AO JUIZ:\n{votes_str}")
    
    parser = PydanticOutputParser(pydantic_object=JudgeVerdict)
    
    prompt_judge = ChatPromptTemplate.from_messages([
        ("system", "Você é o JUIZ SUPREMO. Decida o destino da aresta."),
        ("user", """Decida: {source} -> {target}
        VOTOS:
        {votes}
        
        Retorne JSON compatível.
        {format_instructions}
        """)
    ])
    
    try:
        res_judge = llm.invoke(prompt_judge.format(
            source=source, target=target, votes=votes_str,
            format_instructions=parser.get_format_instructions()
        ))
        print(f"\nRAW JSON OUTPUT: {res_judge.content}")
        
        verdict = parser.parse(res_judge.content)
        print(f"\n⚖️ VEREDITO FINAL: {verdict.final_action}")
        print(f"📝 TIPO: {verdict.final_type}")
        print(f"🤔 RAZÃO: {verdict.rationale}")
        
    except Exception as e:
        print(f"\n💥 ERRO DE PARSING NO JUIZ: {e}")

# Executar testes
if __name__ == "__main__":
    # Teste 1: Caso Óbvio (Deveria Aprovar)
    run_debug_test("Kernel", "Linux", "CONCEITO_TEORICO", "CONCEITO_TEORICO")
    
    # Teste 2: Caso Duvidoso (Talvez Rejeite)
    # run_debug_test("cat", "echo", "COMANDO", "COMANDO")
