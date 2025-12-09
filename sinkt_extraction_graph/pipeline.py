"""Pipeline executável para gerar o grafo de conhecimento do SINKT.

Este script substitui a versão anterior baseada em anotações e garante
uma execução sequencial única: carrega os artefatos de extração, aplica
uma mesa redonda de 8 agentes com heurísticas de densificação, trata nós
órfãos e exporta o grafo final com relatórios de qualidade.
"""
from __future__ import annotations

import datetime as _dt
import json
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

BASE_RELATION_TYPES = {
    "definition",
    "prerequisite",
    "property",
    "part-of",
    "including",
    "related",
}

RELATION_ALIASES = {
    "RELATED": "related",
    "RELATION": "related",
    "INCLUDES": "including",
    "INCLUDE": "including",
    "PART_OF": "part-of",
    "PARTOF": "part-of",
    "PREREQ": "prerequisite",
    "PREREQUISITE": "prerequisite",
    "DEFINITION": "definition",
    "PROPERTY": "property",
}

DEFAULT_TYPE = "CONCEITO_TEORICO"


def _canonical_name(text: str) -> str:
    return " ".join(text.strip().lower().replace("_", " ").split())


def _jaccard(a: str, b: str) -> float:
    set_a = set(a.split())
    set_b = set(b.split())
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)


def _unique_relations(relations: Iterable["Relation"]) -> List["Relation"]:
    seen: Set[Tuple[str, str, str]] = set()
    deduped: List[Relation] = []
    for rel in relations:
        key = (rel.source, rel.target, rel.type)
        if key not in seen:
            seen.add(key)
            deduped.append(rel)
    return deduped


@dataclass
class Concept:
    nome: str
    tipo: str
    definicao: str
    capitulo_origem: str
    caminho: Optional[str] = None
    evidencias: List[str] = field(default_factory=list)

    def canonical(self) -> str:
        return _canonical_name(self.nome)


@dataclass
class Relation:
    source: str
    target: str
    type: str
    explanation: Optional[str] = None
    confidence: float = 0.6
    strategy: str = "lexical"


@dataclass
class GraphState:
    concepts: Dict[str, Concept]
    relations: List[Relation]
    audit_trail: List[str] = field(default_factory=list)

    def log(self, message: str) -> None:
        timestamp = _dt.datetime.utcnow().isoformat()
        self.audit_trail.append(f"[{timestamp}] {message}")


@dataclass
class PipelineConfig:
    base_dir: Path = Path(__file__).resolve().parent
    pdf_path: Path = Path(__file__).resolve().parent / "pdf" / "linux.pdf"
    raw_concepts_path: Path = Path(__file__).resolve().parent / "output" / "01_extraction" / "concepts_map.json"
    raw_relations_path: Path = Path(__file__).resolve().parent / "output" / "01_extraction" / "relations_initial.json"
    ontology_map_path: Path = Path(__file__).resolve().parent / "output" / "01_extraction" / "ontology_map.json"
    densified_output: Path = Path(__file__).resolve().parent / "output" / "02_densification" / "enhanced_graph.json"
    final_output: Path = Path(__file__).resolve().parent / "output" / "03_final_audit" / "final_sinkt_graph.json"
    quality_report: Path = Path(__file__).resolve().parent / "output" / "graph_quality_report.json"

    def ensure_dirs(self) -> None:
        for path in [
            self.densified_output.parent,
            self.final_output.parent,
            self.quality_report.parent,
        ]:
            path.mkdir(parents=True, exist_ok=True)


class RoundTableAgent:
    name: str = "agent"

    def contribute(self, state: GraphState, context: Dict) -> GraphState:  # pragma: no cover - interface
        raise NotImplementedError


class ModeratorAgent(RoundTableAgent):
    name = "Moderador"

    def contribute(self, state: GraphState, context: Dict) -> GraphState:
        state.log("Mesa redonda iniciada com 8 agentes.")
        return state


class CleanerAgent(RoundTableAgent):
    name = "Cleaner"

    def contribute(self, state: GraphState, context: Dict) -> GraphState:
        by_canonical: Dict[str, Concept] = {}
        for concept in state.concepts.values():
            key = concept.canonical()
            if key not in by_canonical:
                by_canonical[key] = concept
            else:
                existing = by_canonical[key]
                if concept.definicao and concept.definicao not in existing.definicao:
                    existing.definicao += f" | {concept.definicao}"
                existing.evidencias.extend(concept.evidencias)
        state.concepts = by_canonical
        state.relations = [
            rel
            for rel in state.relations
            if _canonical_name(rel.source) in state.concepts
            and _canonical_name(rel.target) in state.concepts
            and rel.source != rel.target
        ]
        state.log(f"Cleaner consolidou conceitos em {len(state.concepts)} nós únicos.")
        return state


class TypeResolverAgent(RoundTableAgent):
    name = "Terminologista"

    def contribute(self, state: GraphState, context: Dict) -> GraphState:
        ontology: Dict[str, str] = context.get("ontology", {})
        for concept in state.concepts.values():
            mapped = ontology.get(concept.nome) or ontology.get(concept.nome.title())
            concept.tipo = mapped or concept.tipo or DEFAULT_TYPE
        state.log("Terminologista aplicou tipagem canônica e fallback.")
        return state


class RelationNormalizerAgent(RoundTableAgent):
    name = "Normalizador de Relações"

    def contribute(self, state: GraphState, context: Dict) -> GraphState:
        normalized: List[Relation] = []
        for rel in state.relations:
            rel_type = RELATION_ALIASES.get(rel.type.upper(), rel.type.lower())
            if rel_type not in BASE_RELATION_TYPES:
                rel_type = "related"
            normalized.append(
                Relation(
                    source=_canonical_name(rel.source),
                    target=_canonical_name(rel.target),
                    type=rel_type,
                    explanation=rel.explanation,
                    confidence=min(max(rel.confidence, 0.0), 1.0),
                    strategy=rel.strategy,
                )
            )
        state.relations = _unique_relations(normalized)
        state.log("Relações normalizadas e deduplicadas.")
        return state


class LexicalLinkerAgent(RoundTableAgent):
    name = "Linker Léxico"

    def __init__(self, threshold: float = 0.32, top_k: int = 6):
        self.threshold = threshold
        self.top_k = top_k

    def contribute(self, state: GraphState, context: Dict) -> GraphState:
        concepts = list(state.concepts.values())
        added: List[Relation] = []
        for i, c1 in enumerate(concepts):
            for c2 in concepts[i + 1 :]:
                sim = _jaccard(c1.canonical(), c2.canonical())
                if sim >= self.threshold:
                    added.append(
                        Relation(
                            source=c1.canonical(),
                            target=c2.canonical(),
                            type="related",
                            confidence=sim,
                            strategy="lexical",
                        )
                    )
        existing_degree = Counter()
        for rel in state.relations + added:
            existing_degree[rel.source] += 1
            existing_degree[rel.target] += 1
        hubs = {
            node for node, deg in existing_degree.most_common() if deg >= max(1, len(concepts) // 50)
        }
        for concept in concepts:
            if concept.canonical() not in hubs:
                continue
            for candidate in concepts:
                if candidate is concept:
                    continue
                added.append(
                    Relation(
                        source=concept.canonical(),
                        target=candidate.canonical(),
                        type="related",
                        confidence=0.41,
                        strategy="hub-propagation",
                    )
                )
                if len(added) > len(concepts) * self.top_k:
                    break
        state.relations = _unique_relations(state.relations + added)
        state.log(f"Linker Léxico adicionou {len(added)} relações para aumentar densidade.")
        return state


class ChapterLinkAgent(RoundTableAgent):
    name = "Estruturador de Capítulos"

    def contribute(self, state: GraphState, context: Dict) -> GraphState:
        anchors: Dict[str, Concept] = {}
        for concept in list(state.concepts.values()):
            chapter = concept.capitulo_origem or "Geral"
            anchor_name = f"capitulo_{chapter}"
            if anchor_name not in state.concepts:
                anchors[anchor_name] = Concept(
                    nome=anchor_name,
                    tipo="CAPITULO",
                    definicao=f"Âncora automática do capítulo {chapter} para reduzir nós órfãos.",
                    capitulo_origem=str(chapter),
                    caminho=f"Capítulo > {chapter}",
                )
        state.concepts.update({c.canonical(): c for c in anchors.values()})
        added: List[Relation] = []
        for concept in state.concepts.values():
            if concept.tipo == "CAPITULO":
                continue
            anchor_key = _canonical_name(f"capitulo_{concept.capitulo_origem or 'Geral'}")
            added.append(
                Relation(
                    source=anchor_key,
                    target=concept.canonical(),
                    type="part-of",
                    confidence=0.55,
                    strategy="chapter-anchor",
                )
            )
        state.relations = _unique_relations(state.relations + added)
        state.log("Estruturador conectou conceitos às âncoras de capítulo.")
        return state


class OrphanRescuerAgent(RoundTableAgent):
    name = "Resgate de Órfãos"

    def __init__(self, min_degree: int = 2):
        self.min_degree = min_degree

    def contribute(self, state: GraphState, context: Dict) -> GraphState:
        degree = Counter()
        for rel in state.relations:
            degree[rel.source] += 1
            degree[rel.target] += 1
        concepts = list(state.concepts.values())
        added: List[Relation] = []
        for concept in concepts:
            if degree.get(concept.canonical(), 0) >= self.min_degree:
                continue
            candidates = sorted(
                concepts,
                key=lambda c: _jaccard(concept.canonical(), c.canonical()),
                reverse=True,
            )
            for candidate in candidates:
                if candidate.canonical() == concept.canonical():
                    continue
                sim = _jaccard(concept.canonical(), candidate.canonical())
                if sim == 0:
                    continue
                added.append(
                    Relation(
                        source=candidate.canonical(),
                        target=concept.canonical(),
                        type="related",
                        confidence=0.45 + sim / 2,
                        strategy="orphan-rescue",
                    )
                )
                if degree.get(concept.canonical(), 0) + len([r for r in added if r.target == concept.canonical()]) >= self.min_degree:
                    break
        state.relations = _unique_relations(state.relations + added)
        state.log(f"Resgate reduziu órfãos com {len(added)} novas relações.")
        return state


class AuditAgent(RoundTableAgent):
    name = "Auditor"

    def contribute(self, state: GraphState, context: Dict) -> GraphState:
        state.relations = _unique_relations(
            rel
            for rel in state.relations
            if rel.source in state.concepts and rel.target in state.concepts
        )
        state.log("Auditoria final aplicada: relações e conceitos sincronizados.")
        return state


class RoundTable:
    def __init__(self, agents: Sequence[RoundTableAgent]):
        if len(agents) != 8:
            raise ValueError("A mesa redonda deve conter exatamente 8 agentes.")
        self.agents = agents

    def run(self, state: GraphState, context: Dict) -> GraphState:
        for agent in self.agents:
            state = agent.contribute(state, context)
        return state


class GraphPipeline:
    def __init__(self, config: Optional[PipelineConfig] = None):
        self.config = config or PipelineConfig()

    def run(self) -> None:
        self.config.ensure_dirs()
        state, context = self._bootstrap_state()
        round_table = RoundTable(
            [
                ModeratorAgent(),
                CleanerAgent(),
                TypeResolverAgent(),
                RelationNormalizerAgent(),
                LexicalLinkerAgent(),
                ChapterLinkAgent(),
                OrphanRescuerAgent(),
                AuditAgent(),
            ]
        )
        state = round_table.run(state, context)
        quality = self._quality_report(state)
        self._persist(state, quality)
        print("Pipeline concluído com sucesso.")
        print(f"Nós: {len(state.concepts)} | Relações: {len(state.relations)} | Órfãos: {quality['orphans']}")

    def _bootstrap_state(self) -> Tuple[GraphState, Dict]:
        concepts_raw = self._load_json_list(self.config.raw_concepts_path)
        relations_raw = self._load_json_list(self.config.raw_relations_path)
        ontology_map = self._load_json_dict(self.config.ontology_map_path)

        concepts: Dict[str, Concept] = {}
        for item in concepts_raw:
            concept = Concept(
                nome=item.get("nome", ""),
                tipo=item.get("tipo", DEFAULT_TYPE),
                definicao=item.get("definicao", ""),
                capitulo_origem=str(item.get("capitulo_origem", "")),
                caminho=item.get("caminho"),
            )
            concepts[concept.canonical()] = concept

        relations: List[Relation] = []
        for item in relations_raw:
            relations.append(
                Relation(
                    source=item.get("source", ""),
                    target=item.get("target", ""),
                    type=item.get("type", "related"),
                    explanation=item.get("explanation"),
                    confidence=0.6,
                    strategy="seed",
                )
            )

        state = GraphState(concepts=concepts, relations=relations)
        context = {"ontology": ontology_map}
        state.log("Estado inicial carregado.")
        return state, context

    def _quality_report(self, state: GraphState) -> Dict:
        degree = Counter()
        for rel in state.relations:
            degree[rel.source] += 1
            degree[rel.target] += 1
        orphans = [node for node in state.concepts if degree.get(node, 0) == 0]
        density = (2 * len(state.relations)) / max(1, len(state.concepts) * (len(state.concepts) - 1))
        return {
            "generated_at": _dt.datetime.utcnow().isoformat(),
            "nodes": len(state.concepts),
            "edges": len(state.relations),
            "orphans": len(orphans),
            "density": round(density, 6),
            "audit_trail": state.audit_trail,
        }

    def _persist(self, state: GraphState, quality: Dict) -> None:
        densified_payload = {
            "metadata": {
                "generated_at": quality["generated_at"],
                "stage": "02_densification",
            },
            "concepts": [self._concept_to_dict(c) for c in state.concepts.values()],
            "relations": [self._relation_to_dict(r) for r in state.relations],
        }
        self.config.densified_output.write_text(json.dumps(densified_payload, ensure_ascii=False, indent=2), encoding="utf-8")

        final_payload = {
            "metadata": {
                "generated_at": quality["generated_at"],
                "stage": "03_final_audit",
                "quality": quality,
            },
            "concepts": [self._concept_to_dict(c) for c in state.concepts.values()],
            "relations": [self._relation_to_dict(r) for r in state.relations],
        }
        self.config.final_output.write_text(json.dumps(final_payload, ensure_ascii=False, indent=2), encoding="utf-8")
        self.config.quality_report.write_text(json.dumps(quality, ensure_ascii=False, indent=2), encoding="utf-8")

    @staticmethod
    def _concept_to_dict(concept: Concept) -> Dict:
        return {
            "nome": concept.nome,
            "tipo": concept.tipo or DEFAULT_TYPE,
            "definicao": concept.definicao,
            "capitulo_origem": concept.capitulo_origem,
            "caminho": concept.caminho,
            "evidencias": concept.evidencias,
        }

    @staticmethod
    def _relation_to_dict(rel: Relation) -> Dict:
        return {
            "source": rel.source,
            "target": rel.target,
            "type": rel.type,
            "explanation": rel.explanation,
            "confidence": rel.confidence,
            "strategy": rel.strategy,
        }

    @staticmethod
    def _load_json_list(path: Path) -> List[Dict]:
        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {path}")
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return data
        raise ValueError(f"Esperado uma lista em {path}, obtido {type(data)}")

    @staticmethod
    def _load_json_dict(path: Path) -> Dict:
        if not path.exists():
            return {}
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data
        raise ValueError(f"Esperado um dicionário em {path}, obtido {type(data)}")


def main() -> None:
    GraphPipeline().run()


if __name__ == "__main__":
    main()
