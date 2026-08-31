import json
import logging
from dataclasses import dataclass, asdict
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@dataclass
class EnvironmentalTelemetry:
    temperature_c: float        # Range: -10.0 to 50.0 C
    relative_humidity_pct: float# Range: 0.0 to 100.0 %
    soil_moisture_pct: float    # Range: 0.0 to 100.0 %
    leaf_wetness_score: float   # Range: 0.0 (Dry) to 1.0 (Completely Saturated)
    ambient_light_lux: float    # Range: 0.0 to 100,000.0 Lux

# Phytopathological epidemiological climate affinity database
DISEASE_EPIDEMIOLOGY = {
    "Tomato_Late_blight": {
        "ideal_temp_range": (14.0, 22.0),
        "ideal_humidity_min": 85.0,
        "leaf_wetness_threshold": 0.60,
        "causal_agent": "Phytophthora infestans (Oomycete)",
        "urgency": "CRITICAL",
        "chemical_treatment": "Apply Mancozeb (2g/L) or Metalaxyl + Mancozeb (Ridomil MZ @ 2.5g/L) spray.",
        "organic_treatment": "Copper oxychloride (3g/L), remove and burn infected foliage immediately.",
        "irrigation_advice": "Halt overhead sprinkler irrigation immediately. Switch to low-flow drip to keep canopy dry."
    },
    "Potato___Late_blight": {
        "ideal_temp_range": (12.0, 20.0),
        "ideal_humidity_min": 85.0,
        "leaf_wetness_threshold": 0.65,
        "causal_agent": "Phytophthora infestans",
        "urgency": "CRITICAL",
        "chemical_treatment": "Spray Cymoxanil + Mancozeb (Curzate @ 2g/L) or Dimethomorph.",
        "organic_treatment": "Bacillus subtilis bio-fungicide or Bordeaux mixture (1%).",
        "irrigation_advice": "Eliminate excess field moisture. Improve furrow drainage."
    },
    "Tomato_Early_blight": {
        "ideal_temp_range": (24.0, 30.0),
        "ideal_humidity_min": 75.0,
        "leaf_wetness_threshold": 0.40,
        "causal_agent": "Alternaria solani (Fungus)",
        "urgency": "HIGH",
        "chemical_treatment": "Chlorothalonil (2ml/L) or Azoxystrobin (1ml/L) at 7-10 day intervals.",
        "organic_treatment": "Neem oil emulsion (5ml/L) or Trichoderma harzianum soil application.",
        "irrigation_advice": "Avoid splashing soil onto lower leaves. Maintain moderate soil moisture."
    },
    "Potato___Early_blight": {
        "ideal_temp_range": (22.0, 30.0),
        "ideal_humidity_min": 70.0,
        "leaf_wetness_threshold": 0.40,
        "causal_agent": "Alternaria solani",
        "urgency": "HIGH",
        "chemical_treatment": "Mancozeb (75% WP @ 2.5g/L) or Difenoconazole (1ml/L).",
        "organic_treatment": "Copper hydroxide spray and potassium silicate foliar feed.",
        "irrigation_advice": "Ensure balanced nitrogen fertilization; avoid water stress during tuber initiation."
    },
    "Tomato_Bacterial_spot": {
        "ideal_temp_range": (25.0, 32.0),
        "ideal_humidity_min": 80.0,
        "leaf_wetness_threshold": 0.50,
        "causal_agent": "Xanthomonas perforans / euvesicatoria",
        "urgency": "HIGH",
        "chemical_treatment": "Copper hydroxide combined with Mancozeb (bactericide synergy).",
        "organic_treatment": "Streptomyces bio-inoculant, garlic extract spray, certified clean seeds.",
        "irrigation_advice": "Do not enter field when foliage is wet. Disinfect pruning tools with 10% bleach."
    },
    "Pepper__bell___Bacterial_spot": {
        "ideal_temp_range": (24.0, 32.0),
        "ideal_humidity_min": 80.0,
        "leaf_wetness_threshold": 0.50,
        "causal_agent": "Xanthomonas campestris pv. vesicatoria",
        "urgency": "HIGH",
        "chemical_treatment": "Fixed copper bactericide (Kocide @ 2g/L).",
        "organic_treatment": "Pseudomonas fluorescens bio-agent @ 5g/L.",
        "irrigation_advice": "Ensure crop rotation with non-solanaceous crops for minimum 2 years."
    },
    "Tomato_Spider_mites_Two_spotted_spider_mite": {
        "ideal_temp_range": (28.0, 38.0),
        "ideal_humidity_min": 0.0, # Thrives in DRY air (< 50%)
        "leaf_wetness_threshold": 0.10,
        "causal_agent": "Tetranychus urticae (Acari: Tetranychidae)",
        "urgency": "MEDIUM",
        "chemical_treatment": "Abamectin (1.8% EC @ 0.5ml/L) or Spiromesifen (Oberon @ 1ml/L).",
        "organic_treatment": "Release predatory mites (Phytoseiulus persimilis), insecticidal soap spray.",
        "irrigation_advice": "Increase overhead micro-misting to raise canopy humidity and suppress mite reproduction."
    },
    "Tomato_Septoria_leaf_spot": {
        "ideal_temp_range": (20.0, 26.0),
        "ideal_humidity_min": 75.0,
        "leaf_wetness_threshold": 0.50,
        "causal_agent": "Septoria lycopersici",
        "urgency": "MEDIUM",
        "chemical_treatment": "Chlorothalonil or Copper-based fungicides.",
        "organic_treatment": "Prune lower 24 inches of leaves to prevent soil splash.",
        "irrigation_advice": "Drip irrigation only; apply organic straw mulch around plant base."
    },
    "Tomato_Leaf_Mold": {
        "ideal_temp_range": (21.0, 26.0),
        "ideal_humidity_min": 85.0,
        "leaf_wetness_threshold": 0.55,
        "causal_agent": "Passalora fulva",
        "urgency": "MEDIUM",
        "chemical_treatment": "Difenoconazole or Cyprodinil + Fludioxonil.",
        "organic_treatment": "Improve greenhouse ventilation, maintain RH < 80%.",
        "irrigation_advice": "Ventilate polytunnel/greenhouse during early morning hours."
    },
    "Tomato__Tomato_YellowLeaf__Curl_Virus": {
        "ideal_temp_range": (26.0, 36.0),
        "ideal_humidity_min": 0.0,
        "leaf_wetness_threshold": 0.0,
        "causal_agent": "Begomovirus (Vector: Bemisia tabaci whitefly)",
        "urgency": "CRITICAL",
        "chemical_treatment": "Vector management: Thiamethoxam (25% WG @ 0.3g/L) or Acetamiprid.",
        "organic_treatment": "Install yellow sticky traps (15 traps/acre), spray Neem Baan 10,000 ppm.",
        "irrigation_advice": "Uproot and destroy infected virus-stunted plants immediately."
    },
    "Tomato__Tomato_mosaic_virus": {
        "ideal_temp_range": (20.0, 32.0),
        "ideal_humidity_min": 0.0,
        "leaf_wetness_threshold": 0.0,
        "causal_agent": "Tobamovirus (Mechanical transmission)",
        "urgency": "HIGH",
        "chemical_treatment": "No curative viricide exists. Soak hands/tools in skim milk (20%) or trisodium phosphate.",
        "organic_treatment": "Remove infected plants; use virus-resistant seed cultivars (Tm-2(2) gene).",
        "irrigation_advice": "Wash hands with soap before touching healthy nursery plants."
    },
    "Tomato__Target_Spot": {
        "ideal_temp_range": (22.0, 28.0),
        "ideal_humidity_min": 80.0,
        "leaf_wetness_threshold": 0.50,
        "causal_agent": "Corynespora cassiicola",
        "urgency": "MEDIUM",
        "chemical_treatment": "Azoxystrobin + Difenoconazole or Pyraclostrobin.",
        "organic_treatment": "Copper sulfate pentahydrate and Bacillus amyloliquefaciens.",
        "irrigation_advice": "Maximize row spacing to promote air circulation."
    },
    "Pepper__bell___healthy": {
        "ideal_temp_range": (18.0, 28.0),
        "ideal_humidity_min": 50.0,
        "leaf_wetness_threshold": 0.30,
        "causal_agent": "None (Healthy Tissue)",
        "urgency": "LOW",
        "chemical_treatment": "No intervention required. Maintain standard preventive schedule.",
        "organic_treatment": "Apply Seaweed extract or Humic acid foliar biostimulants.",
        "irrigation_advice": "Maintain standard soil moisture (60-70% Field Capacity)."
    },
    "Potato___healthy": {
        "ideal_temp_range": (15.0, 24.0),
        "ideal_humidity_min": 50.0,
        "leaf_wetness_threshold": 0.30,
        "causal_agent": "None (Healthy Tissue)",
        "urgency": "LOW",
        "chemical_treatment": "No fungicide needed.",
        "organic_treatment": "Preventive Trichoderma soil drenching at hilling stage.",
        "irrigation_advice": "Consistent moisture to prevent tuber hollow-heart."
    },
    "Tomato_healthy": {
        "ideal_temp_range": (18.0, 28.0),
        "ideal_humidity_min": 50.0,
        "leaf_wetness_threshold": 0.30,
        "causal_agent": "None (Healthy Tissue)",
        "urgency": "LOW",
        "chemical_treatment": "No fungicide needed. Crop is in optimal vegetative condition.",
        "organic_treatment": "Maintain balanced NPK fertigation and beneficial mycorrhizae.",
        "irrigation_advice": "Standard tensiometer-based automated irrigation schedule."
    }
}

class IoTSensorFusionEngine:
    """
    Multimodal Decision Engine: Combines Edge Vision Inference with Environmental IoT Telemetry.
    Implements Bayesian Evidence Weighting to compute Disease Risk Index (DRI).
    """
    def __init__(self):
        self.disease_db = DISEASE_EPIDEMIOLOGY

    def compute_environmental_affinity_score(self, disease_name: str, telemetry: EnvironmentalTelemetry) -> float:
        """
        Calculates how favorable current microclimate conditions are for the given pathogen [0.0 to 1.0].
        """
        if disease_name not in self.disease_db:
            return 0.50 # Neutral default

        info = self.disease_db[disease_name]
        
        # If healthy, score is higher when conditions are moderate
        if "healthy" in disease_name.lower():
            t_min, t_max = info["ideal_temp_range"]
            t_score = 1.0 if (t_min <= telemetry.temperature_c <= t_max) else 0.4
            h_score = 1.0 if (40.0 <= telemetry.relative_humidity_pct <= 75.0) else 0.5
            w_score = 1.0 if (telemetry.leaf_wetness_score < 0.40) else 0.4
            return float(0.4 * t_score + 0.3 * h_score + 0.3 * w_score)

        # Pathogen scoring
        t_min, t_max = info["ideal_temp_range"]
        # Temperature affinity
        if t_min <= telemetry.temperature_c <= t_max:
            temp_score = 1.0
        elif (t_min - 4.0) <= telemetry.temperature_c <= (t_max + 4.0):
            temp_score = 0.65
        else:
            temp_score = 0.20

        # Humidity & Wetness affinity
        # Spider mites thrive in dry conditions; fungal/bacterial thrive in wet
        if "spider_mite" in disease_name.lower():
            humidity_score = 1.0 if telemetry.relative_humidity_pct < 55.0 else (0.3 if telemetry.relative_humidity_pct > 80.0 else 0.6)
            wetness_score = 1.0 if telemetry.leaf_wetness_score < 0.20 else 0.20
        else:
            req_h = info["ideal_humidity_min"]
            humidity_score = 1.0 if telemetry.relative_humidity_pct >= req_h else max(0.1, telemetry.relative_humidity_pct / (req_h + 1e-5))
            wetness_thresh = info["leaf_wetness_threshold"]
            wetness_score = 1.0 if telemetry.leaf_wetness_score >= wetness_thresh else max(0.15, telemetry.leaf_wetness_score / (wetness_thresh + 1e-5))

        affinity = 0.40 * temp_score + 0.35 * humidity_score + 0.25 * wetness_score
        return round(float(affinity), 4)

    def fuse_prediction_and_telemetry(self, 
                                     vision_predictions: Dict[str, float], 
                                     telemetry: EnvironmentalTelemetry, 
                                     vision_weight: float = 0.70) -> Dict[str, Any]:
        """
        Fuses top visual predictions with IoT telemetry environmental affinity scores.
        vision_predictions: dict mapping disease_name -> visual confidence percentage [0.0 - 100.0]
        """
        sensor_weight = 1.0 - vision_weight
        fused_rankings = []

        for disease_name, visual_conf in vision_predictions.items():
            vis_prob = visual_conf / 100.0
            env_affinity = self.compute_environmental_affinity_score(disease_name, telemetry)
            
            # Weighted multimodal fusion score
            fused_score = (vis_prob * vision_weight) + (env_affinity * sensor_weight)
            
            fused_rankings.append({
                "disease": disease_name,
                "visual_confidence_pct": round(visual_conf, 2),
                "environmental_risk_pct": round(env_affinity * 100.0, 2),
                "fused_confidence_pct": round(fused_score * 100.0, 2)
            })

        fused_rankings.sort(key=lambda x: x["fused_confidence_pct"], reverse=True)
        primary = fused_rankings[0]["disease"]
        primary_info = self.disease_db.get(primary, {})

        # Multimodal Disease Risk Index (DRI) [0 - 100]
        dri = fused_rankings[0]["fused_confidence_pct"] if "healthy" not in primary.lower() else max(0, 100 - fused_rankings[0]["fused_confidence_pct"])
        
        # Risk Category
        if "healthy" in primary.lower():
            alert_level = "NOMINAL (Healthy Crop)"
            color = "GREEN"
        elif dri >= 80.0:
            alert_level = "CRITICAL / HIGH EPIDEMIC RISK"
            color = "RED"
        elif dri >= 50.0:
            alert_level = "MODERATE RISK (Action Recommended)"
            color = "AMBER"
        else:
            alert_level = "LOW RISK (Watch & Monitor)"
            color = "BLUE"

        diagnostic_dossier = {
            "primary_diagnosis": primary,
            "fused_confidence": fused_rankings[0]["fused_confidence_pct"],
            "disease_risk_index": round(dri, 1),
            "alert_level": alert_level,
            "status_color": color,
            "causal_agent": primary_info.get("causal_agent", "N/A"),
            "urgency": primary_info.get("urgency", "LOW"),
            "telemetry_snapshot": asdict(telemetry),
            "fused_rankings": fused_rankings,
            "prescriptions": {
                "chemical_intervention": primary_info.get("chemical_treatment", "None required."),
                "organic_biocontrol": primary_info.get("organic_treatment", "Standard biostimulants."),
                "irrigation_adjustment": primary_info.get("irrigation_advice", "Maintain optimal moisture.")
            }
        }
        return diagnostic_dossier

if __name__ == "__main__":
    engine = IoTSensorFusionEngine()
    
    # Test case: Tomato Late Blight predicted with humid IoT environment
    sample_vision = {
        "Tomato_Late_blight": 88.5,
        "Tomato_Early_blight": 8.2,
        "Tomato_healthy": 3.3
    }
    sample_telemetry = EnvironmentalTelemetry(
        temperature_c=18.5,
        relative_humidity_pct=92.0,
        soil_moisture_pct=78.0,
        leaf_wetness_score=0.85,
        ambient_light_lux=18500.0
    )
    dossier = engine.fuse_prediction_and_telemetry(sample_vision, sample_telemetry)
    print(json.dumps(dossier, indent=2))
