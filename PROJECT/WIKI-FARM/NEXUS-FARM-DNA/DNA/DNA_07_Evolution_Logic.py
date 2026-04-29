import numpy as np
from scipy.spatial.distance import cosine
from typing import Dict, List, Any

# DNA_07_Evolution_Logic v2.0 (ANTI-COLLAPSE)
# FIX [H-04]: Dynamic novelty normalization using population-aware percentile
# FIX [V3-05]: Handles 10-dimensional DNA vectors (backward-compatible with 6-dim)
# FIX [V3-06]: Euclidean distance fallback for near-zero cosine vectors
# FIX [V3-07]: Compatibility uses hybrid distance (cosine + trait divergence)


def calculate_compatibility(node_a: Dict[str, Any], node_b: Dict[str, Any]) -> float:
    """
    Computes compatibility index between two nodes (0.0 – 1.0).
    v2.0: Hybrid metric — cosine distance + trait divergence bonus.
    """
    # 1. Hard restrictions (Risk & Interface)
    risk_a = node_a.get('meta', {}).get('risk_level', 'none')
    risk_b = node_b.get('meta', {}).get('risk_level', 'none')
    if risk_a == 'high' or risk_b == 'high':
        iface_a = node_a['evolution_matrix']['traits_fixed']['interface']
        iface_b = node_b['evolution_matrix']['traits_fixed']['interface']
        if iface_a == 'gui' or iface_b == 'gui':
            return 0.0  # Mutation forbidden: dangerous tool cannot have public GUI

    # 2. Security-level critical hardstop
    sec_a = node_a['evolution_matrix']['traits_fixed'].get('security_level', 'none')
    sec_b = node_b['evolution_matrix']['traits_fixed'].get('security_level', 'none')
    iface_a = node_a['evolution_matrix']['traits_fixed']['interface']
    iface_b = node_b['evolution_matrix']['traits_fixed']['interface']
    if (sec_a == 'critical' and iface_b == 'gui') or (sec_b == 'critical' and iface_a == 'gui'):
        return 0.0

    # 3. Semantic distance (Cosine)
    dna_a = np.array(node_a['evolution_matrix']['dna_signature'], dtype=float)
    dna_b = np.array(node_b['evolution_matrix']['dna_signature'], dtype=float)

    # Guard against zero vectors — use Euclidean fallback
    norm_a = np.linalg.norm(dna_a)
    norm_b = np.linalg.norm(dna_b)

    if norm_a < 1e-8 or norm_b < 1e-8:
        # FIX [V3-06]: Use Euclidean distance for near-zero vectors
        max_dist = np.sqrt(len(dna_a))  # Theoretical max in N-dim unit hypercube
        eucl_dist = np.linalg.norm(dna_a - dna_b)
        distance = eucl_dist / max_dist  # Normalize to [0, 1]
    else:
        distance = cosine(dna_a, dna_b)   # 0 = identical, 1 = orthogonal

    # Hybridization limits — relaxed for v3.0 (was 0.15/0.85)
    if distance < 0.05:
        return 0.0   # Inbreeding: nearly identical DNA
    if distance > 0.95:
        return 0.05  # Chimera: too distant

    # 4. FIX [V4-03]: Trait divergence bonus v2.0
    # Cross-domain pairs get HIGHER scores — encourages innovation
    traits_a = node_a['evolution_matrix']['traits_fixed']
    traits_b = node_b['evolution_matrix']['traits_fixed']
    
    trait_keys = ['domain', 'role', 'computing', 'interface', 'autonomy']
    divergence = sum(1 for k in trait_keys if traits_a.get(k) != traits_b.get(k))
    divergence_bonus = divergence * 0.08  # Up to 0.40 bonus for max divergence (was 0.05)

    # Optimal crossing distance: 0.3–0.7
    base_score = 1.0 - abs(0.5 - distance)
    
    # FIX [V4-04]: Domain penalty nearly eliminated for cross-domain breeding
    domain_a = traits_a.get('domain', '')
    domain_b = traits_b.get('domain', '')
    domain_multiplier = 1.0 if domain_a == domain_b else 0.95  # Was 0.9

    final = base_score * domain_multiplier + divergence_bonus
    return float(round(min(1.0, final), 3))


def calculate_novelty(new_dna: List[float], population: List[Dict[str, Any]], k: int = 7) -> float:
    """
    Computes novelty as mean distance to K nearest neighbors.
    v2.0: 
    - k=7 (was 5) for better statistical stability with 1300+ nodes
    - Euclidean fallback for zero-cosine vectors
    - Dynamic normalization using population 90th percentile (was 95th)
    """
    if not population:
        return 1.0

    new_dna_vec = np.array(new_dna, dtype=float)
    new_norm = np.linalg.norm(new_dna_vec)
    distances = []

    for node in population:
        node_dna = np.array(node['evolution_matrix']['dna_signature'], dtype=float)
        node_norm = np.linalg.norm(node_dna)

        # FIX [V3-06]: Euclidean fallback
        if new_norm < 1e-8 or node_norm < 1e-8:
            max_dist = np.sqrt(len(new_dna_vec))
            dist = np.linalg.norm(new_dna_vec - node_dna) / max_dist
        else:
            dist = cosine(new_dna_vec, node_dna)

        distances.append(dist)

    distances.sort()
    k_nearest = distances[:k]

    mean_dist = float(np.mean(k_nearest)) if k_nearest else 0.0

    # FIX [V3-08]: Use 90th percentile (was 95th) — slightly more aggressive
    if len(distances) >= 10:
        p90 = float(np.percentile(distances, 90))
        normalizer = p90 if p90 > 0.01 else 1.0
    else:
        normalizer = 0.5   # Fallback only for tiny populations

    normalized_novelty = min(1.0, mean_dist / normalizer)
    return float(round(normalized_novelty, 3))
