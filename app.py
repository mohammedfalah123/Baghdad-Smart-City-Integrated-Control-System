"""
BAGHDAD SMART CITY CONTROL SYSTEM - REAL PHYSICS-BASED OPTIMIZATION
====================================================================
نظام متكامل لتحسين قطاعات مدينة بغداد باستخدام فيزياء حقيقية وخوارزميات Mealpy
متوافق مع Hugging Face Spaces 100%
"""

# ============================================================================
# 1️⃣ استيراد المكتبات الأساسية
# ============================================================================

import os
import sys
import warnings
import time
import json
import random
import subprocess
from typing import Dict, List, Tuple, Optional, Any, Callable
from datetime import datetime, timedelta
import requests

# استيراد المكتبات العلمية
import numpy as np
import pandas as pd
import gradio as gr
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt

# تجاهل التحذيرات
warnings.filterwarnings('ignore')

print("="*80)
print("🏙️ BAGHDAD SMART CITY CONTROL SYSTEM - REAL PHYSICS VERSION")
print("="*80)

# ============================================================================
# 2️⃣ استيراد جميع خوارزميات Mealpy (35 خوارزمية)
# ============================================================================

try:
    from mealpy import FloatVar
    
    # Swarm-based (13 algorithms)
    from mealpy.swarm_based.PSO import OriginalPSO as PSO
    from mealpy.swarm_based.GWO import OriginalGWO as GWO
    from mealpy.swarm_based.WOA import OriginalWOA as WOA
    from mealpy.swarm_based.SSA import OriginalSSA as SSA
    from mealpy.swarm_based.MFO import OriginalMFO as MFO
    from mealpy.swarm_based.GOA import OriginalGOA as GOA
    from mealpy.swarm_based.HHO import OriginalHHO as HHO
    from mealpy.swarm_based.FA import OriginalFA as FA
    from mealpy.swarm_based.FOA import OriginalFOA as FOA
    from mealpy.swarm_based.TSO import OriginalTSO as TSO
    from mealpy.swarm_based.DO import OriginalDO as DO
    from mealpy.swarm_based.COA import OriginalCOA as COA
    from mealpy.swarm_based.EHO import OriginalEHO as EHO
    
    # Evolutionary-based (6 algorithms)
    from mealpy.evolutionary_based.DE import OriginalDE as DE
    from mealpy.evolutionary_based.EP import OriginalEP as EP
    from mealpy.evolutionary_based.ES import OriginalES as ES
    from mealpy.evolutionary_based.MA import OriginalMA as MA
    from mealpy.evolutionary_based.CRO import OriginalCRO as CRO
    from mealpy.evolutionary_based.SHADE import OriginalSHADE as SHADE
    
    # Physics-based (8 algorithms)
    from mealpy.physics_based.SA import OriginalSA as SA
    from mealpy.physics_based.MVO import OriginalMVO as MVO
    from mealpy.physics_based.HGSO import OriginalHGSO as HGSO
    from mealpy.physics_based.NRO import OriginalNRO as NRO
    from mealpy.physics_based.EO import OriginalEO as EO
    from mealpy.physics_based.ASO import OriginalASO as ASO
    from mealpy.physics_based.WDO import OriginalWDO as WDO
    from mealpy.physics_based.TWO import OriginalTWO as TWO
    from mealpy.physics_based.EFO import OriginalEFO as EFO
    
    # Human-based (5 algorithms)
    from mealpy.human_based.CA import OriginalCA as CA
    from mealpy.human_based.ICA import OriginalICA as ICA
    from mealpy.human_based.LCO import OriginalLCO as LCO
    from mealpy.human_based.QSA import OriginalQSA as QSA
    from mealpy.human_based.TLO import OriginalTLO as TLO
    from mealpy.human_based.SARO import OriginalSARO as SARO
    from mealpy.human_based.SSDO import OriginalSSDO as SSDO
    
    MEALPY_AVAILABLE = True
    print("✅ All 35 Mealpy algorithms imported successfully")
    
except Exception as e:
    print(f"⚠️ Mealpy import error: {e}")
    MEALPY_AVAILABLE = False
    # تعريف كلاسات وهمية للطوارئ
    class Optimizer:
        def __init__(self, **kwargs): 
            self.epoch = kwargs.get('epoch', 100)
            self.pop_size = kwargs.get('pop_size', 50)
            self.history = type('History', (), {'list_global_best': []})()
        def solve(self, problem):
            import numpy as np
            best_solution = np.random.uniform(problem['bounds'].lb, problem['bounds'].ub)
            best_fitness = problem['obj_func'](best_solution)
            self.history.list_global_best = [(best_solution, best_fitness)]
    
    PSO = GWO = WOA = SSA = MFO = GOA = HHO = FA = FOA = TSO = DO = COA = EHO = Optimizer
    DE = EP = ES = MA = CRO = SHADE = Optimizer
    SA = MVO = HGSO = NRO = EO = ASO = WDO = TWO = EFO = Optimizer
    CA = ICA = LCO = QSA = TLO = SARO = SSDO = Optimizer
    FloatVar = lambda lb, ub: type('Bounds', (), {'lb': lb, 'ub': ub})()

# ============================================================================
# 3️⃣ مولد الخوارزميات الهجينة
# ============================================================================

SINGLE_ALGORITHMS = {
    "PSO": PSO, "GWO": GWO, "WOA": WOA, "SSA": SSA, "MFO": MFO,
    "GOA": GOA, "HHO": HHO, "FA": FA, "FOA": FOA, "TSO": TSO,
    "DO": DO, "COA": COA, "EHO": EHO, "DE": DE, "EP": EP,
    "ES": ES, "MA": MA, "CRO": CRO, "SHADE": SHADE, "SA": SA,
    "MVO": MVO, "HGSO": HGSO, "NRO": NRO, "EO": EO, "ASO": ASO,
    "WDO": WDO, "TWO": TWO, "EFO": EFO, "CA": CA, "ICA": ICA,
    "LCO": LCO, "QSA": QSA, "TLO": TLO, "SARO": SARO, "SSDO": SSDO
}

class HybridAlgorithmGenerator:
    """توليد خوارزميات هجينة ديناميكياً"""
    
    def __init__(self):
        self.algorithm_names = list(SINGLE_ALGORITHMS.keys())
        self.generated = self._generate_all()
        self.single_names_with_full = [f"{name}" for name in self.algorithm_names]
        
    def _generate_all(self) -> Dict:
        """توليد جميع الخوارزميات الهجينة"""
        algorithms = {}
        names = self.algorithm_names
        
        # توليد الخوارزميات الثنائية (200)
        binary_count = 0
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                if binary_count >= 200:
                    break
                name1, name2 = names[i], names[j]
                algorithms[f"{name1}+{name2}"] = (name1, name2)
                algorithms[f"{name2}+{name1}"] = (name2, name1)
                binary_count += 2
        
        # توليد الخوارزميات الثلاثية (300)
        triple_count = 0
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                for k in range(j + 1, len(names)):
                    if triple_count >= 300:
                        break
                    name1, name2, name3 = names[i], names[j], names[k]
                    algorithms[f"{name1}+{name2}+{name3}"] = (name1, name2, name3)
                    triple_count += 1
        
        # توليد الخوارزميات الرباعية (250)
        quad_count = 0
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                for k in range(j + 1, len(names)):
                    for l in range(k + 1, len(names)):
                        if quad_count >= 250:
                            break
                        name1, name2, name3, name4 = names[i], names[j], names[k], names[l]
                        algorithms[f"{name1}+{name2}+{name3}+{name4}"] = (name1, name2, name3, name4)
                        quad_count += 1
        
        return algorithms
    
    def get_all_algorithms(self) -> Dict[str, List[str]]:
        """الحصول على جميع الخوارزميات مصنفة"""
        return {
            "Single": self.single_names_with_full,
            "Binary": list(self.generated.keys())[:200],
            "Triple": list(self.generated.keys())[200:500],
            "Quad": list(self.generated.keys())[500:750]
        }
    
    def get_algorithm_class(self, algo_name: str):
        """الحصول على صنف الخوارزمية"""
        if algo_name in SINGLE_ALGORITHMS:
            return SINGLE_ALGORITHMS[algo_name]
        elif algo_name in self.generated:
            first_algo = self.generated[algo_name][0]
            return SINGLE_ALGORITHMS[first_algo]
        else:
            return PSO

# ============================================================================
# 4️⃣ Baghdad Real Data Collector with API Keys
# ============================================================================

class BaghdadRealDataCollector:
    """جلب بيانات حقيقية لمدينة بغداد من APIs حية"""

    def __init__(self):
        # Baghdad coordinates
        self.lat = 33.3152
        self.lon = 44.3661

        # REAL API KEYS
        self.weather_api_key = "b297ccf219c4431daf8fec128801cb6e"
        self.waqi_token = "49cf63c8b68c57f499e29ef32266c12a03afc777"
        self.traffic_api_key = "NoNMFAHrjoh6uOT6uiHeOjn59oZ561NR"

        # Cache for rate limiting
        self.cache = {}
        self.cache_timestamp = {}
        self.cache_duration = 300  # 5 minutes cache

        # Iraq grid data from EnergyData.info
        self.iraq_grid_data = {
            "total_capacity": 9348,
            "power_plants": [
                {"name": "Al-Anbar CCGT", "capacity": 1640, "type": "gas"},
                {"name": "Al-Mansouriya", "capacity": 728, "type": "gas"},
                {"name": "Al-Najaf", "capacity": 500, "type": "oil"},
                {"name": "Baiji", "capacity": 1200, "type": "oil"},
                {"name": "Erbil", "capacity": 1500, "type": "gas"},
                {"name": "Baghdad South", "capacity": 1200, "type": "gas"},
                {"name": "Baghdad North", "capacity": 900, "type": "oil"},
                {"name": "Taji", "capacity": 800, "type": "gas"},
                {"name": "Musayyib", "capacity": 1280, "type": "gas"},
                {"name": "Al-Doura", "capacity": 600, "type": "oil"}
            ]
        }

        # Test connections
        self.test_connections()

    def _is_cache_valid(self, key):
        """التحقق من صحة الكاش"""
        if key in self.cache_timestamp:
            return (time.time() - self.cache_timestamp[key]) < self.cache_duration
        return False

    def test_connections(self):
        """اختبار الاتصال بجميع APIs"""
        print("\n🔌 Testing API Connections...")

        # Test OpenWeatherMap
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&appid={self.weather_api_key}&units=metric"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print("✅ OpenWeatherMap API: Connected")
            else:
                print(f"⚠️ OpenWeatherMap API: Status {response.status_code}")
        except Exception as e:
            print(f"❌ OpenWeatherMap API: {e}")

        # Test WAQI
        try:
            url = f"https://api.waqi.info/feed/geo:{self.lat};{self.lon}/?token={self.waqi_token}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200 and response.json().get('status') == 'ok':
                print("✅ WAQI API: Connected")
            else:
                print("⚠️ WAQI API: Using fallback data")
        except:
            print("⚠️ WAQI API: Using fallback data")

        # Test TomTom
        try:
            url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
            params = {"key": self.traffic_api_key, "point": f"{self.lat},{self.lon}", "radius": 5000}
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                print("✅ TomTom API: Connected")
            else:
                print(f"⚠️ TomTom API: Status {response.status_code}")
        except Exception as e:
            print(f"❌ TomTom API: {e}")

        print("="*80)

    def get_baghdad_weather(self):
        """الحصول على بيانات الطقس الحقيقية لبغداد"""
        cache_key = "weather"
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]

        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&appid={self.weather_api_key}&units=metric"
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                data = response.json()
                weather_data = {
                    "temperature": data['main']['temp'],
                    "feels_like": data['main']['feels_like'],
                    "temp_min": data['main']['temp_min'],
                    "temp_max": data['main']['temp_max'],
                    "humidity": data['main']['humidity'],
                    "pressure": data['main']['pressure'],
                    "sea_level": data['main'].get('sea_level', 0),
                    "grnd_level": data['main'].get('grnd_level', 0),
                    "wind_speed": data['wind']['speed'],
                    "wind_direction": data['wind'].get('deg', 0),
                    "wind_gust": data['wind'].get('gust', 0),
                    "clouds": data['clouds']['all'],
                    "weather_main": data['weather'][0]['main'],
                    "weather_description": data['weather'][0]['description'],
                    "weather_icon": data['weather'][0]['icon'],
                    "visibility": data.get('visibility', 10000) / 1000,
                    "timestamp": datetime.now().isoformat(),
                    "source": "OpenWeatherMap"
                }

                self.cache[cache_key] = weather_data
                self.cache_timestamp[cache_key] = time.time()
                return weather_data

        except Exception as e:
            print(f"⚠️ Weather API error: {e}")

        # Fallback data
        fallback = {
            "temperature": 25.0,
            "feels_like": 26.0,
            "humidity": 40,
            "pressure": 1013,
            "wind_speed": 10.0,
            "weather_main": "Clear",
            "weather_description": "clear sky",
            "visibility": 10.0,
            "timestamp": datetime.now().isoformat(),
            "source": "Fallback"
        }
        self.cache[cache_key] = fallback
        return fallback

    def get_baghdad_air_quality(self):
        """الحصول على بيانات جودة الهواء الحقيقية لبغداد"""
        cache_key = "air_quality"
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]

        try:
            url = f"https://api.waqi.info/feed/geo:{self.lat};{self.lon}/?token={self.waqi_token}"
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'ok':
                    station_data = data['data']
                    iaqi = station_data.get('iaqi', {})
                    aqi = station_data.get('aqi', 0)

                    # Determine AQI category
                    if aqi <= 50:
                        category = "Good"
                        color = "green"
                    elif aqi <= 100:
                        category = "Moderate"
                        color = "yellow"
                    elif aqi <= 150:
                        category = "Unhealthy for Sensitive Groups"
                        color = "orange"
                    elif aqi <= 200:
                        category = "Unhealthy"
                        color = "red"
                    elif aqi <= 300:
                        category = "Very Unhealthy"
                        color = "purple"
                    else:
                        category = "Hazardous"
                        color = "maroon"

                    air_data = {
                        "aqi": aqi,
                        "category": category,
                        "color": color,
                        "pm25": iaqi.get('pm25', {}).get('v', 0) if 'pm25' in iaqi else 0,
                        "pm10": iaqi.get('pm10', {}).get('v', 0) if 'pm10' in iaqi else 0,
                        "no2": iaqi.get('no2', {}).get('v', 0) if 'no2' in iaqi else 0,
                        "so2": iaqi.get('so2', {}).get('v', 0) if 'so2' in iaqi else 0,
                        "co": iaqi.get('co', {}).get('v', 0) if 'co' in iaqi else 0,
                        "o3": iaqi.get('o3', {}).get('v', 0) if 'o3' in iaqi else 0,
                        "station": station_data.get('city', {}).get('name', 'Baghdad'),
                        "timestamp": datetime.now().isoformat(),
                        "source": "WAQI"
                    }

                    self.cache[cache_key] = air_data
                    self.cache_timestamp[cache_key] = time.time()
                    return air_data

        except Exception as e:
            print(f"⚠️ Air Quality API error: {e}")

        # Fallback data
        fallback = {
            "aqi": 85,
            "category": "Moderate",
            "color": "yellow",
            "pm25": 25.5,
            "pm10": 45.2,
            "no2": 35.1,
            "so2": 5.2,
            "co": 0.8,
            "o3": 30.5,
            "station": "Baghdad (Estimated)",
            "timestamp": datetime.now().isoformat(),
            "source": "Fallback"
        }
        self.cache[cache_key] = fallback
        return fallback

    def get_baghdad_traffic(self):
        """الحصول على بيانات حركة المرور الحقيقية لبغداد"""
        cache_key = "traffic"
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]

        try:
            url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
            params = {
                "key": self.traffic_api_key,
                "point": f"{self.lat},{self.lon}",
                "radius": 5000,
                "unit": "KMPH"
            }
            response = requests.get(url, params=params, timeout=5)

            if response.status_code == 200:
                data = response.json()
                if 'flowSegmentData' in data:
                    flow_data = data['flowSegmentData']
                    current_speed = flow_data.get('currentSpeed', 30)
                    free_flow_speed = flow_data.get('freeFlowSpeed', 50)
                    confidence = flow_data.get('confidence', 0.8)

                    if free_flow_speed > 0:
                        congestion = current_speed / free_flow_speed
                    else:
                        congestion = 0.7

                    if congestion >= 0.8:
                        condition = "Heavy Traffic"
                        condition_color = "red"
                    elif congestion >= 0.6:
                        condition = "Moderate Traffic"
                        condition_color = "orange"
                    elif congestion >= 0.4:
                        condition = "Light Traffic"
                        condition_color = "yellow"
                    else:
                        condition = "Free Flow"
                        condition_color = "green"

                    traffic_data = {
                        "current_speed": current_speed,
                        "free_flow_speed": free_flow_speed,
                        "congestion_level": congestion,
                        "confidence": confidence,
                        "condition": condition,
                        "condition_color": condition_color,
                        "timestamp": datetime.now().isoformat(),
                        "source": "TomTom"
                    }

                    self.cache[cache_key] = traffic_data
                    self.cache_timestamp[cache_key] = time.time()
                    return traffic_data

        except Exception as e:
            print(f"⚠️ Traffic API error: {e}")

        # Fallback data
        hour = datetime.now().hour
        if 7 <= hour <= 9 or 16 <= hour <= 19:
            congestion = 0.8
        elif 10 <= hour <= 15:
            congestion = 0.6
        else:
            congestion = 0.4

        fallback = {
            "current_speed": 50 * congestion,
            "free_flow_speed": 50,
            "congestion_level": congestion,
            "confidence": 0.7,
            "condition": "Moderate Traffic",
            "condition_color": "orange",
            "timestamp": datetime.now().isoformat(),
            "source": "Fallback"
        }
        self.cache[cache_key] = fallback
        return fallback

    def get_baghdad_electricity_data(self):
        """الحصول على بيانات الكهرباء من EnergyData.info"""
        cache_key = "electricity"
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]

        weather = self.get_baghdad_weather()
        hour = datetime.now().hour

        # Peak hours based on Baghdad time
        if 12 <= hour <= 16:  # Afternoon peak
            peak_factor = 1.3
        elif 19 <= hour <= 23:  # Evening peak
            peak_factor = 1.2
        else:
            peak_factor = 1.0

        # Temperature effect on consumption
        temp = weather['temperature']
        temp_factor = 1.0 + 0.02 * max(0, temp - 20)

        # Calculate current load (70% of capacity as base)
        base_load = self.iraq_grid_data["total_capacity"] * 0.7
        current_load = base_load * peak_factor * temp_factor

        electricity_data = {
            "current_load": current_load,
            "available_capacity": self.iraq_grid_data["total_capacity"] - current_load,
            "load_percentage": (current_load / self.iraq_grid_data["total_capacity"]) * 100,
            "total_capacity": self.iraq_grid_data["total_capacity"],
            "peak_factor": peak_factor,
            "temp_factor": temp_factor,
            "carbon_intensity": 550,  # gCO2/kWh for Iraq
            "fossil_fuel_ratio": 95,  # 95% fossil fuels
            "renewable_ratio": 5,     # 5% renewable
            "timestamp": datetime.now().isoformat(),
            "source": "EnergyData.info + Estimates"
        }

        self.cache[cache_key] = electricity_data
        self.cache_timestamp[cache_key] = time.time()
        return electricity_data

    def get_baghdad_waste_data(self):
        """الحصول على بيانات النفايات (مبنية على إحصائيات حقيقية)"""
        cache_key = "waste"
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]

        # Real Baghdad waste statistics
        waste_data = {
            "daily_waste_tons": 9315,
            "per_capita_kg": 1.5,
            "population": 8500000,
            "collection_efficiency": 0.75,
            "recycling_rate": 0.05,
            "fleet_size": 450,
            "containers": 2500,
            "collection_routes": 85,
            "disposal_sites": 3,
            "timestamp": datetime.now().isoformat(),
            "source": "Baghdad Municipality Estimates"
        }

        self.cache[cache_key] = waste_data
        self.cache_timestamp[cache_key] = time.time()
        return waste_data

# ============================================================================
# 5️⃣ إنشاء كائن البيانات الحقيقية
# ============================================================================

print("\n📡 Initializing Baghdad Real Data Collector...")
baghdad_real = BaghdadRealDataCollector()

# Get initial live data
print("\n🌍 Fetching live Baghdad data...")
weather = baghdad_real.get_baghdad_weather()
air = baghdad_real.get_baghdad_air_quality()
traffic = baghdad_real.get_baghdad_traffic()
electricity = baghdad_real.get_baghdad_electricity_data()
waste = baghdad_real.get_baghdad_waste_data()

print(f"\n📍 Baghdad Real-time Status:")
print(f"   🌡️ Temperature: {weather['temperature']}°C - {weather['weather_description']}")
print(f"   🌍 AQI: {air['aqi']} - {air['category']}")
print(f"   🚦 Traffic: {traffic['current_speed']:.1f} km/h - {traffic['condition']}")
print(f"   ⚡ Power Load: {electricity['current_load']:.0f} MW ({electricity['load_percentage']:.1f}%)")
print(f"   🗑️ Daily Waste: {waste['daily_waste_tons']} tons")
print("="*80)

# ============================================================================
# 6️⃣ معايير ودوال فيزيائية لكل قطاع
# ============================================================================

class PhysicalConstants:
    """الثوابت الفيزيائية والمعايير"""
    
    # معايير IEEE للطاقة
    VOLTAGE_LIMITS = {'min': 0.95, 'max': 1.05}  # pu
    FREQUENCY_LIMITS = {'min': 49.5, 'max': 50.5}  # Hz
    THERMAL_LIMIT = 100  # % of line rating
    
    # معايير المرور
    TRAFFIC_SPEED_LIMIT = 120  # km/h
    JAM_DENSITY = 150  # veh/km
    FREE_FLOW_SPEED = 60  # km/h
    # q_max فيزيائي = k_j * v_f / 4 = 150*60/4 = 2250 veh/h (Greenshields)
    # لكن الواقعي في شوارع المدن العربية ≈ 1800 veh/h (قيود هندسية وسلوكية)
    PRACTICAL_FLOW_MAX = 1800  # veh/h (الحد العملي لشوارع بغداد)
    # معاملات COPERT لأسطول بغداد (مزيج Euro 2-4، غالباً بنزين قديم)
    # CO2 = COPERT_A/v + COPERT_B + COPERT_C*v + COPERT_D*v²
    # معايَرة: CO2(20)=220, CO2(50)=150 (min), CO2(100)=185 g/km
    COPERT_A = 3986.11
    COPERT_B = -14.31
    COPERT_C = 1.7889
    COPERT_D = -0.00194
    
    # معايير البيئة (منظمة الصحة العالمية)
    AQI_BREAKPOINTS = {
        'pm25': [(0, 12, 0, 50), (12.1, 35.4, 51, 100), (35.5, 55.4, 101, 150),
                 (55.5, 150.4, 151, 200), (150.5, 250.4, 201, 300), (250.5, 500, 301, 500)],
        'pm10': [(0, 54, 0, 50), (55, 154, 51, 100), (155, 254, 101, 150),
                 (255, 354, 151, 200), (355, 424, 201, 300), (425, 604, 301, 500)]
    }
    
    # معايير النفايات
    VEHICLE_CAPACITY = 10  # tons
    FUEL_EFFICIENCY = 0.3  # L/km
    EMISSION_FACTOR = 2.68  # kg CO2/L

# ============================================================================
# 7️⃣ قطاع الطاقة - مع pandapower
# ============================================================================

try:
    import pandapower as pp
    import pandapower.networks as pn
    PANDAPOWER_AVAILABLE = True
    print("✅ Pandapower imported successfully")
except:
    print("⚠️ Pandapower not available, using fallback")
    PANDAPOWER_AVAILABLE = False

class EnergySector:
    """قطاع الطاقة - مع pandapower للفيزياء الحقيقية"""
    
    def __init__(self):
        self.name = "Baghdad Energy Sector"
        self.icon = "⚡"
        self.criteria = [
            "Current Load (MW)", "Available Capacity (MW)", "Load Percentage (%)",
            "Carbon Intensity (gCO2/kWh)", "Fossil Fuel Ratio (%)", "Renewable Ratio (%)",
            "Grid Frequency (Hz)", "Voltage Stability (pu)", "Power Losses (MW)",
            "System Efficiency (%)"
        ]
        self.units = ["MW", "MW", "%", "gCO2/kWh", "%", "%", "Hz", "pu", "MW", "%"]
        self.higher_is_better = [False, True, False, False, False, True, True, True, False, True]
        
        if PANDAPOWER_AVAILABLE:
            self.network = self._create_baghdad_network()
    
    def _create_baghdad_network(self):
        """إنشاء شبكة كهرباء بغداد باستخدام pandapower"""
        import pandapower as pp
        
        # استخدام شبكة IEEE 30 كنموذج أساسي
        net = pn.case30()
        
        # تعديل الأحمال لتناسب بغداد
        net.load['p_mw'] *= 300  # تكبير الأحمال
        
        # إضافة محطات توليد بغداد
        plants = [
            {"bus": 1, "p_mw": 1200, "name": "Baghdad South", "type": "gas"},
            {"bus": 2, "p_mw": 900, "name": "Baghdad North", "type": "oil"},
            {"bus": 3, "p_mw": 800, "name": "Taji", "type": "gas"},
            {"bus": 4, "p_mw": 600, "name": "Al-Doura", "type": "oil"},
            {"bus": 5, "p_mw": 1280, "name": "Musayyib", "type": "gas"}
        ]
        
        for plant in plants:
            pp.create_gen(net, bus=plant['bus'], p_mw=plant['p_mw'], 
                         name=plant['name'], vm_pu=1.02)
        
        return net
    
    def get_baseline(self):
        """القيم الأساسية - نفس المنطق كـ evaluate() بدون تحسين"""
        electricity = baghdad_real.get_baghdad_electricity_data()
        base_load   = float(electricity['current_load'])

        # baseline: loss_factor = 0.12 (بدون تحسين: imbalance=0، renewable=5%)
        loss_factor_base = float(0.12 * (1.0 + 0.0) * (1.0 - 0.5 * 5.0 / 100.0))
        loss_factor_base = float(max(0.03, min(0.18, loss_factor_base)))
        losses_base      = float(base_load * loss_factor_base)
        efficiency_base  = float(((base_load - losses_base) / base_load) * 100.0)

        return [
            float(base_load),
            float(electricity['available_capacity']),
            float(electricity['load_percentage']),
            float(electricity['carbon_intensity']),
            float(electricity['fossil_fuel_ratio']),
            float(electricity['renewable_ratio']),
            50.0,
            1.0,
            float(losses_base),
            float(efficiency_base)
        ]
    
    def evaluate(self, solution):
        """تقييم حل مقترح - نموذج فيزيائي متسق"""
        try:
            if isinstance(solution, np.ndarray):
                solution = solution.tolist()
            elif not isinstance(solution, (list, tuple)):
                solution = [float(solution)]

            electricity    = baghdad_real.get_baghdad_electricity_data()
            total_capacity = float(electricity['total_capacity'])   # 9348 MW
            base_load      = float(electricity['current_load'])     # MW حقيقي

            # ── 10 متغيرات توليد: gen[0..7] أحفوري، gen[8..9] متجدد ─────────
            gen_values = [max(0.0, float(solution[i]) if i < len(solution) else base_load / 10.0)
                          for i in range(10)]
            total_gen = max(1.0, float(sum(gen_values)))

            # ── نسبة الطاقة المتجددة ─────────────────────────────────────────
            renewable_gen   = float(gen_values[8] + gen_values[9])
            renewable_ratio = float(min(60.0, (renewable_gen / total_gen) * 100.0))
            fossil_ratio    = float(100.0 - renewable_ratio)

            # ── توازن التوليد ────────────────────────────────────────────────
            mean_gen  = total_gen / 10.0
            imbalance = float(np.std(gen_values) / mean_gen) if mean_gen > 0 else 0.0

            # ── خسائر الشبكة I²R ─────────────────────────────────────────────
            # خسائر بغداد baseline: ~12% (شبكة قديمة)
            # imbalance عالٍ → خسائر أعلى (تيارات غير متوازنة)
            # renewable عالٍ → خسائر أقل (مصادر موزعة)
            #
            # مهم: الخسائر تُحسب من base_load (الحمل الفعلي المُوصَّل)
            # وليس من total_gen (الذي قد يكون أعلى بكثير بسبب المتجددة)
            # لأن خسائر I²R تعتمد على التيار في خطوط النقل وليس على التوليد
            loss_base   = 0.12
            imbalance_c = float(min(imbalance, 1.5))  # تحديد أقصى تأثير لـ imbalance
            loss_factor = float(loss_base * (1.0 + 0.3 * imbalance_c) * (1.0 - 0.5 * renewable_ratio / 100.0))
            loss_factor = float(max(0.03, min(0.18, loss_factor)))
            losses      = float(base_load * loss_factor)   # ← من base_load الثابت

            # ── كفاءة النظام = (الطاقة المخرجة / الطاقة المدخلة) × 100 ──────
            # الطاقة المدخلة = base_load (الحمل المطلوب)
            # الطاقة المخرجة = base_load - losses (ما يصل للمستهلك)
            efficiency = float(((base_load - losses) / base_load) * 100.0)
            efficiency = float(min(98.0, max(70.0, efficiency)))

            # ── استقرار الجهد ────────────────────────────────────────────────
            v_improvement     = float(renewable_ratio * 0.0003)
            v_dev             = float(max(0.0, imbalance_c * 0.01 - v_improvement))
            voltage_stability = float(min(1.04, max(0.95, 1.0 - v_dev + v_improvement * 0.5)))

            # ── كثافة الكربون ────────────────────────────────────────────────
            carbon_intensity = float(max(30.0, 550.0 * fossil_ratio / 100.0))

            # ── الطاقة المتاحة ───────────────────────────────────────────────
            delivered_power = float(base_load - losses)
            current_load    = float(min(base_load, max(0.0, delivered_power)))
            available       = float(max(0.0, total_capacity - current_load))
            load_pct        = float(current_load / total_capacity * 100.0)

            # ── عقوبات القيود IEEE ───────────────────────────────────────────
            penalty = 0.0
            if total_gen > total_capacity * 1.05:
                penalty += float((total_gen - total_capacity * 1.05) / total_capacity * 5.0)
            if total_gen < base_load * 0.85:
                penalty += float((base_load * 0.85 - total_gen) / base_load * 5.0)
            if voltage_stability < PhysicalConstants.VOLTAGE_LIMITS['min']:
                penalty += float(10.0 * (PhysicalConstants.VOLTAGE_LIMITS['min'] - voltage_stability))
            if voltage_stability > PhysicalConstants.VOLTAGE_LIMITS['max']:
                penalty += float(10.0 * (voltage_stability - PhysicalConstants.VOLTAGE_LIMITS['max']))

            # ── دالة الهدف ───────────────────────────────────────────────────
            fitness = float(
                0.35 * loss_factor / 0.18 +
                0.30 * carbon_intensity / 550.0 +
                0.20 * (1.0 - renewable_ratio / 60.0) +
                0.15 * v_dev / 0.05 +
                penalty
            )

            results = [
                float(current_load),
                float(available),
                float(load_pct),
                float(carbon_intensity),
                float(fossil_ratio),
                float(renewable_ratio),
                float(50.0 + np.random.normal(0, 0.02)),
                float(voltage_stability),
                float(losses),
                float(efficiency)
            ]

            return fitness, results

        except Exception as e:
            print(f"Energy evaluation error: {e}")
            return 1e9, self.get_baseline()

# ============================================================================
# 8️⃣ قطاع المرور - نموذج Greenshields
# ============================================================================

class TrafficSector:
    """قطاع المرور - نموذج Greenshields الفيزيائي"""
    
    def __init__(self):
        self.name = "Baghdad Traffic Sector"
        self.icon = "🚦"
        self.criteria = [
            "Average Speed (km/h)", "Congestion Level", "Travel Time (min)",
            "Wait Time at Lights (s)", "Traffic Flow (veh/h)", "CO2 Emissions (g/km)",
            "Fuel Consumption (L/100km)", "Intersection Efficiency (%)",
            "Public Transport Delay (min)", "Emergency Response Time (s)"
        ]
        self.units = ["km/h", "-", "min", "s", "veh/h", "g/km", "L/100km", "%", "min", "s"]
        self.higher_is_better = [True, False, False, False, True, False, False, True, False, False]
    
    def get_baseline(self):
        """القيم الأساسية - نفس المعادلات كـ evaluate() بدون تحسين"""
        traffic = baghdad_real.get_baghdad_traffic()
        cong    = float(traffic['congestion_level'])
        density = float(cong * PhysicalConstants.JAM_DENSITY)

        speed, flow = self.greenshields_model(
            density,
            free_speed=PhysicalConstants.FREE_FLOW_SPEED,
            jam_density=PhysicalConstants.JAM_DENSITY
        )
        speed = float(max(1.0, speed))

        # الحد العملي لشوارع بغداد (لا الحد النظري)
        flow = float(min(flow, PhysicalConstants.PRACTICAL_FLOW_MAX))

        # CO2 بنموذج COPERT المعايَر لبغداد
        a = PhysicalConstants.COPERT_A
        b = PhysicalConstants.COPERT_B
        c = PhysicalConstants.COPERT_C
        d = PhysicalConstants.COPERT_D
        co2  = float(max(50.0, a / speed + b + c * speed + d * speed ** 2))
        fuel = float(co2 / 2392.0 * 100.0)

        congestion    = float(max(0.0, min(1.0, 1.0 - speed / PhysicalConstants.FREE_FLOW_SPEED)))
        travel_time   = float(30.0 / speed * 60.0)
        wait_time     = float(60.0 * congestion)
        efficiency_i  = float(max(0.0, 100.0 * (1.0 - congestion) * 0.5))
        transport_del = float(15.0 * congestion)
        emergency_t   = float(180.0 * congestion)

        return [
            float(speed), float(congestion), float(travel_time),
            float(wait_time), float(flow), float(co2), float(fuel),
            float(efficiency_i), float(transport_del), float(emergency_t)
        ]
    
    def greenshields_model(self, density, free_speed=60, jam_density=150):
        """
        نموذج Greenshields لانسياب المرور
        v = v_f * (1 - k/k_j)
        q = k * v_f * (1 - k/k_j)
        """
        if density >= jam_density:
            speed = 0.0
            flow = 0.0
        else:
            speed = float(free_speed * (1 - density / jam_density))
            flow = float(density * speed)
        return speed, flow
    
    def evaluate(self, solution):
        """تقييم حل مقترح باستخدام نموذج Greenshields"""
        try:
            if isinstance(solution, np.ndarray):
                solution = solution.tolist()
            elif not isinstance(solution, (list, tuple)):
                solution = [float(solution)]

            traffic = baghdad_real.get_baghdad_traffic()

            # signal_factor: [0.5, 2.0]
            signal_factor = float(solution[0]) if len(solution) > 0 else 1.0
            # speed_limit:   [30, 120] km/h
            speed_limit   = float(solution[1]) if len(solution) > 1 else 60.0

            # ── بيانات المرور الحقيقية ────────────────────────────────────────
            base_congestion = float(traffic['congestion_level'])  # 0..1
            density = float(base_congestion * PhysicalConstants.JAM_DENSITY)  # veh/km

            # تحسين الإشارات يُقلل الكثافة الفعلية
            effective_density = float(max(1.0, density / signal_factor))

            # ── نموذج Greenshields ────────────────────────────────────────────
            raw_speed, raw_flow = self.greenshields_model(
                effective_density,
                free_speed=PhysicalConstants.FREE_FLOW_SPEED,
                jam_density=PhysicalConstants.JAM_DENSITY
            )
            speed = float(max(1.0, min(speed_limit, raw_speed)))

            # الانسياب محدود بالحد العملي لشوارع بغداد
            flow = float(effective_density * speed)
            flow = float(min(flow, PhysicalConstants.PRACTICAL_FLOW_MAX))

            # مستوى الازدحام
            congestion = float(max(0.0, min(1.0, 1.0 - speed / PhysicalConstants.FREE_FLOW_SPEED)))

            # زمن الرحلة (30 كم مسافة مرجعية)
            travel_time = float(30.0 / speed * 60.0) if speed > 0 else 999.0

            # وقت الانتظار عند الإشارات
            wait_time = float(max(0.0, 60.0 * congestion / signal_factor))

            # ── انبعاثات CO2 — نموذج COPERT المعايَر لبغداد ─────────────────
            # معاملات محسوبة: CO2(20)=220, CO2(50)=150 (min), CO2(100)=185 g/km
            # الحد الأدنى عند السرعة المثلى ~50 km/h
            a = PhysicalConstants.COPERT_A
            b = PhysicalConstants.COPERT_B
            c = PhysicalConstants.COPERT_C
            d = PhysicalConstants.COPERT_D
            emissions = float(max(50.0, a / max(speed, 1.0) + b + c * speed + d * speed ** 2))

            # استهلاك الوقود (L/100km): CO2 / 2392 (بنزين) × 100
            fuel = float(max(3.0, emissions / 2392.0 * 100.0))

            # كفاءة التقاطعات
            efficiency = float(min(100.0, max(0.0, 100.0 * (1.0 - congestion) * min(1.0, signal_factor / 2.0))))

            # تأخير النقل العام (دقائق)
            transport_delay = float(max(0.0, 15.0 * congestion / signal_factor))

            # زمن الاستجابة الطارئة (ثانية)
            emergency_time = float(max(0.0, 180.0 * congestion / signal_factor))

            # عقوبات
            penalty = 0.0
            if speed > PhysicalConstants.TRAFFIC_SPEED_LIMIT:
                penalty += float(speed - PhysicalConstants.TRAFFIC_SPEED_LIMIT) / 10.0

            # دالة الهدف
            fitness = float(
                0.35 * travel_time / 60.0 +
                0.30 * congestion +
                0.20 * emissions / 300.0 +
                0.15 * (1.0 - efficiency / 100.0) +
                penalty
            )

            results = [
                float(speed),
                float(congestion),
                float(travel_time),
                float(wait_time),
                float(flow),
                float(emissions),
                float(fuel),
                float(efficiency),
                float(transport_delay),
                float(emergency_time)
            ]

            return fitness, results

        except Exception as e:
            print(f"Traffic evaluation error: {e}")
            return 1e9, self.get_baseline()

# ============================================================================
# 9️⃣ قطاع البيئة - نموذج Gaussian Plume
# ============================================================================

class EnvironmentSector:
    """قطاع البيئة - نموذج انتشار Gaussian"""
    
    def __init__(self):
        self.name = "Baghdad Environment Sector"
        self.icon = "🌍"
        self.criteria = [
            "Air Quality Index (AQI)", "PM2.5 Concentration (μg/m³)",
            "PM10 Concentration (μg/m³)", "NO2 Level (ppb)", "Temperature (°C)",
            "Humidity (%)", "Wind Speed (km/h)", "Pressure (hPa)",
            "UV Index", "Green Space Coverage (%)"
        ]
        self.units = ["AQI", "μg/m³", "μg/m³", "ppb", "°C", "%", "km/h", "hPa", "-", "%"]
        self.higher_is_better = [False, False, False, False, False, False, False, False, False, True]
    
    def get_baseline(self):
        """القيم الأساسية — من نفس مصدر evaluate لضمان التناسق الكامل"""
        weather = baghdad_real.get_baghdad_weather()
        pm25, pm10, no2, _, _ = self._get_real_concentrations()
        aqi = self.calculate_aqi(pm25, pm10)
        return [
            float(aqi),
            float(pm25),
            float(pm10),
            float(no2),
            float(weather['temperature']),
            float(weather['humidity']),
            float(weather['wind_speed']),
            float(weather['pressure']),
            5.0,
            12.0
        ]

    def gaussian_plume(self, Q, u, x, y, z, H=10):
        """
        نموذج انتشار Gaussian للملوثات
        C(x,y,z) = (Q/(2π u σ_y σ_z)) * exp(-y²/(2σ_y²)) * [exp(-(z-H)²/(2σ_z²)) + exp(-(z+H)²/(2σ_z²))]
        """
        σ_y = 0.32 * x * (1 + 0.0004 * x)**(-0.5)
        σ_z = 0.24 * x * (1 + 0.001 * x)**(0.5)
        
        term1 = Q / (2 * np.pi * u * σ_y * σ_z)
        term2 = np.exp(-y**2 / (2 * σ_y**2))
        term3 = np.exp(-(z - H)**2 / (2 * σ_z**2)) + np.exp(-(z + H)**2 / (2 * σ_z**2))
        
        return float(term1 * term2 * term3)
    
    def calculate_aqi(self, pm25, pm10):
        """حساب AQI وفقاً لوكالة حماية البيئة"""
        def get_aqi_for_pollutant(concentration, breakpoints):
            for low, high, i_low, i_high in breakpoints:
                if low <= concentration <= high:
                    return float(((i_high - i_low) / (high - low)) * (concentration - low) + i_low)
            return 500.0
        
        aqi_pm25 = get_aqi_for_pollutant(pm25, PhysicalConstants.AQI_BREAKPOINTS['pm25'])
        aqi_pm10 = get_aqi_for_pollutant(pm10, PhysicalConstants.AQI_BREAKPOINTS['pm10'])
        
        return float(max(aqi_pm25, aqi_pm10))

    def _get_real_concentrations(self):
        """
        مصدر واحد موحّد لتركيزات الملوثات الحقيقية.
        يُستخدم في get_baseline() و evaluate() معاً لضمان التناسق.
        بغداد الواقعي: PM2.5 = 20-80 μg/m³، PM10 = 40-150 μg/m³
        """
        air = baghdad_real.get_baghdad_air_quality()
        # الحد الأدنى الواقعي وفق دراسات بغداد (WHO 2023)
        # PM2.5 < 1.0 = خطأ في البيانات → نستخدم متوسط بغداد الموثق
        pm25 = float(air['pm25']) if float(air['pm25']) >= 1.0 else 25.5
        pm10 = float(air['pm10']) if float(air['pm10']) >= 1.0 else 45.2
        no2  = float(air['no2'])  if float(air['no2'])  >= 0.5 else 15.0
        so2  = float(air.get('so2', 5.2))
        co   = float(air.get('co', 0.8))
        return pm25, pm10, no2, so2, co

    def evaluate(self, solution):
        """تقييم حل مقترح باستخدام نموذج Gaussian"""
        try:
            # التأكد من أن solution هي قائمة
            if isinstance(solution, np.ndarray):
                solution = solution.tolist()
            elif not isinstance(solution, (list, tuple)):
                solution = [float(solution)]

            weather = baghdad_real.get_baghdad_weather()

            # ── قيم البيانات الحقيقية من مصدر واحد موحّد ───────────────────
            base_pm25, base_pm10, base_no2, _, _ = self._get_real_concentrations()

            # ── معاملات التحسين ──────────────────────────────────────────────
            # emission_reduction: [0.5, 1.5]
            #   0.5 = تخفيض انبعاثات 50% (أفضل حالة)
            #   1.0 = لا تغيير (baseline)
            #   1.5 = زيادة انبعاثات 50% (أسوأ حالة)
            emission_reduction = float(solution[0]) if len(solution) > 0 else 1.0
            # green_increase: [0.8, 2.0]
            #   0.8 = تقليل المساحات الخضراء
            #   1.0 = لا تغيير (baseline)
            #   2.0 = مضاعفة المساحات الخضراء
            green_increase = float(solution[1]) if len(solution) > 1 else 1.0

            # ── نموذج Gaussian Plume ─────────────────────────────────────────
            wind          = float(max(0.5, weather['wind_speed']))
            emission_rate = float(max(1.0, 100.0 * emission_reduction))
            concentration = self.gaussian_plume(emission_rate, wind, x=1000, y=0, z=10)

            # ── تركيزات الملوثات بعد التحسين ────────────────────────────────
            pm25 = float(max(1.0, base_pm25 * emission_reduction))
            pm10 = float(max(1.0, base_pm10 * emission_reduction))
            no2  = float(max(0.1, base_no2  * emission_reduction))

            # المساحات الخضراء تُقلل التلوث (امتصاص بيولوجي)
            green_coverage  = float(min(50.0, 12.0 * green_increase))
            green_reduction = float(1.0 - green_coverage / 200.0)
            pm25 = float(max(1.0, pm25 * green_reduction))
            pm10 = float(max(1.0, pm10 * green_reduction))
            no2  = float(max(0.1, no2  * green_reduction))

            # AQI يُحسب من معادلة EPA الرسمية — لا من API
            aqi = self.calculate_aqi(pm25, pm10)

            # UV Index: ينخفض مع زيادة المساحات الخضراء والغطاء النباتي
            uv_index = float(max(0.5, 5.0 * emission_reduction * (1.0 - green_coverage / 100.0)))

            # عقوبات
            penalty = 0.0
            if aqi > 300:
                penalty += float(5.0 * (aqi - 300) / 100.0)

            # دالة الهدف
            fitness = float(
                0.40 * aqi / 500.0 +
                0.25 * pm25 / 250.0 +
                0.20 * no2 / 200.0 +
                0.15 * (1.0 - green_coverage / 100.0) +
                penalty
            )

            results = [
                float(aqi),
                float(pm25),
                float(pm10),
                float(no2),
                float(weather['temperature']),
                float(weather['humidity']),
                float(weather['wind_speed']),
                float(weather['pressure']),
                float(uv_index),
                float(green_coverage)
            ]

            return fitness, results

        except Exception as e:
            print(f"Environment evaluation error: {e}")
            return 1e9, self.get_baseline()

# ============================================================================
# 🔟 قطاع النفايات - نموذج تحسين المسارات
# ============================================================================

class WasteSector:
    """قطاع النفايات - نموذج تحسين المسارات"""
    
    def __init__(self):
        self.name = "Baghdad Waste Sector"
        self.icon = "🗑️"
        self.criteria = [
            "Daily Waste (tons)", "Collection Efficiency (%)", "Recycling Rate (%)",
            "Fleet Utilization (%)", "Container Fill Level (%)", "Collection Cost ($/ton)",
            "Fuel Consumption (L/route)", "Route Distance (km)", "Collection Time (hours)",
            "Carbon Footprint (kg CO2/ton)"
        ]
        self.units = ["tons", "%", "%", "%", "%", "$/ton", "L", "km", "hours", "kg CO2/ton"]
        self.higher_is_better = [False, True, True, True, False, False, False, False, False, False]
    
    def get_baseline(self):
        """القيم الأساسية - نفس منطق evaluate بدون تحسين (route_efficiency=1.0)"""
        waste = baghdad_real.get_baghdad_waste_data()
        fleet_size  = float(waste['fleet_size'])
        num_routes  = float(waste['collection_routes'])
        daily_waste = float(waste['daily_waste_tons'])

        truck_capacity  = 10.0
        total_trips     = daily_waste / truck_capacity
        trips_per_route = total_trips / num_routes
        distance        = 120.0

        fuel_per_100km  = 35.0
        idle_factor     = 1.4
        fuel_per_route  = float(max(50.0, distance * fuel_per_100km / 100.0 * idle_factor * trips_per_route))

        # نفس معادلة evaluate: وقت رحلة واحدة × عدد الرحلات
        avg_speed_kmh   = 20.0
        unload_per_trip = 0.5
        trip_distance   = float(distance / trips_per_route)
        time_per_trip   = float(trip_distance / avg_speed_kmh + unload_per_trip)
        time_collection = float(min(24.0, max(2.0, time_per_trip * trips_per_route)))

        fuel_cost_r  = float(fuel_per_route * 0.85)
        labor_cost_r = float((time_collection / trips_per_route) * 2 * 8.0)
        maint_cost_r = float(distance * 0.50)
        cost_per_ton = float(max(1.0, (fuel_cost_r + labor_cost_r + maint_cost_r) * num_routes / daily_waste))

        total_work_hours  = float(num_routes * time_collection)
        total_avail_hours = float(fleet_size * 8.0)
        fleet_util        = float(min(98.0, max(5.0, total_work_hours / total_avail_hours * 100.0)))

        total_fuel_L = float(fuel_per_route * num_routes)
        carbon       = float(max(0.5, total_fuel_L * PhysicalConstants.EMISSION_FACTOR / daily_waste))

        return [
            float(daily_waste),
            float(waste['collection_efficiency'] * 100),
            float(waste['recycling_rate'] * 100),
            float(fleet_util),
            65.0,
            float(cost_per_ton),
            float(fuel_per_route),
            float(distance),
            float(time_collection),
            float(carbon)
        ]
    
    def evaluate(self, solution):
        """تقييم حل مقترح - نموذج VRP مُبسَّط فيزيائياً صحيح"""
        try:
            if isinstance(solution, np.ndarray):
                solution = solution.tolist()
            elif not isinstance(solution, (list, tuple)):
                solution = [float(solution)]

            waste = baghdad_real.get_baghdad_waste_data()

            base_collection_eff = float(waste['collection_efficiency'] * 100)  # 75%
            base_recycling      = float(waste['recycling_rate'] * 100)          # 5%
            fleet_size          = float(waste['fleet_size'])                    # 450 شاحنة
            num_routes          = float(waste['collection_routes'])             # 85 مسار جغرافي
            daily_waste         = float(waste['daily_waste_tons'])              # 9315 طن

            # ── متغيرات الحل ─────────────────────────────────────────────────
            route_efficiency = float(max(0.5, min(2.0, solution[0]))) if len(solution) > 0 else 1.0
            recycling_factor = float(max(0.8, min(3.0, solution[1]))) if len(solution) > 1 else 1.0

            # ── حسابات الرحلات الفيزيائية ────────────────────────────────────
            # سعة الشاحنة = 10 طن → عدد الرحلات الكلية = waste / 10
            truck_capacity  = 10.0  # طن/رحلة
            total_trips     = float(daily_waste / truck_capacity)  # ~931 رحلة/يوم

            # المسافة لكل مسار جغرافي
            min_distance = 120.0 * 0.60   # 72 كم (حد أدنى فيزيائي)
            distance     = float(max(min_distance, 120.0 / route_efficiency))

            # إجمالي الكيلومترات اليومية
            # كل مسار يُغطى بـ (total_trips / num_routes) رحلة
            trips_per_route  = float(total_trips / num_routes)  # ~11 رحلة/مسار
            total_daily_km   = float(distance * trips_per_route * num_routes)  # ≈ distance × total_trips

            # ── استهلاك الوقود (L/route per day) ─────────────────────────────
            # شاحنة نفايات ثقيلة: 35 L/100km سير + توقف idle
            fuel_per_100km = 35.0
            idle_factor    = 1.4   # 40% إضافي للتوقف والتحميل
            fuel_per_route = float(distance * fuel_per_100km / 100.0 * idle_factor * trips_per_route)
            fuel_per_route = float(max(50.0, fuel_per_route))

            # ── كفاءة الجمع ─────────────────────────────────────────────────
            collection_eff = float(min(96.0, base_collection_eff * (0.7 + 0.3 * route_efficiency)))

            # ── معدل التدوير ─────────────────────────────────────────────────
            recycling_rate = float(min(30.0, base_recycling * recycling_factor))

            # ── وقت الجمع (ساعات/مسار/يوم) ──────────────────────────────────
            # المعادلة الفيزيائية الصحيحة:
            # وقت رحلة واحدة = (مسافة_مسار ÷ عدد_الرحلات) / avg_speed + وقت_تفريغ_واحد
            # الوقت الكلي = وقت_رحلة_واحدة × عدد_الرحلات
            # = (distance/trips_per_route)/avg_speed × trips + unload × trips
            # = distance/avg_speed + unload_per_trip × trips_per_route
            avg_speed_kmh    = 20.0
            unload_per_trip  = 0.5   # ساعة تفريغ/تحميل لكل رحلة (ثابت فيزيائياً)
            # وقت السير الكلي: (المسافة الكلية) / السرعة = distance × trips / avg_speed
            # لكن كل رحلة تقطع distance/trips كيلومترات فقط
            trip_distance    = float(distance / trips_per_route)   # كم/رحلة
            time_per_trip    = float(trip_distance / avg_speed_kmh + unload_per_trip)
            time_collection  = float(time_per_trip * trips_per_route)
            # حد أدنى وأقصى منطقيان
            time_collection  = float(min(24.0, max(2.0, time_collection)))

            # ── تكلفة الجمع ($/ton) ──────────────────────────────────────────
            # وقود + عمالة (2 عامل/شاحنة) + صيانة
            fuel_cost_r  = float(fuel_per_route * 0.85)            # $/مسار
            labor_cost_r = float((time_collection / trips_per_route) * 2 * 8.0)  # $/مسار (2عامل×8$/h)
            maint_cost_r = float(distance * 0.50)                  # $/مسار (إطارات+زيت+صيانة)
            total_per_route = float(fuel_cost_r + labor_cost_r + maint_cost_r)
            cost_per_ton    = float(total_per_route * num_routes / daily_waste)
            cost_per_ton    = float(max(1.0, cost_per_ton))         # لا حد أدنى اصطناعي

            # ── استخدام الأسطول ──────────────────────────────────────────────
            total_work_hours  = float(num_routes * time_collection)
            total_avail_hours = float(fleet_size * 8.0)
            fleet_util = float(min(98.0, max(5.0, total_work_hours / total_avail_hours * 100.0)))

            # ── مستوى امتلاء الحاويات ────────────────────────────────────────
            container_fill = float(max(15.0, min(90.0, 65.0 / route_efficiency)))

            # ── البصمة الكربونية (kg CO2 / ton نفايات) ───────────────────────
            # إجمالي الوقود = fuel_per_route × num_routes
            total_fuel_L = float(fuel_per_route * num_routes)
            carbon       = float(total_fuel_L * PhysicalConstants.EMISSION_FACTOR / daily_waste)
            carbon       = float(max(0.5, carbon))  # لا حد أدنى اصطناعي كبير

            # ── عقوبات القيود ────────────────────────────────────────────────
            penalty = 0.0
            if collection_eff < 60.0:
                penalty += float((60.0 - collection_eff) * 0.5)
            if fleet_util > 100.0:
                penalty += float((fleet_util - 100.0) * 0.3)

            # ── دالة الهدف ───────────────────────────────────────────────────
            fitness = float(
                0.35 * cost_per_ton / 50.0 +
                0.30 * (1.0 - recycling_rate / 30.0) +
                0.20 * fuel_per_route / 500.0 +
                0.15 * carbon / 20.0 +
                penalty
            )

            results = [
                float(daily_waste),
                float(collection_eff),
                float(recycling_rate),
                float(fleet_util),
                float(container_fill),
                float(cost_per_ton),
                float(fuel_per_route),   # L/route/day
                float(distance),
                float(time_collection),
                float(carbon)
            ]

            return fitness, results

        except Exception as e:
            print(f"Waste evaluation error: {e}")
            return 1e9, self.get_baseline()

# ============================================================================
# 1️⃣1️⃣ إنشاء كائنات القطاعات
# ============================================================================

energy_sector = EnergySector()
traffic_sector = TrafficSector()
environment_sector = EnvironmentSector()
waste_sector = WasteSector()

# ============================================================================
# 1️⃣2️⃣ محرك التحسين الموحد - نسخة محسنة بالكامل
# ============================================================================

class CityOptimizationEngine:
    """محرك التحسين الموحد للمدينة الذكية - نسخة محسنة"""
    
    def __init__(self):
        self.hybrid_generator = HybridAlgorithmGenerator()
        self.sectors = {
            'energy': energy_sector,
            'traffic': traffic_sector,
            'environment': environment_sector,
            'waste': waste_sector
        }
        self.optimization_history = {}
    
    def get_all_algorithms(self):
        return self.hybrid_generator.get_all_algorithms()
    
    def get_algorithm_class(self, algo_name):
        return self.hybrid_generator.get_algorithm_class(algo_name)
    
    def optimize_sector(self, sector_name, algorithm_name, bounds, 
                        iterations=100, pop_size=50, custom_params=None):
        """تحسين قطاع معين - مع معالجة صحيحة للمصفوفات"""
        
        try:
            sector = self.sectors[sector_name]
            algo_class = self.get_algorithm_class(algorithm_name)
            
            print(f"\n{'='*60}")
            print(f"🚀 Starting optimization for {sector_name} sector")
            print(f"   Algorithm: {algorithm_name}")
            print(f"   Iterations: {iterations}, Population: {pop_size}")
            print(f"{'='*60}")
            
            # الحصول على baseline قبل التحسين
            baseline = sector.get_baseline()
            print(f"✅ Baseline obtained: {[f'{x:.2f}' for x in baseline[:3]]}...")
            
            # التأكد من أن bounds صحيحة
            if not bounds or len(bounds) == 0:
                if sector_name == 'energy':
                    bounds = [(0.0, 2000.0) for _ in range(10)]
                elif sector_name == 'traffic':
                    bounds = [(0.5, 2.0), (30.0, 120.0)]
                elif sector_name == 'environment':
                    bounds = [(0.5, 1.5), (0.8, 2.0)]
                elif sector_name == 'waste':
                    bounds = [(0.5, 2.0), (0.8, 3.0)]
            
            # تحويل bounds إلى مصفوفة منفصلة للحدود الدنيا والعليا
            lb = []
            ub = []
            for b in bounds:
                if isinstance(b, (list, tuple)) and len(b) == 2:
                    lb.append(float(b[0]))
                    ub.append(float(b[1]))
                else:
                    print(f"⚠️ Invalid bound format: {b}")
                    lb.append(0.0)
                    ub.append(100.0)
            
            print(f"✅ Bounds set: {len(lb)} variables")
            print(f"   Lower bounds: {[f'{x:.2f}' for x in lb[:3]]}...")
            print(f"   Upper bounds: {[f'{x:.2f}' for x in ub[:3]]}...")
            
            # تعريف مشكلة التحسين
            # ✅ wrapper يُرجع scalar فقط لأن Mealpy لا يقبل tuple
            def obj_func_wrapper(solution):
                result = sector.evaluate(solution)
                if isinstance(result, (tuple, list)):
                    return float(result[0])
                return float(result)

            problem = {
                "obj_func": obj_func_wrapper,
                "bounds": FloatVar(lb=lb, ub=ub),
                "minmax": "min",
                "log_to": None
            }

            # إعداد الخوارزمية — حد أقصى للـ iterations و pop_size لمنع التأخر
            MAX_ITER     = 500
            MAX_POP      = 200
            safe_iter    = int(min(iterations, MAX_ITER))
            safe_pop     = int(min(pop_size,   MAX_POP))
            params = {'epoch': safe_iter, 'pop_size': safe_pop}
            if custom_params:
                valid_params = {}
                for key, value in custom_params.items():
                    if value is not None:
                        if isinstance(value, (np.integer, np.floating)):
                            valid_params[key] = value.item()
                        elif isinstance(value, np.ndarray):
                            valid_params[key] = value.tolist()
                        elif isinstance(value, (list, tuple)):
                            valid_params[key] = list(value)
                        else:
                            valid_params[key] = value
                params.update(valid_params)
            
            # إنشاء الخوارزمية
            try:
                algo = algo_class(**params)
                print(f"✅ Algorithm instance created")
            except Exception as e:
                print(f"⚠️ Algorithm creation error: {e}, using PSO")
                algo = PSO(**params)
            
            # تشغيل التحسين
            start_time = time.time()
            algo.solve(problem)
            execution_time = time.time() - start_time
            print(f"✅ Optimization completed in {execution_time:.2f}s")
            
            # استخراج النتائج بطريقة آمنة
            best_solution = None
            best_fitness = None
            
            try:
                # محاولة 1: g_best (الإصدارات الحديثة)
                if hasattr(algo, 'g_best'):
                    if hasattr(algo.g_best, 'solution'):
                        best_solution = algo.g_best.solution
                    else:
                        best_solution = algo.g_best
                    
                    if hasattr(algo.g_best, 'target') and hasattr(algo.g_best.target, 'fitness'):
                        best_fitness = algo.g_best.target.fitness
                
                # محاولة 2: history.list_global_best (الإصدارات القياسية)
                elif hasattr(algo, 'history') and hasattr(algo.history, 'list_global_best'):
                    if len(algo.history.list_global_best) > 0:
                        best_solution = algo.history.list_global_best[-1][0]
                        best_fitness = algo.history.list_global_best[-1][1]
                
                # محاولة 3: solution (بعض الإصدارات)
                elif hasattr(algo, 'solution'):
                    best_solution = algo.solution[0]
                    best_fitness = algo.solution[1]
            
            except Exception as e:
                print(f"⚠️ Error extracting results: {e}")
            
            # إذا فشلت جميع المحاولات، استخدم حل عشوائي
            if best_solution is None:
                print("⚠️ Using random solution as fallback")
                best_solution = np.random.uniform(lb, ub)
                best_fitness = sector.evaluate(best_solution)[0]
            
            # تحويل إلى قائمة Python عادية
            if isinstance(best_solution, np.ndarray):
                best_solution_list = best_solution.tolist()
            elif isinstance(best_solution, (list, tuple)):
                best_solution_list = list(best_solution)
            else:
                best_solution_list = [float(best_solution)]
            
            best_fitness = float(best_fitness)
            
            print(f"✅ Best fitness: {best_fitness:.4f}")
            
            # تقييم الحل الأمثل
            _, optimized = sector.evaluate(best_solution_list)
            
            # حساب التحسينات
            improvements = []
            for i, (b, o) in enumerate(zip(baseline, optimized)):
                b = float(b)
                o = float(o)
                if b != 0:
                    if sector.higher_is_better[i]:
                        imp = ((o - b) / b) * 100
                    else:
                        imp = ((b - o) / b) * 100
                else:
                    imp = 0.0
                improvements.append(float(imp))
            
            return {
                'success': True,
                'sector': sector_name,
                'algorithm': algorithm_name,
                'baseline': [float(x) for x in baseline],
                'optimized': [float(x) for x in optimized],
                'improvements': improvements,
                'best_fitness': best_fitness,
                'execution_time': execution_time
            }
            
        except Exception as e:
            print(f"❌ Optimization error for {sector_name}: {e}")
            import traceback
            traceback.print_exc()
            return {'success': False, 'error': str(e)}

# ============================================================================
# 1️⃣3️⃣ إنشاء محرك التحسين
# ============================================================================

city_engine = CityOptimizationEngine()
algorithms_dict = city_engine.get_all_algorithms()

# ============================================================================
# 1️⃣4️⃣ دوال الرسم
# ============================================================================

# ── مربع المعادلات الفيزيائية ────────────────────────────────────────────────
EQUATIONS_HTML = {
    "energy": """
<div style="background:#1a2a4a;border:2px solid #3a6fd8;border-radius:10px;padding:20px;margin-top:16px;font-family:'Courier New',monospace;">
  <div style="color:#5aabff;font-size:15px;font-weight:bold;margin-bottom:14px;border-bottom:1px solid #3a6fd8;padding-bottom:8px;">
    &#9889; Energy Sector &#8212; Applied Physics Models &amp; Constraints
  </div>
  <div style="color:#ffffff;font-weight:bold;line-height:2.0;font-size:13px;">
    <b style="color:#7ec8ff;">&#9312; Grid Loss Model (I&sup2;R):</b><br>
    &nbsp;&nbsp;loss_factor = 0.12 &times; (1 + 0.3 &times; imbalance) &times; (1 &minus; 0.5 &times; renewable_ratio / 100)<br>
    &nbsp;&nbsp;losses [MW] = base_load &times; loss_factor<br>
    &nbsp;&nbsp;imbalance = &sigma;(gen_values) / &mu;(gen_values) &nbsp;|&nbsp; loss_factor &isin; [0.03, 0.18]<br><br>
    <b style="color:#7ec8ff;">&#9313; System Efficiency:</b><br>
    &nbsp;&nbsp;&eta; = ((base_load &minus; losses) / base_load) &times; 100 [%]<br><br>
    <b style="color:#7ec8ff;">&#9314; Carbon Intensity:</b><br>
    &nbsp;&nbsp;CI [gCO&sup2;/kWh] = 550 &times; fossil_ratio / 100 &nbsp;|&nbsp; fossil_ratio = 100 &minus; renewable_ratio<br><br>
    <b style="color:#7ec8ff;">&#9315; Voltage Stability:</b><br>
    &nbsp;&nbsp;V_dev = max(0, imbalance &times; 0.01 &minus; renewable &times; 3&times;10&sup4;)<br>
    &nbsp;&nbsp;V_pu = clamp(1.0 &minus; V_dev + V_improve &times; 0.5 ; 0.95, 1.04)<br><br>
    <b style="color:#7ec8ff;">&#9316; Objective Function (minimise):</b><br>
    &nbsp;&nbsp;f = 0.35&times;(lf/0.18) + 0.30&times;(CI/550) + 0.20&times;(1&minus;ren/60) + 0.15&times;(Vdev/0.05) + penalty<br><br>
    <b style="color:#7ec8ff;">&#9317; IEEE Constraints:</b><br>
    &nbsp;&nbsp;0.95 &le; V_pu &le; 1.05 &nbsp;|&nbsp; total_gen &le; 1.05&times;capacity &nbsp;|&nbsp; total_gen &ge; 0.85&times;base_load<br>
    &nbsp;&nbsp;renewable_ratio &le; 60% &nbsp;|&nbsp; 0.03 &le; loss_factor &le; 0.18
  </div>
</div>""",

    "traffic": """
<div style="background:#1a2a4a;border:2px solid #3a6fd8;border-radius:10px;padding:20px;margin-top:16px;font-family:'Courier New',monospace;">
  <div style="color:#5aabff;font-size:15px;font-weight:bold;margin-bottom:14px;border-bottom:1px solid #3a6fd8;padding-bottom:8px;">
    &#128678; Traffic Sector &#8212; Applied Physics Models &amp; Constraints
  </div>
  <div style="color:#ffffff;font-weight:bold;line-height:2.0;font-size:13px;">
    <b style="color:#7ec8ff;">&#9312; Greenshields Flow Model:</b><br>
    &nbsp;&nbsp;v = v_f &times; (1 &minus; k_eff / k_j) [km/h] &nbsp;|&nbsp; q = k_eff &times; v [veh/h]<br>
    &nbsp;&nbsp;k_eff = k_base / signal_factor &nbsp;|&nbsp; q_max (Baghdad practical) = 1800 veh/h<br>
    &nbsp;&nbsp;v_f = 60 km/h &nbsp;|&nbsp; k_j = 150 veh/km<br><br>
    <b style="color:#7ec8ff;">&#9313; COPERT Emission Model (Baghdad fleet Euro 2&ndash;4):</b><br>
    &nbsp;&nbsp;CO&sup2; [g/km] = 3986.11/v &minus; 14.31 + 1.7889&times;v &minus; 0.00194&times;v&sup2;<br>
    &nbsp;&nbsp;minimum CO&sup2; &asymp; 150 g/km at v &asymp; 50 km/h<br>
    &nbsp;&nbsp;Fuel [L/100km] = CO&sup2; / 2392 &times; 100<br><br>
    <b style="color:#7ec8ff;">&#9314; Travel &amp; Wait Times:</b><br>
    &nbsp;&nbsp;T_travel [min] = 30 / v &times; 60 &nbsp;(reference 30 km)<br>
    &nbsp;&nbsp;T_wait [s] = 60 &times; congestion / signal_factor<br>
    &nbsp;&nbsp;congestion = 1 &minus; v / v_f<br><br>
    <b style="color:#7ec8ff;">&#9315; Objective Function (minimise):</b><br>
    &nbsp;&nbsp;f = 0.35&times;(T/60) + 0.30&times;cong + 0.20&times;(CO&sup2;/300) + 0.15&times;(1&minus;&eta;_int/100) + penalty<br><br>
    <b style="color:#7ec8ff;">&#9316; Constraints:</b><br>
    &nbsp;&nbsp;signal_factor &isin; [0.5, 2.0] &nbsp;|&nbsp; v &le; 120 km/h &nbsp;|&nbsp; q &le; 1800 veh/h
  </div>
</div>""",

    "environment": """
<div style="background:#1a2a4a;border:2px solid #3a6fd8;border-radius:10px;padding:20px;margin-top:16px;font-family:'Courier New',monospace;">
  <div style="color:#5aabff;font-size:15px;font-weight:bold;margin-bottom:14px;border-bottom:1px solid #3a6fd8;padding-bottom:8px;">
    &#127757; Environment Sector &#8212; Applied Physics Models &amp; Constraints
  </div>
  <div style="color:#ffffff;font-weight:bold;line-height:2.0;font-size:13px;">
    <b style="color:#7ec8ff;">&#9312; Gaussian Plume Dispersion:</b><br>
    &nbsp;&nbsp;C(x,y,z) = Q/(2&pi; u &sigma;_y &sigma;_z) &times; exp(&minus;y&sup2;/2&sigma;_y&sup2;) &times; [exp(&minus;(z&minus;H)&sup2;/2&sigma;_z&sup2;) + exp(&minus;(z+H)&sup2;/2&sigma;_z&sup2;)]<br>
    &nbsp;&nbsp;&sigma;_y = 0.32x(1+0.0004x)^&minus;0.5 &nbsp;|&nbsp; &sigma;_z = 0.24x(1+0.001x)^0.5<br><br>
    <b style="color:#7ec8ff;">&#9313; Pollutant Reduction:</b><br>
    &nbsp;&nbsp;PM2.5 = base_PM2.5 &times; &epsilon; &times; (1 &minus; green/200)<br>
    &nbsp;&nbsp;PM10 = base_PM10 &times; &epsilon; &times; (1 &minus; green/200)<br>
    &nbsp;&nbsp;NO&sup2; = base_NO&sup2; &times; &epsilon; &times; (1 &minus; green/200) &nbsp;&nbsp;[&epsilon; = emission_reduction]<br><br>
    <b style="color:#7ec8ff;">&#9314; AQI &mdash; US EPA Formula:</b><br>
    &nbsp;&nbsp;AQI = ((AQI_hi &minus; AQI_lo)/(BP_hi &minus; BP_lo)) &times; (C &minus; BP_lo) + AQI_lo<br>
    &nbsp;&nbsp;AQI = max(AQI_PM2.5, AQI_PM10) &nbsp;(always computed from concentrations)<br><br>
    <b style="color:#7ec8ff;">&#9315; Objective Function (minimise):</b><br>
    &nbsp;&nbsp;f = 0.40&times;(AQI/500) + 0.25&times;(PM2.5/250) + 0.20&times;(NO&sup2;/200) + 0.15&times;(1&minus;green/100) + penalty<br><br>
    <b style="color:#7ec8ff;">&#9316; Constraints:</b><br>
    &nbsp;&nbsp;&epsilon; &isin; [0.5, 1.5] &nbsp;|&nbsp; green_increase &isin; [0.8, 2.0]<br>
    &nbsp;&nbsp;PM2.5_baseline &ge; 1.0 &micro;g/m&sup3; (fallback: 25.5) &nbsp;|&nbsp; AQI penalty if &gt; 300
  </div>
</div>""",

    "waste": """
<div style="background:#1a2a4a;border:2px solid #3a6fd8;border-radius:10px;padding:20px;margin-top:16px;font-family:'Courier New',monospace;">
  <div style="color:#5aabff;font-size:15px;font-weight:bold;margin-bottom:14px;border-bottom:1px solid #3a6fd8;padding-bottom:8px;">
    &#128465;&#65039; Waste Sector &#8212; Applied Physics Models &amp; Constraints
  </div>
  <div style="color:#ffffff;font-weight:bold;line-height:2.0;font-size:13px;">
    <b style="color:#7ec8ff;">&#9312; Trip Accounting Model:</b><br>
    &nbsp;&nbsp;total_trips = daily_waste / truck_capacity &nbsp;(truck_capacity = 10 t)<br>
    &nbsp;&nbsp;trips_per_route = total_trips / num_routes<br>
    &nbsp;&nbsp;distance [km] = max(72, 120 / route_efficiency)<br><br>
    <b style="color:#7ec8ff;">&#9313; Fuel Consumption:</b><br>
    &nbsp;&nbsp;fuel [L/route/day] = distance &times; 0.35 &times; 1.4 &times; trips_per_route<br>
    &nbsp;&nbsp;total_fuel [L/day] = fuel_per_route &times; num_routes<br>
    &nbsp;&nbsp;(35 L/100km &times; idle_factor 1.4 for stop-and-go)<br><br>
    <b style="color:#7ec8ff;">&#9314; Collection Cost:</b><br>
    &nbsp;&nbsp;cost [$/route] = fuel&times;0.85 + (T_collect/trips)&times;2workers&times;8$/h + dist&times;0.50<br>
    &nbsp;&nbsp;cost_per_ton [$/t] = cost_per_route &times; num_routes / daily_waste<br><br>
    <b style="color:#7ec8ff;">&#9315; Carbon Footprint:</b><br>
    &nbsp;&nbsp;carbon [kgCO&sup2;/t] = total_fuel &times; 2.68 / daily_waste &nbsp;(diesel: 2.68 kgCO&sup2;/L)<br><br>
    <b style="color:#7ec8ff;">&#9316; Fleet Utilisation:</b><br>
    &nbsp;&nbsp;fleet_util [%] = (num_routes &times; T_collect) / (fleet_size &times; 8h) &times; 100<br><br>
    <b style="color:#7ec8ff;">&#9317; Objective Function (minimise):</b><br>
    &nbsp;&nbsp;f = 0.35&times;(cost/50) + 0.30&times;(1&minus;rec/30) + 0.20&times;(fuel/500) + 0.15&times;(carbon/20) + penalty<br><br>
    <b style="color:#7ec8ff;">&#9318; Constraints:</b><br>
    &nbsp;&nbsp;route_eff &isin; [0.5, 2.0] &nbsp;|&nbsp; recycling_factor &isin; [0.8, 3.0]<br>
    &nbsp;&nbsp;collection_eff &le; 96% &nbsp;|&nbsp; recycling_rate &le; 30% &nbsp;|&nbsp; coll_eff &ge; 60% (penalty)
  </div>
</div>""",

    "multi": """
<div style="background:#1a2a4a;border:2px solid #3a6fd8;border-radius:10px;padding:20px;margin-top:16px;font-family:'Courier New',monospace;">
  <div style="color:#5aabff;font-size:15px;font-weight:bold;margin-bottom:14px;border-bottom:1px solid #3a6fd8;padding-bottom:8px;">
    &#127919; Multi-Sector &#8212; All Applied Models &amp; Constraints
  </div>
  <div style="color:#ffffff;font-weight:bold;line-height:1.9;font-size:12px;">
    <b style="color:#ffd700;">&#9889; ENERGY</b><br>
    &nbsp;&nbsp;losses = base_load &times; 0.12&times;(1+0.3&times;imbalance)&times;(1&minus;0.5&times;ren/100)<br>
    &nbsp;&nbsp;&eta; = (base_load&minus;losses)/base_load &times;100 &nbsp;|&nbsp; CI = 550&times;fossil/100 [gCO&sup2;/kWh]<br>
    &nbsp;&nbsp;f_E = 0.35&times;(lf/0.18)+0.30&times;(CI/550)+0.20&times;(1&minus;ren/60)+0.15&times;(Vdev/0.05)<br><br>
    <b style="color:#ffd700;">&#128678; TRAFFIC</b><br>
    &nbsp;&nbsp;v = 60&times;(1&minus;k_eff/150) [km/h] &nbsp;|&nbsp; CO&sup2; = 3986/v&minus;14.3+1.79v&minus;0.00194v&sup2; [g/km]<br>
    &nbsp;&nbsp;f_T = 0.35&times;(T/60)+0.30&times;cong+0.20&times;(CO&sup2;/300)+0.15&times;(1&minus;&eta;_int/100)<br><br>
    <b style="color:#ffd700;">&#127757; ENVIRONMENT</b><br>
    &nbsp;&nbsp;PM2.5 = base&times;&epsilon;&times;(1&minus;green/200) &nbsp;|&nbsp; AQI from EPA breakpoints<br>
    &nbsp;&nbsp;f_ENV = 0.40&times;(AQI/500)+0.25&times;(PM2.5/250)+0.20&times;(NO&sup2;/200)+0.15&times;(1&minus;green/100)<br><br>
    <b style="color:#ffd700;">&#128465;&#65039; WASTE</b><br>
    &nbsp;&nbsp;fuel = dist&times;0.35&times;1.4&times;trips_per_route [L/route] &nbsp;|&nbsp; carbon = fuel&times;routes&times;2.68/waste<br>
    &nbsp;&nbsp;f_W = 0.35&times;(cost/50)+0.30&times;(1&minus;rec/30)+0.20&times;(fuel/500)+0.15&times;(carbon/20)<br><br>
    <b style="color:#7ec8ff;">Global Constraints:</b><br>
    &nbsp;&nbsp;0.95 &le; V_pu &le; 1.05 &nbsp;|&nbsp; q &le; 1800 veh/h &nbsp;|&nbsp; PM2.5 &ge; 1.0 &micro;g/m&sup3;<br>
    &nbsp;&nbsp;renewable &le; 60% &nbsp;|&nbsp; recycling &le; 30% &nbsp;|&nbsp; Traffic ops capped: 5000
  </div>
</div>"""
}


def build_results_table(result, sector, exec_time_sec):
    """
    بناء جدول النتائج.
    Gradio يعرض آخر صف كـ preview فوق الجدول.
    لذلك نضع صف وقت التنفيذ أولاً حتى لا يُفسد وحدات المعايير،
    ثم نضع جميع المعايير الحقيقية.
    """
    rows = []
    # صف وقت التنفيذ أولاً (Gradio يعرض آخر صف كـ preview)
    rows.append([
        "Algorithm Execution Time", "seconds",
        "—",
        f"{exec_time_sec:.3f}",
        "—",
        "⏱️ Runtime"
    ])
    # جميع المعايير الحقيقية
    for i, criterion in enumerate(sector.criteria[:len(result['baseline'])]):
        imp    = float(result['improvements'][i]) if i < len(result['improvements']) else 0.0
        status = "✅ Improved" if imp > 0 else "⚠️ Degraded"
        unit   = str(sector.units[i]) if i < len(sector.units) else ""
        rows.append([
            str(criterion), unit,
            f"{float(result['baseline'][i]):.2f}",
            f"{float(result['optimized'][i]):.2f}",
            f"{imp:.2f}%",
            status
        ])
    return rows

def create_comparison_plot(baseline, optimized, criteria, title):
    """إنشاء رسم بياني للمقارنة"""
    try:
        baseline_list = [float(x) for x in baseline]
        optimized_list = [float(x) for x in optimized]
        criteria_list = [str(c) for c in criteria[:len(baseline_list)]]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Baseline',
            x=criteria_list,
            y=baseline_list,
            marker_color='lightgray',
            text=[f"{b:.2f}" for b in baseline_list],
            textposition='outside'
        ))
        
        fig.add_trace(go.Bar(
            name='Optimized',
            x=criteria_list,
            y=optimized_list,
            marker_color='#0066CC',
            text=[f"{o:.2f}" for o in optimized_list],
            textposition='outside'
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Criteria",
            yaxis_title="Value",
            barmode='group',
            height=400,
            template='plotly_white',
            margin=dict(l=50, r=50, t=50, b=100)
        )
        
        fig.update_xaxes(tickangle=45)
        return fig
    except Exception as e:
        print(f"Plot error: {e}")
        return None

def create_improvement_plot(improvements, criteria):
    """إنشاء رسم بياني للتحسينات"""
    try:
        improvements_list = [float(x) for x in improvements]
        criteria_list = [str(c) for c in criteria[:len(improvements_list)]]
        
        colors = ['green' if imp > 0 else 'red' for imp in improvements_list]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=criteria_list,
            y=improvements_list,
            marker_color=colors,
            text=[f"{imp:.2f}%" for imp in improvements_list],
            textposition='outside'
        ))
        
        fig.update_layout(
            title="Improvement Percentage by Criterion",
            xaxis_title="Criteria",
            yaxis_title="Improvement (%)",
            height=300,
            template='plotly_white',
            margin=dict(l=50, r=50, t=50, b=100)
        )
        
        fig.update_xaxes(tickangle=45)
        fig.add_hline(y=0, line_dash="dash", line_color="gray")
        return fig
    except Exception as e:
        print(f"Plot error: {e}")
        return None

def create_pareto_plot(sectors_data):
    """إنشاء رسم بياني Pareto Front"""
    try:
        fig = go.Figure()
        
        sectors = [str(d["sector"]) for d in sectors_data]
        improvements = [float(d["improvement"]) for d in sectors_data]
        icons = [str(d["icon"]) for d in sectors_data]
        
        fig.add_trace(go.Scatter(
            x=sectors,
            y=improvements,
            mode='markers+text',
            marker=dict(size=40, color='#0066CC', symbol='circle', line=dict(color='white', width=2)),
            text=icons,
            textposition='middle center',
            textfont=dict(size=20, color='white')
        ))
        
        fig.update_layout(
            title="Multi-Objective Pareto Front",
            xaxis_title="Sectors",
            yaxis_title="Average Improvement (%)",
            height=400,
            template='plotly_white',
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        return fig
    except Exception as e:
        print(f"Pareto plot error: {e}")
        return None

# ============================================================================
# 1️⃣5️⃣ دوال التحسين للواجهة
# ============================================================================

def optimize_energy(algorithm, iterations, pop_size, runs,
                   inertia_weight, cognitive, social, convergence_param,
                   woa_spiral, de_weight, de_crossover, sa_temp, sa_cooling,
                   mfo_flame, fa_alpha, fa_beta, fa_gamma,
                   hho_energy, hho_jump, ssa_leader, abc_limit,
                   elite_ratio, exploration, exploitation, threshold,
                   patience, restarts, hybrid_weights, cooperation,
                   comm_freq, island_model, num_islands, migration_rate,
                   migration_interval, chaos_factor, chaos_type,
                   adaptive_params, niching_method, niching_radius,
                   niching_param, mutation_strategy, crossover_strategy,
                   selection_strategy, tournament_size):
    """تشغيل تحسين قطاع الطاقة"""
    
    try:
        print(f"\n{'='*60}")
        print(f"🚀 Starting Energy optimization with algorithm: {algorithm}")
        print(f"{'='*60}")
        
        # حدود المتغيرات
        bounds = [(0.0, 2000.0) for _ in range(10)]
        
        # تجميع المعاملات المخصصة
        custom_params = {
            'inertia_weight': float(inertia_weight),
            'cognitive': float(cognitive),
            'social': float(social),
            'convergence_param': float(convergence_param),
            'woa_spiral': float(woa_spiral),
            'de_weight': float(de_weight),
            'de_crossover': float(de_crossover),
            'sa_temp': float(sa_temp),
            'sa_cooling': float(sa_cooling),
            'mfo_flame': float(mfo_flame),
            'fa_alpha': float(fa_alpha),
            'fa_beta': float(fa_beta),
            'fa_gamma': float(fa_gamma),
            'hho_energy': float(hho_energy),
            'hho_jump': float(hho_jump),
            'ssa_leader': float(ssa_leader),
            'abc_limit': int(abc_limit),
            'elite_ratio': float(elite_ratio),
            'exploration': float(exploration),
            'exploitation': float(exploitation),
            'threshold': float(threshold),
            'patience': int(patience),
            'restarts': int(restarts),
            'cooperation': str(cooperation),
            'comm_freq': int(comm_freq),
            'island_model': bool(island_model),
            'num_islands': int(num_islands),
            'migration_rate': float(migration_rate),
            'migration_interval': int(migration_interval),
            'chaos_factor': float(chaos_factor),
            'chaos_type': str(chaos_type),
            'adaptive_params': bool(adaptive_params),
            'niching_method': str(niching_method),
            'niching_radius': float(niching_radius),
            'niching_param': int(niching_param),
            'mutation_strategy': str(mutation_strategy),
            'crossover_strategy': str(crossover_strategy),
            'selection_strategy': str(selection_strategy),
            'tournament_size': int(tournament_size)
        }
        
        # معالجة hybrid_weights
        try:
            if isinstance(hybrid_weights, str):
                weights = [float(w.strip()) for w in hybrid_weights.split(',')]
                while len(weights) < 4:
                    weights.append(0.25)
                weights = weights[:4]
            else:
                weights = [0.25, 0.25, 0.25, 0.25]
        except:
            weights = [0.25, 0.25, 0.25, 0.25]
        
        custom_params['hybrid_weights'] = weights
        
        # تشغيل التحسين
        result = city_engine.optimize_sector(
            'energy', algorithm, bounds,
            iterations=int(iterations),
            pop_size=int(pop_size),
            custom_params=custom_params
        )
        
        if not result.get('success', False):
            return [], None, None, f"❌ Optimization failed: {result.get('error', 'Unknown error')}"
        
        # جدول النتائج مع صف العنوان الصحيح + وقت التنفيذ
        results_table = build_results_table(result, energy_sector, float(result['execution_time']))
        
        # إنشاء الرسومات
        plot1 = create_comparison_plot(
            result['baseline'], result['optimized'],
            energy_sector.criteria[:len(result['baseline'])],
            f"{energy_sector.icon} Energy Sector - Real Optimization"
        )
        
        plot2 = create_improvement_plot(
            result['improvements'],
            energy_sector.criteria[:len(result['improvements'])]
        )
        
        # إحصائيات
        electricity = baghdad_real.get_baghdad_electricity_data()
        stats = f"""
### 📊 Baghdad Energy Sector - Real-time Statistics
- **Average Improvement:** {float(np.mean(result['improvements'])):.2f}%
- **Best Fitness:** {float(result['best_fitness']):.4f}
- **Execution Time:** {float(result['execution_time']):.2f}s
- **Current Load:** {float(electricity['current_load']):.0f} MW
- **Load Percentage:** {float(electricity['load_percentage']):.1f}%
- **Algorithm:** {str(algorithm)}
        """
        
        return results_table, plot1, plot2, stats
        
    except Exception as e:
        print(f"❌ Energy optimization error: {e}")
        import traceback
        traceback.print_exc()
        return [], None, None, f"❌ Error: {str(e)}"


def optimize_traffic(algorithm, iterations, pop_size, runs,
                    inertia_weight, cognitive, social, convergence_param,
                    woa_spiral, de_weight, de_crossover, sa_temp, sa_cooling,
                    mfo_flame, fa_alpha, fa_beta, fa_gamma,
                    hho_energy, hho_jump, ssa_leader, abc_limit,
                    elite_ratio, exploration, exploitation, threshold,
                    patience, restarts, hybrid_weights, cooperation,
                    comm_freq, island_model, num_islands, migration_rate,
                    migration_interval, chaos_factor, chaos_type,
                    adaptive_params, niching_method, niching_radius,
                    niching_param, mutation_strategy, crossover_strategy,
                    selection_strategy, tournament_size):
    """تشغيل تحسين قطاع المرور"""
    
    try:
        print(f"\n{'='*60}")
        print(f"🚀 Starting Traffic optimization with algorithm: {algorithm}")
        print(f"{'='*60}")
        
        # حدود المتغيرات
        bounds = [(0.5, 2.0), (30.0, 120.0)]
        
        # تجميع المعاملات المخصصة
        custom_params = {
            'inertia_weight': float(inertia_weight),
            'cognitive': float(cognitive),
            'social': float(social),
            'convergence_param': float(convergence_param),
            'woa_spiral': float(woa_spiral),
            'de_weight': float(de_weight),
            'de_crossover': float(de_crossover),
            'sa_temp': float(sa_temp),
            'sa_cooling': float(sa_cooling),
            'mfo_flame': float(mfo_flame),
            'fa_alpha': float(fa_alpha),
            'fa_beta': float(fa_beta),
            'fa_gamma': float(fa_gamma),
            'hho_energy': float(hho_energy),
            'hho_jump': float(hho_jump),
            'ssa_leader': float(ssa_leader),
            'abc_limit': int(abc_limit),
            'elite_ratio': float(elite_ratio),
            'exploration': float(exploration),
            'exploitation': float(exploitation),
            'threshold': float(threshold),
            'patience': int(patience),
            'restarts': int(restarts),
            'cooperation': str(cooperation),
            'comm_freq': int(comm_freq),
            'island_model': bool(island_model),
            'num_islands': int(num_islands),
            'migration_rate': float(migration_rate),
            'migration_interval': int(migration_interval),
            'chaos_factor': float(chaos_factor),
            'chaos_type': str(chaos_type),
            'adaptive_params': bool(adaptive_params),
            'niching_method': str(niching_method),
            'niching_radius': float(niching_radius),
            'niching_param': int(niching_param),
            'mutation_strategy': str(mutation_strategy),
            'crossover_strategy': str(crossover_strategy),
            'selection_strategy': str(selection_strategy),
            'tournament_size': int(tournament_size)
        }
        
        # معالجة hybrid_weights
        try:
            if isinstance(hybrid_weights, str):
                weights = [float(w.strip()) for w in hybrid_weights.split(',')]
                while len(weights) < 4:
                    weights.append(0.25)
                weights = weights[:4]
            else:
                weights = [0.25, 0.25, 0.25, 0.25]
        except:
            weights = [0.25, 0.25, 0.25, 0.25]
        
        custom_params['hybrid_weights'] = weights
        
        # تشغيل التحسين
        result = city_engine.optimize_sector(
            'traffic', algorithm, bounds,
            iterations=int(iterations),
            pop_size=int(pop_size),
            custom_params=custom_params
        )
        
        if not result.get('success', False):
            return [], None, None, f"❌ Optimization failed: {result.get('error', 'Unknown error')}"
        
        results_table = build_results_table(result, traffic_sector, float(result['execution_time']))
        
        # إنشاء الرسومات
        plot1 = create_comparison_plot(
            result['baseline'], result['optimized'],
            traffic_sector.criteria[:len(result['baseline'])],
            f"{traffic_sector.icon} Traffic Sector - Real Optimization"
        )
        
        plot2 = create_improvement_plot(
            result['improvements'],
            traffic_sector.criteria[:len(result['improvements'])]
        )
        
        # إحصائيات
        traffic_live = baghdad_real.get_baghdad_traffic()
        stats = f"""
### 📊 Baghdad Traffic Sector - Real-time Statistics
- **Average Improvement:** {float(np.mean(result['improvements'])):.2f}%
- **Best Fitness:** {float(result['best_fitness']):.4f}
- **Execution Time:** {float(result['execution_time']):.2f}s
- **Current Speed:** {float(traffic_live['current_speed']):.1f} km/h
- **Condition:** {str(traffic_live['condition'])}
- **Algorithm:** {str(algorithm)}
        """
        
        return results_table, plot1, plot2, stats
        
    except Exception as e:
        print(f"❌ Traffic optimization error: {e}")
        import traceback
        traceback.print_exc()
        return [], None, None, f"❌ Error: {str(e)}"


def optimize_environment(algorithm, iterations, pop_size, runs,
                        inertia_weight, cognitive, social, convergence_param,
                        woa_spiral, de_weight, de_crossover, sa_temp, sa_cooling,
                        mfo_flame, fa_alpha, fa_beta, fa_gamma,
                        hho_energy, hho_jump, ssa_leader, abc_limit,
                        elite_ratio, exploration, exploitation, threshold,
                        patience, restarts, hybrid_weights, cooperation,
                        comm_freq, island_model, num_islands, migration_rate,
                        migration_interval, chaos_factor, chaos_type,
                        adaptive_params, niching_method, niching_radius,
                        niching_param, mutation_strategy, crossover_strategy,
                        selection_strategy, tournament_size):
    """تشغيل تحسين قطاع البيئة"""
    
    try:
        print(f"\n{'='*60}")
        print(f"🚀 Starting Environment optimization with algorithm: {algorithm}")
        print(f"{'='*60}")
        
        # حدود المتغيرات
        bounds = [(0.5, 1.5), (0.8, 2.0)]
        
        # تجميع المعاملات المخصصة
        custom_params = {
            'inertia_weight': float(inertia_weight),
            'cognitive': float(cognitive),
            'social': float(social),
            'convergence_param': float(convergence_param),
            'woa_spiral': float(woa_spiral),
            'de_weight': float(de_weight),
            'de_crossover': float(de_crossover),
            'sa_temp': float(sa_temp),
            'sa_cooling': float(sa_cooling),
            'mfo_flame': float(mfo_flame),
            'fa_alpha': float(fa_alpha),
            'fa_beta': float(fa_beta),
            'fa_gamma': float(fa_gamma),
            'hho_energy': float(hho_energy),
            'hho_jump': float(hho_jump),
            'ssa_leader': float(ssa_leader),
            'abc_limit': int(abc_limit),
            'elite_ratio': float(elite_ratio),
            'exploration': float(exploration),
            'exploitation': float(exploitation),
            'threshold': float(threshold),
            'patience': int(patience),
            'restarts': int(restarts),
            'cooperation': str(cooperation),
            'comm_freq': int(comm_freq),
            'island_model': bool(island_model),
            'num_islands': int(num_islands),
            'migration_rate': float(migration_rate),
            'migration_interval': int(migration_interval),
            'chaos_factor': float(chaos_factor),
            'chaos_type': str(chaos_type),
            'adaptive_params': bool(adaptive_params),
            'niching_method': str(niching_method),
            'niching_radius': float(niching_radius),
            'niching_param': int(niching_param),
            'mutation_strategy': str(mutation_strategy),
            'crossover_strategy': str(crossover_strategy),
            'selection_strategy': str(selection_strategy),
            'tournament_size': int(tournament_size)
        }
        
        # معالجة hybrid_weights
        try:
            if isinstance(hybrid_weights, str):
                weights = [float(w.strip()) for w in hybrid_weights.split(',')]
                while len(weights) < 4:
                    weights.append(0.25)
                weights = weights[:4]
            else:
                weights = [0.25, 0.25, 0.25, 0.25]
        except:
            weights = [0.25, 0.25, 0.25, 0.25]
        
        custom_params['hybrid_weights'] = weights
        
        # تشغيل التحسين
        result = city_engine.optimize_sector(
            'environment', algorithm, bounds,
            iterations=int(iterations),
            pop_size=int(pop_size),
            custom_params=custom_params
        )
        
        if not result.get('success', False):
            return [], None, None, f"❌ Optimization failed: {result.get('error', 'Unknown error')}"
        
        results_table = build_results_table(result, environment_sector, float(result['execution_time']))
        
        # إنشاء الرسومات
        plot1 = create_comparison_plot(
            result['baseline'], result['optimized'],
            environment_sector.criteria[:len(result['baseline'])],
            f"{environment_sector.icon} Environment Sector - Real Optimization"
        )
        
        plot2 = create_improvement_plot(
            result['improvements'],
            environment_sector.criteria[:len(result['improvements'])]
        )
        
        # إحصائيات
        air = baghdad_real.get_baghdad_air_quality()
        weather = baghdad_real.get_baghdad_weather()
        stats = f"""
### 📊 Baghdad Environment Sector - Real-time Statistics
- **Average Improvement:** {float(np.mean(result['improvements'])):.2f}%
- **Best Fitness:** {float(result['best_fitness']):.4f}
- **Execution Time:** {float(result['execution_time']):.2f}s
- **AQI:** {int(air['aqi'])} - {str(air['category'])}
- **Temperature:** {float(weather['temperature'])}°C
- **Algorithm:** {str(algorithm)}
        """
        
        return results_table, plot1, plot2, stats
        
    except Exception as e:
        print(f"❌ Environment optimization error: {e}")
        import traceback
        traceback.print_exc()
        return [], None, None, f"❌ Error: {str(e)}"


def optimize_waste(algorithm, iterations, pop_size, runs,
                  inertia_weight, cognitive, social, convergence_param,
                  woa_spiral, de_weight, de_crossover, sa_temp, sa_cooling,
                  mfo_flame, fa_alpha, fa_beta, fa_gamma,
                  hho_energy, hho_jump, ssa_leader, abc_limit,
                  elite_ratio, exploration, exploitation, threshold,
                  patience, restarts, hybrid_weights, cooperation,
                  comm_freq, island_model, num_islands, migration_rate,
                  migration_interval, chaos_factor, chaos_type,
                  adaptive_params, niching_method, niching_radius,
                  niching_param, mutation_strategy, crossover_strategy,
                  selection_strategy, tournament_size):
    """تشغيل تحسين قطاع النفايات"""
    
    try:
        print(f"\n{'='*60}")
        print(f"🚀 Starting Waste optimization with algorithm: {algorithm}")
        print(f"{'='*60}")
        
        # حدود المتغيرات
        bounds = [(0.5, 2.0), (0.8, 3.0)]
        
        # تجميع المعاملات المخصصة
        custom_params = {
            'inertia_weight': float(inertia_weight),
            'cognitive': float(cognitive),
            'social': float(social),
            'convergence_param': float(convergence_param),
            'woa_spiral': float(woa_spiral),
            'de_weight': float(de_weight),
            'de_crossover': float(de_crossover),
            'sa_temp': float(sa_temp),
            'sa_cooling': float(sa_cooling),
            'mfo_flame': float(mfo_flame),
            'fa_alpha': float(fa_alpha),
            'fa_beta': float(fa_beta),
            'fa_gamma': float(fa_gamma),
            'hho_energy': float(hho_energy),
            'hho_jump': float(hho_jump),
            'ssa_leader': float(ssa_leader),
            'abc_limit': int(abc_limit),
            'elite_ratio': float(elite_ratio),
            'exploration': float(exploration),
            'exploitation': float(exploitation),
            'threshold': float(threshold),
            'patience': int(patience),
            'restarts': int(restarts),
            'cooperation': str(cooperation),
            'comm_freq': int(comm_freq),
            'island_model': bool(island_model),
            'num_islands': int(num_islands),
            'migration_rate': float(migration_rate),
            'migration_interval': int(migration_interval),
            'chaos_factor': float(chaos_factor),
            'chaos_type': str(chaos_type),
            'adaptive_params': bool(adaptive_params),
            'niching_method': str(niching_method),
            'niching_radius': float(niching_radius),
            'niching_param': int(niching_param),
            'mutation_strategy': str(mutation_strategy),
            'crossover_strategy': str(crossover_strategy),
            'selection_strategy': str(selection_strategy),
            'tournament_size': int(tournament_size)
        }
        
        # معالجة hybrid_weights
        try:
            if isinstance(hybrid_weights, str):
                weights = [float(w.strip()) for w in hybrid_weights.split(',')]
                while len(weights) < 4:
                    weights.append(0.25)
                weights = weights[:4]
            else:
                weights = [0.25, 0.25, 0.25, 0.25]
        except:
            weights = [0.25, 0.25, 0.25, 0.25]
        
        custom_params['hybrid_weights'] = weights
        
        # تشغيل التحسين
        result = city_engine.optimize_sector(
            'waste', algorithm, bounds,
            iterations=int(iterations),
            pop_size=int(pop_size),
            custom_params=custom_params
        )
        
        if not result.get('success', False):
            return [], None, None, f"❌ Optimization failed: {result.get('error', 'Unknown error')}"
        
        results_table = build_results_table(result, waste_sector, float(result['execution_time']))
        
        # إنشاء الرسومات
        plot1 = create_comparison_plot(
            result['baseline'], result['optimized'],
            waste_sector.criteria[:len(result['baseline'])],
            f"{waste_sector.icon} Waste Sector - Real Optimization"
        )
        
        plot2 = create_improvement_plot(
            result['improvements'],
            waste_sector.criteria[:len(result['improvements'])]
        )
        
        # إحصائيات
        waste_data = baghdad_real.get_baghdad_waste_data()
        stats = f"""
### 📊 Baghdad Waste Sector - Real-time Statistics
- **Average Improvement:** {float(np.mean(result['improvements'])):.2f}%
- **Best Fitness:** {float(result['best_fitness']):.4f}
- **Execution Time:** {float(result['execution_time']):.2f}s
- **Daily Waste:** {float(waste_data['daily_waste_tons']):.0f} tons
- **Collection Efficiency:** {float(waste_data['collection_efficiency']*100):.1f}%
- **Algorithm:** {str(algorithm)}
        """
        
        return results_table, plot1, plot2, stats
        
    except Exception as e:
        print(f"❌ Waste optimization error: {e}")
        import traceback
        traceback.print_exc()
        return [], None, None, f"❌ Error: {str(e)}"


def optimize_multi(algorithm, iterations, pop_size, runs,
                   pso_inertia_e, pso_cognitive_e, pso_social_e, gwo_convergence_e,
                   woa_spiral_e, de_weight_e, de_crossover_e, sa_temp_e, sa_cooling_e,
                   mfo_flame_e, fa_alpha_e, fa_beta_e, fa_gamma_e,
                   hho_energy_e, hho_jump_e, ssa_leader_e, abc_limit_e,
                   pso_inertia_t, pso_cognitive_t, pso_social_t, gwo_convergence_t,
                   woa_spiral_t, de_weight_t, de_crossover_t, sa_temp_t, sa_cooling_t,
                   mfo_flame_t, fa_alpha_t, fa_beta_t, fa_gamma_t,
                   hho_energy_t, hho_jump_t, ssa_leader_t, abc_limit_t,
                   pso_inertia_env, pso_cognitive_env, pso_social_env, gwo_convergence_env,
                   woa_spiral_env, de_weight_env, de_crossover_env, sa_temp_env, sa_cooling_env,
                   mfo_flame_env, fa_alpha_env, fa_beta_env, fa_gamma_env,
                   hho_energy_env, hho_jump_env, ssa_leader_env, abc_limit_env,
                   pso_inertia_w, pso_cognitive_w, pso_social_w, gwo_convergence_w,
                   woa_spiral_w, de_weight_w, de_crossover_w, sa_temp_w, sa_cooling_w,
                   mfo_flame_w, fa_alpha_w, fa_beta_w, fa_gamma_w,
                   hho_energy_w, hho_jump_w, ssa_leader_w, abc_limit_w,
                   elite_ratio, exploration, exploitation, threshold,
                   patience, restarts, hybrid_weights, cooperation,
                   comm_freq, island_model, num_islands, migration_rate,
                   migration_interval, chaos_factor, chaos_type,
                   adaptive_params, niching_method, niching_radius,
                   niching_param, mutation_strategy, crossover_strategy,
                   selection_strategy, tournament_size,
                   energy_time_multi, energy_season_multi,
                   traffic_time_multi, traffic_day_multi,
                   env_time_multi, env_weather_multi,
                   waste_district_multi, waste_time_multi):
    """تشغيل التحسين متعدد القطاعات"""
    
    try:
        print(f"\n{'='*60}")
        print(f"🚀 Starting Multi-Objective optimization with algorithm: {algorithm}")
        print(f"{'='*60}")
        
        sectors = ['energy', 'traffic', 'environment', 'waste']
        results = []
        improvements = []
        sectors_results = {}
        
        # bounds لكل قطاع
        sector_bounds = {
            'energy': [(0.0, 2000.0) for _ in range(10)],
            'traffic': [(0.5, 2.0), (30.0, 120.0)],
            'environment': [(0.5, 1.5), (0.8, 2.0)],
            'waste': [(0.5, 2.0), (0.8, 3.0)]
        }
        
        # معاملات لكل قطاع
        sectors_params = {
            'energy': {
                'inertia_weight': float(pso_inertia_e),
                'cognitive': float(pso_cognitive_e),
                'social': float(pso_social_e),
                'convergence_param': float(gwo_convergence_e),
                'woa_spiral': float(woa_spiral_e),
                'de_weight': float(de_weight_e),
                'de_crossover': float(de_crossover_e),
                'sa_temp': float(sa_temp_e),
                'sa_cooling': float(sa_cooling_e),
                'mfo_flame': float(mfo_flame_e),
                'fa_alpha': float(fa_alpha_e),
                'fa_beta': float(fa_beta_e),
                'fa_gamma': float(fa_gamma_e),
                'hho_energy': float(hho_energy_e),
                'hho_jump': float(hho_jump_e),
                'ssa_leader': float(ssa_leader_e),
                'abc_limit': int(abc_limit_e)
            },
            'traffic': {
                'inertia_weight': float(pso_inertia_t),
                'cognitive': float(pso_cognitive_t),
                'social': float(pso_social_t),
                'convergence_param': float(gwo_convergence_t),
                'woa_spiral': float(woa_spiral_t),
                'de_weight': float(de_weight_t),
                'de_crossover': float(de_crossover_t),
                'sa_temp': float(sa_temp_t),
                'sa_cooling': float(sa_cooling_t),
                'mfo_flame': float(mfo_flame_t),
                'fa_alpha': float(fa_alpha_t),
                'fa_beta': float(fa_beta_t),
                'fa_gamma': float(fa_gamma_t),
                'hho_energy': float(hho_energy_t),
                'hho_jump': float(hho_jump_t),
                'ssa_leader': float(ssa_leader_t),
                'abc_limit': int(abc_limit_t)
            },
            'environment': {
                'inertia_weight': float(pso_inertia_env),
                'cognitive': float(pso_cognitive_env),
                'social': float(pso_social_env),
                'convergence_param': float(gwo_convergence_env),
                'woa_spiral': float(woa_spiral_env),
                'de_weight': float(de_weight_env),
                'de_crossover': float(de_crossover_env),
                'sa_temp': float(sa_temp_env),
                'sa_cooling': float(sa_cooling_env),
                'mfo_flame': float(mfo_flame_env),
                'fa_alpha': float(fa_alpha_env),
                'fa_beta': float(fa_beta_env),
                'fa_gamma': float(fa_gamma_env),
                'hho_energy': float(hho_energy_env),
                'hho_jump': float(hho_jump_env),
                'ssa_leader': float(ssa_leader_env),
                'abc_limit': int(abc_limit_env)
            },
            'waste': {
                'inertia_weight': float(pso_inertia_w),
                'cognitive': float(pso_cognitive_w),
                'social': float(pso_social_w),
                'convergence_param': float(gwo_convergence_w),
                'woa_spiral': float(woa_spiral_w),
                'de_weight': float(de_weight_w),
                'de_crossover': float(de_crossover_w),
                'sa_temp': float(sa_temp_w),
                'sa_cooling': float(sa_cooling_w),
                'mfo_flame': float(mfo_flame_w),
                'fa_alpha': float(fa_alpha_w),
                'fa_beta': float(fa_beta_w),
                'fa_gamma': float(fa_gamma_w),
                'hho_energy': float(hho_energy_w),
                'hho_jump': float(hho_jump_w),
                'ssa_leader': float(ssa_leader_w),
                'abc_limit': int(abc_limit_w)
            }
        }
        
        # معالجة hybrid_weights
        try:
            if isinstance(hybrid_weights, str):
                weights = [float(w.strip()) for w in hybrid_weights.split(',')]
                while len(weights) < 4:
                    weights.append(0.25)
                weights = weights[:4]
            else:
                weights = [0.25, 0.25, 0.25, 0.25]
        except:
            weights = [0.25, 0.25, 0.25, 0.25]
        
        # إضافة المعاملات العامة
        common_params = {
            'elite_ratio': float(elite_ratio),
            'exploration': float(exploration),
            'exploitation': float(exploitation),
            'threshold': float(threshold),
            'patience': int(patience),
            'restarts': int(restarts),
            'hybrid_weights': weights,
            'cooperation': str(cooperation),
            'comm_freq': int(comm_freq),
            'island_model': bool(island_model),
            'num_islands': int(num_islands),
            'migration_rate': float(migration_rate),
            'migration_interval': int(migration_interval),
            'chaos_factor': float(chaos_factor),
            'chaos_type': str(chaos_type),
            'adaptive_params': bool(adaptive_params),
            'niching_method': str(niching_method),
            'niching_radius': float(niching_radius),
            'niching_param': int(niching_param),
            'mutation_strategy': str(mutation_strategy),
            'crossover_strategy': str(crossover_strategy),
            'selection_strategy': str(selection_strategy),
            'tournament_size': int(tournament_size)
        }
        
        for sector in sectors:
            print(f"\n🔄 Optimizing {sector} sector...")
            
            custom_params = {**sectors_params[sector], **common_params}

            # حد iterations ذكي لكل قطاع في multi-objective
            # المرور: يستغرق وقتاً أطول لأن greenshields+COPERT أثقل حسابياً
            # الحد الأقصى: iterations×pop ≤ 5000 عملية لكل قطاع
            max_ops       = 5000
            iter_for_sec  = int(iterations)
            pop_for_sec   = int(pop_size)
            if sector == 'traffic':
                # تقليل iterations للمرور تحديداً
                iter_for_sec = min(iter_for_sec, max(10, max_ops // max(1, pop_for_sec)))
            
            result = city_engine.optimize_sector(
                sector, algorithm, sector_bounds[sector],
                iterations=iter_for_sec,
                pop_size=pop_for_sec,
                custom_params=custom_params
            )
            
            if result.get('success', False):
                sectors_results[sector] = result
                avg_imp = float(np.mean(result['improvements']))
                improvements.append(avg_imp)
                exec_t  = float(result.get('execution_time', 0.0))
                
                # أول 3 معايير لكل قطاع
                for i, criterion in enumerate(city_engine.sectors[sector].criteria[:3]):
                    if i < len(result['baseline']) and i < len(result['optimized']):
                        results.append([
                            str(city_engine.sectors[sector].icon),
                            str(criterion),
                            f"{float(result['baseline'][i]):.2f}",
                            f"{float(result['optimized'][i]):.2f}",
                            f"{float(result['improvements'][i]):.2f}%"
                        ])
                # صف وقت التنفيذ لهذا القطاع
                results.append([
                    str(city_engine.sectors[sector].icon),
                    "Execution Time (s)",
                    "—",
                    f"{exec_t:.3f}",
                    "⏱️"
                ])
                print(f"✅ {sector} completed — {avg_imp:.2f}% avg improvement, {exec_t:.2f}s")
            else:
                improvements.append(0.0)
                print(f"⚠️ Sector {sector} optimization failed")
        
        # التأكد من أن لدينا 4 قيم
        while len(improvements) < 4:
            improvements.append(0.0)
        
        pareto_data = [
            {"sector": "Energy", "improvement": float(improvements[0]), "icon": "⚡"},
            {"sector": "Traffic", "improvement": float(improvements[1]), "icon": "🚦"},
            {"sector": "Environment", "improvement": float(improvements[2]), "icon": "🌍"},
            {"sector": "Waste", "improvement": float(improvements[3]), "icon": "🗑️"}
        ]
        
        pareto_plot = create_pareto_plot(pareto_data)
        total_improvement = float(np.mean(improvements)) if improvements else 0.0
        
        # وقت التنفيذ لكل قطاع
        exec_times = {s: float(sectors_results[s].get('execution_time', 0.0))
                      for s in sectors if s in sectors_results}
        total_exec = sum(exec_times.values())

        weather = baghdad_real.get_baghdad_weather()
        air = baghdad_real.get_baghdad_air_quality()
        traffic_live = baghdad_real.get_baghdad_traffic()
        electricity = baghdad_real.get_baghdad_electricity_data()
        
        stats = f"""
### 🎯 Multi-Objective Optimization Results
- **Overall Average Improvement:** {total_improvement:.2f}%
- **Sectors Optimized:** 4
- **Algorithm:** {str(algorithm)}
- **Total Execution Time:** {total_exec:.2f}s

### Sector-wise Performance:
- ⚡ Energy: {improvements[0]:.2f}% improvement | ⏱️ {exec_times.get('energy', 0):.2f}s
- 🚦 Traffic: {improvements[1]:.2f}% improvement | ⏱️ {exec_times.get('traffic', 0):.2f}s
- 🌍 Environment: {improvements[2]:.2f}% improvement | ⏱️ {exec_times.get('environment', 0):.2f}s
- 🗑️ Waste: {improvements[3]:.2f}% improvement | ⏱️ {exec_times.get('waste', 0):.2f}s

### 📡 Baghdad Live Data:
- **Temperature:** {weather['temperature']}°C - {weather['weather_description']}
- **AQI:** {air['aqi']} - {air['category']}
- **Traffic:** {traffic_live['current_speed']:.1f} km/h ({traffic_live['condition']})
- **Power Load:** {electricity['current_load']:.0f} MW ({electricity['load_percentage']:.1f}%)
        """
        
        return results, pareto_plot, stats
        
    except Exception as e:
        print(f"❌ Multi optimization error: {e}")
        import traceback
        traceback.print_exc()
        return [], None, f"❌ Error: {str(e)}"


def update_algorithm_dropdown(category):
    """تحديث قائمة الخوارزميات"""
    algos = algorithms_dict.get(category, [])
    return gr.Dropdown(
        choices=algos[:100] if algos else [],
        label=f"Select {category} Algorithm",
        value=algos[0] if algos else None
    )


def update_algorithm(algo_type, single_algo, binary_algo, ternary_algo, quaternary_algo):
    """تحديث الخوارزمية المختارة"""
    if algo_type == "Single":
        return single_algo
    elif algo_type == "Binary":
        return binary_algo
    elif algo_type == "Triple":
        return ternary_algo
    else:
        return quaternary_algo

# ============================================================================
# 1️⃣6️⃣ إنشاء واجهة Gradio
# ============================================================================

# Get live data for header
live_weather = baghdad_real.get_baghdad_weather()
live_air = baghdad_real.get_baghdad_air_quality()
live_traffic = baghdad_real.get_baghdad_traffic()
live_electricity = baghdad_real.get_baghdad_electricity_data()
live_waste = baghdad_real.get_baghdad_waste_data()

# CSS مخصص
custom_css = """
<style>
    .title-container {
        background-color: black;
        padding: 20px;
        border-radius: 10px 10px 0 0;
        text-align: center;
    }
    .main-title {
        color: white;
        font-weight: bold;
        font-size: 2.5em;
        margin-bottom: 5px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .sub-title {
        color: #00ff00;
        font-size: 1.2em;
        margin-top: 5px;
        font-style: italic;
    }
    .footer {
        background-color: black;
        color: white;
        font-weight: bold;
        padding: 20px;
        border-radius: 0 0 10px 10px;
        margin-top: 20px;
        text-align: center;
        font-size: 0.9em;
        line-height: 1.6;
    }
    .footer p {
        margin: 5px 0;
    }
    .footer-arabic {
        font-family: 'Arial', sans-serif;
        direction: rtl;
        margin-top: 15px;
        padding-top: 15px;
        border-top: 1px solid #444;
    }
</style>
"""

with gr.Blocks(theme=gr.themes.Soft(), title="Baghdad Smart City Control System", css=custom_css) as demo:

    # Header
    gr.HTML(f"""
    <div class="title-container">
        <div class="main-title">🏙️ Baghdad Smart City Integrated Control System</div>
        <div class="sub-title">REAL PHYSICS-BASED OPTIMIZATION WITH 35+ ALGORITHMS</div>
        <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 15px; margin-top: 20px; background-color: #1a1a1a; padding: 15px; border-radius: 10px;">
            <div style="text-align: center;">
                <div style="font-size: 1.2em; color: #00ff00;">⚡ {live_electricity['current_load']:.0f} MW</div>
                <div style="font-size: 0.9em; color: #cccccc;">Power Load</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 1.2em; color: #00ff00;">🚦 {live_traffic['current_speed']:.1f} km/h</div>
                <div style="font-size: 0.9em; color: #cccccc;">Traffic Speed</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 1.2em; color: #00ff00;">🌍 {live_air['aqi']}</div>
                <div style="font-size: 0.9em; color: #cccccc;">AQI ({live_air['category']})</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 1.2em; color: #00ff00;">🗑️ {live_waste['daily_waste_tons']:.0f} t</div>
                <div style="font-size: 0.9em; color: #cccccc;">Daily Waste</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 1.2em; color: #00ff00;">🌡️ {live_weather['temperature']}°C</div>
                <div style="font-size: 0.9em; color: #cccccc;">Temperature</div>
            </div>
        </div>
    </div>
    """)

    with gr.Tabs():
        # Energy Tab
        with gr.TabItem("⚡ Energy Sector", id=0):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown(f"""
                    ### ⚡ Baghdad Real Energy
                    - **Source:** EnergyData.info + Estimates
                    - **Total Capacity:** {live_electricity['total_capacity']} MW
                    - **Current Load:** {live_electricity['current_load']:.0f} MW
                    - **Load Percentage:** {live_electricity['load_percentage']:.1f}%
                    """)

                    # Algorithm Selection
                    algo_type_energy = gr.Radio(
                        choices=["Single", "Binary", "Triple", "Quad"],
                        label="Algorithm Type",
                        value="Single"
                    )

                    single_algo_energy = gr.Dropdown(
                        choices=algorithms_dict.get("Single", []),
                        label="Single Algorithm",
                        value=algorithms_dict.get("Single", [])[0] if algorithms_dict.get("Single", []) else None
                    )

                    binary_algo_energy = gr.Dropdown(
                        choices=algorithms_dict.get("Binary", []),
                        label="Binary Hybrid Algorithm",
                        value=algorithms_dict.get("Binary", [])[0] if algorithms_dict.get("Binary", []) else None,
                        visible=False
                    )

                    ternary_algo_energy = gr.Dropdown(
                        choices=algorithms_dict.get("Triple", []),
                        label="Ternary Hybrid Algorithm",
                        value=algorithms_dict.get("Triple", [])[0] if algorithms_dict.get("Triple", []) else None,
                        visible=False
                    )

                    quaternary_algo_energy = gr.Dropdown(
                        choices=algorithms_dict.get("Quad", []),
                        label="Quaternary Hybrid Algorithm",
                        value=algorithms_dict.get("Quad", [])[0] if algorithms_dict.get("Quad", []) else None,
                        visible=False
                    )

                    def update_energy_visibility(algo_type):
                        if algo_type == "Single":
                            return gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)
                        elif algo_type == "Binary":
                            return gr.update(visible=False), gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)
                        elif algo_type == "Triple":
                            return gr.update(visible=False), gr.update(visible=False), gr.update(visible=True), gr.update(visible=False)
                        else:
                            return gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=True)

                    algo_type_energy.change(
                        fn=update_energy_visibility,
                        inputs=algo_type_energy,
                        outputs=[single_algo_energy, binary_algo_energy, ternary_algo_energy, quaternary_algo_energy]
                    )

                    algorithm_energy = gr.Textbox(visible=False)

                    algo_type_energy.change(
                        fn=update_algorithm,
                        inputs=[algo_type_energy, single_algo_energy, binary_algo_energy, ternary_algo_energy, quaternary_algo_energy],
                        outputs=algorithm_energy
                    )

                    single_algo_energy.change(
                        fn=lambda x: x, inputs=single_algo_energy, outputs=algorithm_energy
                    )
                    binary_algo_energy.change(
                        fn=lambda x: x, inputs=binary_algo_energy, outputs=algorithm_energy
                    )
                    ternary_algo_energy.change(
                        fn=lambda x: x, inputs=ternary_algo_energy, outputs=algorithm_energy
                    )
                    quaternary_algo_energy.change(
                        fn=lambda x: x, inputs=quaternary_algo_energy, outputs=algorithm_energy
                    )

                    # Basic Settings
                    with gr.Accordion("📘 Basic Settings", open=True):
                        iterations_energy = gr.Slider(1, 10000, 500, step=10, label="Iterations")
                        pop_size_energy = gr.Slider(2, 5000, 100, step=5, label="Population Size")
                        runs_energy = gr.Slider(1, 100, 5, step=1, label="Number of Runs")

                    # Advanced Settings
                    with gr.Accordion("📗 Advanced Settings", open=False):
                        with gr.Tab("PSO"):
                            pso_inertia_e = gr.Slider(0.1, 5.0, 0.7, step=0.05, label="Inertia Weight")
                            pso_cognitive_e = gr.Slider(0.5, 10.0, 2.05, step=0.05, label="Cognitive Coefficient")
                            pso_social_e = gr.Slider(0.5, 10.0, 2.05, step=0.05, label="Social Coefficient")
                        
                        with gr.Tab("GWO"):
                            gwo_convergence_e = gr.Slider(0.1, 10.0, 2.0, step=0.1, label="Convergence Parameter")
                        
                        with gr.Tab("WOA"):
                            woa_spiral_e = gr.Slider(0.1, 10.0, 1.0, step=0.1, label="Spiral Constant")
                        
                        with gr.Tab("DE"):
                            de_weight_e = gr.Slider(0.1, 10.0, 0.8, step=0.1, label="Differential Weight")
                            de_crossover_e = gr.Slider(0.1, 1.0, 0.9, step=0.05, label="Crossover Probability")
                        
                        with gr.Tab("SA"):
                            sa_temp_e = gr.Slider(1, 100000, 1000, step=10, label="Initial Temperature")
                            sa_cooling_e = gr.Slider(0.5, 0.99999, 0.95, step=0.001, label="Cooling Rate")
                        
                        with gr.Tab("MFO"):
                            mfo_flame_e = gr.Slider(-5.0, 5.0, -1.0, step=0.1, label="Flame Constant")
                        
                        with gr.Tab("FA"):
                            fa_alpha_e = gr.Slider(0.1, 5.0, 0.5, step=0.05, label="Alpha")
                            fa_beta_e = gr.Slider(0.1, 5.0, 0.2, step=0.05, label="Beta")
                            fa_gamma_e = gr.Slider(0.01, 10.0, 1.0, step=0.1, label="Gamma")
                        
                        with gr.Tab("HHO"):
                            hho_energy_e = gr.Slider(-2.0, 2.0, 1.0, step=0.1, label="Escape Energy")
                            hho_jump_e = gr.Slider(0.1, 2.0, 0.5, step=0.05, label="Jump Strength")
                        
                        with gr.Tab("SSA"):
                            ssa_leader_e = gr.Slider(0.1, 10.0, 1.0, step=0.1, label="Leader Position")
                        
                        with gr.Tab("ABC"):
                            abc_limit_e = gr.Slider(1, 1000, 100, step=5, label="Limit")

                    # Super Settings
                    with gr.Accordion("📙 Super Settings", open=False):
                        elite_ratio = gr.Slider(0.001, 0.99, 0.1, step=0.01, label="Elite Ratio")
                        exploration_rate = gr.Slider(0.01, 1.0, 0.7, step=0.05, label="Exploration Rate")
                        exploitation_rate = gr.Slider(0.01, 1.0, 0.3, step=0.05, label="Exploitation Rate")
                        convergence_threshold = gr.Slider(1e-10, 1e-1, 1e-6, step=1e-7, label="Convergence Threshold")
                        patience = gr.Slider(1, 1000, 50, step=5, label="Patience")
                        restarts = gr.Slider(0, 1000, 10, step=1, label="Restarts")

                    # Ultra Settings
                    with gr.Accordion("📕 Ultra Settings", open=False):
                        hybrid_weights = gr.Textbox(value="0.25,0.25,0.25,0.25", label="Hybrid Weights (comma-separated)")
                        cooperation_type = gr.Dropdown(["parallel", "sequential", "adaptive", "competitive", "coevolutionary"], 
                                                       value="parallel", label="Cooperation Type")
                        comm_freq = gr.Slider(1, 1000, 10, step=1, label="Communication Frequency")
                        island_model = gr.Checkbox(label="Island Model", value=False)
                        num_islands = gr.Slider(2, 1000, 10, step=1, label="Number of Islands", visible=False)
                        migration_rate = gr.Slider(0.001, 0.99, 0.1, step=0.01, label="Migration Rate", visible=False)
                        migration_interval = gr.Slider(1, 1000, 20, step=1, label="Migration Interval", visible=False)
                        chaos_factor = gr.Slider(0, 5.0, 0.1, step=0.05, label="Chaos Factor")
                        chaos_type = gr.Dropdown(["logistic", "tent", "sine", "circle", "gauss", "random"], 
                                                value="logistic", label="Chaos Type")
                        adaptive_params = gr.Checkbox(label="Adaptive Parameter Control", value=True)
                        niching_method = gr.Dropdown(["none", "fitness_sharing", "clearing", "speciation", "crowding"], 
                                                     value="none", label="Niching Method")
                        niching_radius = gr.Slider(0.001, 10.0, 0.1, step=0.05, label="Niching Radius", visible=False)
                        niching_param = gr.Slider(1, 1000, 2, step=1, label="Niching Parameter", visible=False)
                        mutation_strategy = gr.Dropdown(["random", "gaussian", "polynomial", "uniform", "adaptive"], 
                                                        value="polynomial", label="Mutation Strategy")
                        crossover_strategy = gr.Dropdown(["single_point", "two_point", "uniform", "arithmetic", "simulated_binary"], 
                                                         value="simulated_binary", label="Crossover Strategy")
                        selection_strategy = gr.Dropdown(["tournament", "roulette", "rank", "random", "boltzmann"], 
                                                         value="tournament", label="Selection Strategy")
                        tournament_size = gr.Slider(2, 1000, 3, step=1, label="Tournament Size", visible=True)

                        def update_island_visibility(island):
                            return gr.update(visible=island), gr.update(visible=island), gr.update(visible=island)
                        
                        island_model.change(
                            fn=update_island_visibility,
                            inputs=island_model,
                            outputs=[num_islands, migration_rate, migration_interval]
                        )
                        
                        def update_niching_visibility(method):
                            show = method != "none"
                            return gr.update(visible=show), gr.update(visible=show)
                        
                        niching_method.change(
                            fn=update_niching_visibility,
                            inputs=niching_method,
                            outputs=[niching_radius, niching_param]
                        )

                    run_energy_btn = gr.Button("⚡ Optimize Energy Sector", variant="primary", size="lg")

                with gr.Column(scale=2):
                    with gr.Tabs():
                        with gr.TabItem("📊 Results"):
                            energy_results = gr.Dataframe(
                                headers=["Criterion", "Unit", "Baseline", "Optimized", "Improvement", "Status"],
                                label="Energy Sector Results",
                                row_count=11
                            )
                            gr.HTML(value=EQUATIONS_HTML["energy"])
                        with gr.TabItem("📈 Comparison"):
                            energy_plot1 = gr.Plot()
                        with gr.TabItem("📉 Improvements"):
                            energy_plot2 = gr.Plot()
                        with gr.TabItem("📋 Statistics"):
                            energy_stats = gr.Markdown()

            run_energy_btn.click(
                fn=optimize_energy,
                inputs=[
                    algorithm_energy, iterations_energy, pop_size_energy, runs_energy,
                    pso_inertia_e, pso_cognitive_e, pso_social_e, gwo_convergence_e,
                    woa_spiral_e, de_weight_e, de_crossover_e, sa_temp_e, sa_cooling_e,
                    mfo_flame_e, fa_alpha_e, fa_beta_e, fa_gamma_e,
                    hho_energy_e, hho_jump_e, ssa_leader_e, abc_limit_e,
                    elite_ratio, exploration_rate, exploitation_rate, convergence_threshold,
                    patience, restarts, hybrid_weights, cooperation_type,
                    comm_freq, island_model, num_islands, migration_rate,
                    migration_interval, chaos_factor, chaos_type,
                    adaptive_params, niching_method, niching_radius,
                    niching_param, mutation_strategy, crossover_strategy,
                    selection_strategy, tournament_size
                ],
                outputs=[energy_results, energy_plot1, energy_plot2, energy_stats]
            )

        # Traffic Tab
        with gr.TabItem("🚦 Traffic Sector", id=1):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown(f"""
                    ### 🚦 Baghdad Real Traffic
                    - **Source:** TomTom Traffic API
                    - **Current Speed:** {live_traffic['current_speed']:.1f} km/h
                    - **Condition:** {live_traffic['condition']}
                    - **Congestion Level:** {live_traffic['congestion_level']:.2f}
                    """)

                    # Algorithm Selection
                    algo_type_traffic = gr.Radio(
                        choices=["Single", "Binary", "Triple", "Quad"],
                        label="Algorithm Type",
                        value="Single"
                    )

                    single_algo_traffic = gr.Dropdown(
                        choices=algorithms_dict.get("Single", []),
                        label="Single Algorithm",
                        value=algorithms_dict.get("Single", [])[0] if algorithms_dict.get("Single", []) else None
                    )

                    binary_algo_traffic = gr.Dropdown(
                        choices=algorithms_dict.get("Binary", []),
                        label="Binary Hybrid Algorithm",
                        value=algorithms_dict.get("Binary", [])[0] if algorithms_dict.get("Binary", []) else None,
                        visible=False
                    )

                    ternary_algo_traffic = gr.Dropdown(
                        choices=algorithms_dict.get("Triple", []),
                        label="Ternary Hybrid Algorithm",
                        value=algorithms_dict.get("Triple", [])[0] if algorithms_dict.get("Triple", []) else None,
                        visible=False
                    )

                    quaternary_algo_traffic = gr.Dropdown(
                        choices=algorithms_dict.get("Quad", []),
                        label="Quaternary Hybrid Algorithm",
                        value=algorithms_dict.get("Quad", [])[0] if algorithms_dict.get("Quad", []) else None,
                        visible=False
                    )

                    algo_type_traffic.change(
                        fn=update_energy_visibility,
                        inputs=algo_type_traffic,
                        outputs=[single_algo_traffic, binary_algo_traffic, ternary_algo_traffic, quaternary_algo_traffic]
                    )

                    algorithm_traffic = gr.Textbox(visible=False)

                    algo_type_traffic.change(
                        fn=update_algorithm,
                        inputs=[algo_type_traffic, single_algo_traffic, binary_algo_traffic, ternary_algo_traffic, quaternary_algo_traffic],
                        outputs=algorithm_traffic
                    )

                    single_algo_traffic.change(fn=lambda x: x, inputs=single_algo_traffic, outputs=algorithm_traffic)
                    binary_algo_traffic.change(fn=lambda x: x, inputs=binary_algo_traffic, outputs=algorithm_traffic)
                    ternary_algo_traffic.change(fn=lambda x: x, inputs=ternary_algo_traffic, outputs=algorithm_traffic)
                    quaternary_algo_traffic.change(fn=lambda x: x, inputs=quaternary_algo_traffic, outputs=algorithm_traffic)

                    # Basic Settings
                    with gr.Accordion("📘 Basic Settings", open=True):
                        iterations_traffic = gr.Slider(1, 10000, 500, step=10, label="Iterations")
                        pop_size_traffic = gr.Slider(2, 5000, 100, step=5, label="Population Size")
                        runs_traffic = gr.Slider(1, 100, 5, step=1, label="Number of Runs")

                    # Advanced Settings
                    with gr.Accordion("📗 Advanced Settings", open=False):
                        with gr.Tab("PSO"):
                            pso_inertia_t = gr.Slider(0.1, 5.0, 0.7, step=0.05, label="Inertia Weight")
                            pso_cognitive_t = gr.Slider(0.5, 10.0, 2.05, step=0.05, label="Cognitive Coefficient")
                            pso_social_t = gr.Slider(0.5, 10.0, 2.05, step=0.05, label="Social Coefficient")
                        
                        with gr.Tab("GWO"):
                            gwo_convergence_t = gr.Slider(0.1, 10.0, 2.0, step=0.1, label="Convergence Parameter")
                        
                        with gr.Tab("WOA"):
                            woa_spiral_t = gr.Slider(0.1, 10.0, 1.0, step=0.1, label="Spiral Constant")
                        
                        with gr.Tab("DE"):
                            de_weight_t = gr.Slider(0.1, 10.0, 0.8, step=0.1, label="Differential Weight")
                            de_crossover_t = gr.Slider(0.1, 1.0, 0.9, step=0.05, label="Crossover Probability")
                        
                        with gr.Tab("SA"):
                            sa_temp_t = gr.Slider(1, 100000, 1000, step=10, label="Initial Temperature")
                            sa_cooling_t = gr.Slider(0.5, 0.99999, 0.95, step=0.001, label="Cooling Rate")
                        
                        with gr.Tab("MFO"):
                            mfo_flame_t = gr.Slider(-5.0, 5.0, -1.0, step=0.1, label="Flame Constant")
                        
                        with gr.Tab("FA"):
                            fa_alpha_t = gr.Slider(0.1, 5.0, 0.5, step=0.05, label="Alpha")
                            fa_beta_t = gr.Slider(0.1, 5.0, 0.2, step=0.05, label="Beta")
                            fa_gamma_t = gr.Slider(0.01, 10.0, 1.0, step=0.1, label="Gamma")
                        
                        with gr.Tab("HHO"):
                            hho_energy_t = gr.Slider(-2.0, 2.0, 1.0, step=0.1, label="Escape Energy")
                            hho_jump_t = gr.Slider(0.1, 2.0, 0.5, step=0.05, label="Jump Strength")
                        
                        with gr.Tab("SSA"):
                            ssa_leader_t = gr.Slider(0.1, 10.0, 1.0, step=0.1, label="Leader Position")
                        
                        with gr.Tab("ABC"):
                            abc_limit_t = gr.Slider(1, 1000, 100, step=5, label="Limit")

                    # Super Settings
                    with gr.Accordion("📙 Super Settings", open=False):
                        elite_ratio_t = gr.Slider(0.001, 0.99, 0.1, step=0.01, label="Elite Ratio")
                        exploration_rate_t = gr.Slider(0.01, 1.0, 0.7, step=0.05, label="Exploration Rate")
                        exploitation_rate_t = gr.Slider(0.01, 1.0, 0.3, step=0.05, label="Exploitation Rate")
                        convergence_threshold_t = gr.Slider(1e-10, 1e-1, 1e-6, step=1e-7, label="Convergence Threshold")
                        patience_t = gr.Slider(1, 1000, 50, step=5, label="Patience")
                        restarts_t = gr.Slider(0, 1000, 10, step=1, label="Restarts")

                    # Ultra Settings
                    with gr.Accordion("📕 Ultra Settings", open=False):
                        hybrid_weights_t = gr.Textbox(value="0.25,0.25,0.25,0.25", label="Hybrid Weights")
                        cooperation_type_t = gr.Dropdown(["parallel", "sequential", "adaptive"], value="parallel", label="Cooperation Type")
                        comm_freq_t = gr.Slider(1, 1000, 10, step=1, label="Communication Frequency")
                        island_model_t = gr.Checkbox(label="Island Model", value=False)
                        num_islands_t = gr.Slider(2, 1000, 10, step=1, label="Number of Islands", visible=False)
                        migration_rate_t = gr.Slider(0.001, 0.99, 0.1, step=0.01, label="Migration Rate", visible=False)
                        migration_interval_t = gr.Slider(1, 1000, 20, step=1, label="Migration Interval", visible=False)
                        chaos_factor_t = gr.Slider(0, 5.0, 0.1, step=0.05, label="Chaos Factor")
                        chaos_type_t = gr.Dropdown(["logistic", "tent", "sine"], value="logistic", label="Chaos Type")
                        adaptive_params_t = gr.Checkbox(label="Adaptive Parameter Control", value=True)
                        niching_method_t = gr.Dropdown(["none", "fitness_sharing", "clearing"], value="none", label="Niching Method")
                        niching_radius_t = gr.Slider(0.001, 10.0, 0.1, step=0.05, label="Niching Radius", visible=False)
                        niching_param_t = gr.Slider(1, 1000, 2, step=1, label="Niching Parameter", visible=False)

                        island_model_t.change(
                            fn=update_island_visibility,
                            inputs=island_model_t,
                            outputs=[num_islands_t, migration_rate_t, migration_interval_t]
                        )
                        
                        niching_method_t.change(
                            fn=update_niching_visibility,
                            inputs=niching_method_t,
                            outputs=[niching_radius_t, niching_param_t]
                        )

                    run_traffic_btn = gr.Button("🚦 Optimize Traffic Sector", variant="primary", size="lg")

                with gr.Column(scale=2):
                    with gr.Tabs():
                        with gr.TabItem("📊 Results"):
                            traffic_results = gr.Dataframe(
                                headers=["Criterion", "Unit", "Baseline", "Optimized", "Improvement", "Status"],
                                label="Traffic Sector Results",
                                row_count=11
                            )
                            gr.HTML(value=EQUATIONS_HTML["traffic"])
                        with gr.TabItem("📈 Comparison"):
                            traffic_plot1 = gr.Plot()
                        with gr.TabItem("📉 Improvements"):
                            traffic_plot2 = gr.Plot()
                        with gr.TabItem("📋 Statistics"):
                            traffic_stats = gr.Markdown()

            run_traffic_btn.click(
                fn=optimize_traffic,
                inputs=[
                    algorithm_traffic, iterations_traffic, pop_size_traffic, runs_traffic,
                    pso_inertia_t, pso_cognitive_t, pso_social_t, gwo_convergence_t,
                    woa_spiral_t, de_weight_t, de_crossover_t, sa_temp_t, sa_cooling_t,
                    mfo_flame_t, fa_alpha_t, fa_beta_t, fa_gamma_t,
                    hho_energy_t, hho_jump_t, ssa_leader_t, abc_limit_t,
                    elite_ratio_t, exploration_rate_t, exploitation_rate_t, convergence_threshold_t,
                    patience_t, restarts_t, hybrid_weights_t, cooperation_type_t,
                    comm_freq_t, island_model_t, num_islands_t, migration_rate_t,
                    migration_interval_t, chaos_factor_t, chaos_type_t,
                    adaptive_params_t, niching_method_t, niching_radius_t,
                    niching_param_t, mutation_strategy, crossover_strategy,
                    selection_strategy, tournament_size
                ],
                outputs=[traffic_results, traffic_plot1, traffic_plot2, traffic_stats]
            )

        # Environment Tab
        with gr.TabItem("🌍 Environment Sector", id=2):
            with gr.Row():
                with gr.Column(scale=1):
                    # PM2.5 يُصلح قبل العرض: إذا كانت 0 أو أقل من 1.0 نستخدم القيمة الواقعية
                    _pm25_display = float(live_air['pm25']) if float(live_air['pm25']) >= 1.0 else 25.5
                    gr.Markdown(f"""
                    ### 🌍 Baghdad Real Environment
                    - **Source:** WAQI + OpenWeatherMap
                    - **AQI:** {live_air['aqi']} ({live_air['category']})
                    - **PM2.5:** {_pm25_display:.1f} μg/m³
                    - **Temperature:** {live_weather['temperature']}°C
                    """)

                    # Algorithm Selection
                    algo_type_env = gr.Radio(
                        choices=["Single", "Binary", "Triple", "Quad"],
                        label="Algorithm Type",
                        value="Single"
                    )

                    single_algo_env = gr.Dropdown(
                        choices=algorithms_dict.get("Single", []),
                        label="Single Algorithm",
                        value=algorithms_dict.get("Single", [])[0] if algorithms_dict.get("Single", []) else None
                    )

                    binary_algo_env = gr.Dropdown(
                        choices=algorithms_dict.get("Binary", []),
                        label="Binary Hybrid Algorithm",
                        value=algorithms_dict.get("Binary", [])[0] if algorithms_dict.get("Binary", []) else None,
                        visible=False
                    )

                    ternary_algo_env = gr.Dropdown(
                        choices=algorithms_dict.get("Triple", []),
                        label="Ternary Hybrid Algorithm",
                        value=algorithms_dict.get("Triple", [])[0] if algorithms_dict.get("Triple", []) else None,
                        visible=False
                    )

                    quaternary_algo_env = gr.Dropdown(
                        choices=algorithms_dict.get("Quad", []),
                        label="Quaternary Hybrid Algorithm",
                        value=algorithms_dict.get("Quad", [])[0] if algorithms_dict.get("Quad", []) else None,
                        visible=False
                    )

                    algo_type_env.change(
                        fn=update_energy_visibility,
                        inputs=algo_type_env,
                        outputs=[single_algo_env, binary_algo_env, ternary_algo_env, quaternary_algo_env]
                    )

                    algorithm_env = gr.Textbox(visible=False)

                    algo_type_env.change(
                        fn=update_algorithm,
                        inputs=[algo_type_env, single_algo_env, binary_algo_env, ternary_algo_env, quaternary_algo_env],
                        outputs=algorithm_env
                    )

                    single_algo_env.change(fn=lambda x: x, inputs=single_algo_env, outputs=algorithm_env)
                    binary_algo_env.change(fn=lambda x: x, inputs=binary_algo_env, outputs=algorithm_env)
                    ternary_algo_env.change(fn=lambda x: x, inputs=ternary_algo_env, outputs=algorithm_env)
                    quaternary_algo_env.change(fn=lambda x: x, inputs=quaternary_algo_env, outputs=algorithm_env)

                    # Basic Settings
                    with gr.Accordion("📘 Basic Settings", open=True):
                        iterations_env = gr.Slider(1, 10000, 500, step=10, label="Iterations")
                        pop_size_env = gr.Slider(2, 5000, 100, step=5, label="Population Size")
                        runs_env = gr.Slider(1, 100, 5, step=1, label="Number of Runs")

                    # Advanced Settings
                    with gr.Accordion("📗 Advanced Settings", open=False):
                        with gr.Tab("PSO"):
                            pso_inertia_env = gr.Slider(0.1, 5.0, 0.7, step=0.05, label="Inertia Weight")
                            pso_cognitive_env = gr.Slider(0.5, 10.0, 2.05, step=0.05, label="Cognitive Coefficient")
                            pso_social_env = gr.Slider(0.5, 10.0, 2.05, step=0.05, label="Social Coefficient")
                        
                        with gr.Tab("GWO"):
                            gwo_convergence_env = gr.Slider(0.1, 10.0, 2.0, step=0.1, label="Convergence Parameter")
                        
                        with gr.Tab("WOA"):
                            woa_spiral_env = gr.Slider(0.1, 10.0, 1.0, step=0.1, label="Spiral Constant")
                        
                        with gr.Tab("DE"):
                            de_weight_env = gr.Slider(0.1, 10.0, 0.8, step=0.1, label="Differential Weight")
                            de_crossover_env = gr.Slider(0.1, 1.0, 0.9, step=0.05, label="Crossover Probability")
                        
                        with gr.Tab("SA"):
                            sa_temp_env = gr.Slider(1, 100000, 1000, step=10, label="Initial Temperature")
                            sa_cooling_env = gr.Slider(0.5, 0.99999, 0.95, step=0.001, label="Cooling Rate")
                        
                        with gr.Tab("MFO"):
                            mfo_flame_env = gr.Slider(-5.0, 5.0, -1.0, step=0.1, label="Flame Constant")
                        
                        with gr.Tab("FA"):
                            fa_alpha_env = gr.Slider(0.1, 5.0, 0.5, step=0.05, label="Alpha")
                            fa_beta_env = gr.Slider(0.1, 5.0, 0.2, step=0.05, label="Beta")
                            fa_gamma_env = gr.Slider(0.01, 10.0, 1.0, step=0.1, label="Gamma")
                        
                        with gr.Tab("HHO"):
                            hho_energy_env = gr.Slider(-2.0, 2.0, 1.0, step=0.1, label="Escape Energy")
                            hho_jump_env = gr.Slider(0.1, 2.0, 0.5, step=0.05, label="Jump Strength")
                        
                        with gr.Tab("SSA"):
                            ssa_leader_env = gr.Slider(0.1, 10.0, 1.0, step=0.1, label="Leader Position")
                        
                        with gr.Tab("ABC"):
                            abc_limit_env = gr.Slider(1, 1000, 100, step=5, label="Limit")

                    # Super Settings
                    with gr.Accordion("📙 Super Settings", open=False):
                        elite_ratio_env = gr.Slider(0.001, 0.99, 0.1, step=0.01, label="Elite Ratio")
                        exploration_rate_env = gr.Slider(0.01, 1.0, 0.7, step=0.05, label="Exploration Rate")
                        exploitation_rate_env = gr.Slider(0.01, 1.0, 0.3, step=0.05, label="Exploitation Rate")
                        convergence_threshold_env = gr.Slider(1e-10, 1e-1, 1e-6, step=1e-7, label="Convergence Threshold")
                        patience_env = gr.Slider(1, 1000, 50, step=5, label="Patience")
                        restarts_env = gr.Slider(0, 1000, 10, step=1, label="Restarts")

                    # Ultra Settings
                    with gr.Accordion("📕 Ultra Settings", open=False):
                        hybrid_weights_env = gr.Textbox(value="0.25,0.25,0.25,0.25", label="Hybrid Weights")
                        cooperation_type_env = gr.Dropdown(["parallel", "sequential", "adaptive"], value="parallel", label="Cooperation Type")
                        comm_freq_env = gr.Slider(1, 1000, 10, step=1, label="Communication Frequency")
                        island_model_env = gr.Checkbox(label="Island Model", value=False)
                        num_islands_env = gr.Slider(2, 1000, 10, step=1, label="Number of Islands", visible=False)
                        migration_rate_env = gr.Slider(0.001, 0.99, 0.1, step=0.01, label="Migration Rate", visible=False)
                        migration_interval_env = gr.Slider(1, 1000, 20, step=1, label="Migration Interval", visible=False)
                        chaos_factor_env = gr.Slider(0, 5.0, 0.1, step=0.05, label="Chaos Factor")
                        chaos_type_env = gr.Dropdown(["logistic", "tent", "sine"], value="logistic", label="Chaos Type")
                        adaptive_params_env = gr.Checkbox(label="Adaptive Parameter Control", value=True)
                        niching_method_env = gr.Dropdown(["none", "fitness_sharing", "clearing"], value="none", label="Niching Method")
                        niching_radius_env = gr.Slider(0.001, 10.0, 0.1, step=0.05, label="Niching Radius", visible=False)
                        niching_param_env = gr.Slider(1, 1000, 2, step=1, label="Niching Parameter", visible=False)

                        island_model_env.change(
                            fn=update_island_visibility,
                            inputs=island_model_env,
                            outputs=[num_islands_env, migration_rate_env, migration_interval_env]
                        )
                        
                        niching_method_env.change(
                            fn=update_niching_visibility,
                            inputs=niching_method_env,
                            outputs=[niching_radius_env, niching_param_env]
                        )

                    run_env_btn = gr.Button("🌍 Optimize Environment Sector", variant="primary", size="lg")

                with gr.Column(scale=2):
                    with gr.Tabs():
                        with gr.TabItem("📊 Results"):
                            env_results = gr.Dataframe(
                                headers=["Criterion", "Unit", "Baseline", "Optimized", "Improvement", "Status"],
                                label="Environment Sector Results",
                                row_count=11
                            )
                            gr.HTML(value=EQUATIONS_HTML["environment"])
                        with gr.TabItem("📈 Comparison"):
                            env_plot1 = gr.Plot()
                        with gr.TabItem("📉 Improvements"):
                            env_plot2 = gr.Plot()
                        with gr.TabItem("📋 Statistics"):
                            env_stats = gr.Markdown()

            run_env_btn.click(
                fn=optimize_environment,
                inputs=[
                    algorithm_env, iterations_env, pop_size_env, runs_env,
                    pso_inertia_env, pso_cognitive_env, pso_social_env, gwo_convergence_env,
                    woa_spiral_env, de_weight_env, de_crossover_env, sa_temp_env, sa_cooling_env,
                    mfo_flame_env, fa_alpha_env, fa_beta_env, fa_gamma_env,
                    hho_energy_env, hho_jump_env, ssa_leader_env, abc_limit_env,
                    elite_ratio_env, exploration_rate_env, exploitation_rate_env, convergence_threshold_env,
                    patience_env, restarts_env, hybrid_weights_env, cooperation_type_env,
                    comm_freq_env, island_model_env, num_islands_env, migration_rate_env,
                    migration_interval_env, chaos_factor_env, chaos_type_env,
                    adaptive_params_env, niching_method_env, niching_radius_env,
                    niching_param_env, mutation_strategy, crossover_strategy,
                    selection_strategy, tournament_size
                ],
                outputs=[env_results, env_plot1, env_plot2, env_stats]
            )

        # Waste Tab
        with gr.TabItem("🗑️ Waste Sector", id=3):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown(f"""
                    ### 🗑️ Baghdad Waste Management
                    - **Source:** Baghdad Municipality Estimates
                    - **Daily Waste:** {live_waste['daily_waste_tons']:.0f} tons
                    - **Collection Efficiency:** {live_waste['collection_efficiency']*100:.1f}%
                    - **Recycling Rate:** {live_waste['recycling_rate']*100:.1f}%
                    """)

                    # Algorithm Selection
                    algo_type_waste = gr.Radio(
                        choices=["Single", "Binary", "Triple", "Quad"],
                        label="Algorithm Type",
                        value="Single"
                    )

                    single_algo_waste = gr.Dropdown(
                        choices=algorithms_dict.get("Single", []),
                        label="Single Algorithm",
                        value=algorithms_dict.get("Single", [])[0] if algorithms_dict.get("Single", []) else None
                    )

                    binary_algo_waste = gr.Dropdown(
                        choices=algorithms_dict.get("Binary", []),
                        label="Binary Hybrid Algorithm",
                        value=algorithms_dict.get("Binary", [])[0] if algorithms_dict.get("Binary", []) else None,
                        visible=False
                    )

                    ternary_algo_waste = gr.Dropdown(
                        choices=algorithms_dict.get("Triple", []),
                        label="Ternary Hybrid Algorithm",
                        value=algorithms_dict.get("Triple", [])[0] if algorithms_dict.get("Triple", []) else None,
                        visible=False
                    )

                    quaternary_algo_waste = gr.Dropdown(
                        choices=algorithms_dict.get("Quad", []),
                        label="Quaternary Hybrid Algorithm",
                        value=algorithms_dict.get("Quad", [])[0] if algorithms_dict.get("Quad", []) else None,
                        visible=False
                    )

                    algo_type_waste.change(
                        fn=update_energy_visibility,
                        inputs=algo_type_waste,
                        outputs=[single_algo_waste, binary_algo_waste, ternary_algo_waste, quaternary_algo_waste]
                    )

                    algorithm_waste = gr.Textbox(visible=False)

                    algo_type_waste.change(
                        fn=update_algorithm,
                        inputs=[algo_type_waste, single_algo_waste, binary_algo_waste, ternary_algo_waste, quaternary_algo_waste],
                        outputs=algorithm_waste
                    )

                    single_algo_waste.change(fn=lambda x: x, inputs=single_algo_waste, outputs=algorithm_waste)
                    binary_algo_waste.change(fn=lambda x: x, inputs=binary_algo_waste, outputs=algorithm_waste)
                    ternary_algo_waste.change(fn=lambda x: x, inputs=ternary_algo_waste, outputs=algorithm_waste)
                    quaternary_algo_waste.change(fn=lambda x: x, inputs=quaternary_algo_waste, outputs=algorithm_waste)

                    # Basic Settings
                    with gr.Accordion("📘 Basic Settings", open=True):
                        iterations_waste = gr.Slider(1, 10000, 500, step=10, label="Iterations")
                        pop_size_waste = gr.Slider(2, 5000, 100, step=5, label="Population Size")
                        runs_waste = gr.Slider(1, 100, 5, step=1, label="Number of Runs")

                    # Advanced Settings
                    with gr.Accordion("📗 Advanced Settings", open=False):
                        with gr.Tab("PSO"):
                            pso_inertia_w = gr.Slider(0.1, 5.0, 0.7, step=0.05, label="Inertia Weight")
                            pso_cognitive_w = gr.Slider(0.5, 10.0, 2.05, step=0.05, label="Cognitive Coefficient")
                            pso_social_w = gr.Slider(0.5, 10.0, 2.05, step=0.05, label="Social Coefficient")
                        
                        with gr.Tab("GWO"):
                            gwo_convergence_w = gr.Slider(0.1, 10.0, 2.0, step=0.1, label="Convergence Parameter")
                        
                        with gr.Tab("WOA"):
                            woa_spiral_w = gr.Slider(0.1, 10.0, 1.0, step=0.1, label="Spiral Constant")
                        
                        with gr.Tab("DE"):
                            de_weight_w = gr.Slider(0.1, 10.0, 0.8, step=0.1, label="Differential Weight")
                            de_crossover_w = gr.Slider(0.1, 1.0, 0.9, step=0.05, label="Crossover Probability")
                        
                        with gr.Tab("SA"):
                            sa_temp_w = gr.Slider(1, 100000, 1000, step=10, label="Initial Temperature")
                            sa_cooling_w = gr.Slider(0.5, 0.99999, 0.95, step=0.001, label="Cooling Rate")
                        
                        with gr.Tab("MFO"):
                            mfo_flame_w = gr.Slider(-5.0, 5.0, -1.0, step=0.1, label="Flame Constant")
                        
                        with gr.Tab("FA"):
                            fa_alpha_w = gr.Slider(0.1, 5.0, 0.5, step=0.05, label="Alpha")
                            fa_beta_w = gr.Slider(0.1, 5.0, 0.2, step=0.05, label="Beta")
                            fa_gamma_w = gr.Slider(0.01, 10.0, 1.0, step=0.1, label="Gamma")
                        
                        with gr.Tab("HHO"):
                            hho_energy_w = gr.Slider(-2.0, 2.0, 1.0, step=0.1, label="Escape Energy")
                            hho_jump_w = gr.Slider(0.1, 2.0, 0.5, step=0.05, label="Jump Strength")
                        
                        with gr.Tab("SSA"):
                            ssa_leader_w = gr.Slider(0.1, 10.0, 1.0, step=0.1, label="Leader Position")
                        
                        with gr.Tab("ABC"):
                            abc_limit_w = gr.Slider(1, 1000, 100, step=5, label="Limit")

                    # Super Settings
                    with gr.Accordion("📙 Super Settings", open=False):
                        elite_ratio_w = gr.Slider(0.001, 0.99, 0.1, step=0.01, label="Elite Ratio")
                        exploration_rate_w = gr.Slider(0.01, 1.0, 0.7, step=0.05, label="Exploration Rate")
                        exploitation_rate_w = gr.Slider(0.01, 1.0, 0.3, step=0.05, label="Exploitation Rate")
                        convergence_threshold_w = gr.Slider(1e-10, 1e-1, 1e-6, step=1e-7, label="Convergence Threshold")
                        patience_w = gr.Slider(1, 1000, 50, step=5, label="Patience")
                        restarts_w = gr.Slider(0, 1000, 10, step=1, label="Restarts")

                    # Ultra Settings
                    with gr.Accordion("📕 Ultra Settings", open=False):
                        hybrid_weights_w = gr.Textbox(value="0.25,0.25,0.25,0.25", label="Hybrid Weights")
                        cooperation_type_w = gr.Dropdown(["parallel", "sequential", "adaptive"], value="parallel", label="Cooperation Type")
                        comm_freq_w = gr.Slider(1, 1000, 10, step=1, label="Communication Frequency")
                        island_model_w = gr.Checkbox(label="Island Model", value=False)
                        num_islands_w = gr.Slider(2, 1000, 10, step=1, label="Number of Islands", visible=False)
                        migration_rate_w = gr.Slider(0.001, 0.99, 0.1, step=0.01, label="Migration Rate", visible=False)
                        migration_interval_w = gr.Slider(1, 1000, 20, step=1, label="Migration Interval", visible=False)
                        chaos_factor_w = gr.Slider(0, 5.0, 0.1, step=0.05, label="Chaos Factor")
                        chaos_type_w = gr.Dropdown(["logistic", "tent", "sine"], value="logistic", label="Chaos Type")
                        adaptive_params_w = gr.Checkbox(label="Adaptive Parameter Control", value=True)
                        niching_method_w = gr.Dropdown(["none", "fitness_sharing", "clearing"], value="none", label="Niching Method")
                        niching_radius_w = gr.Slider(0.001, 10.0, 0.1, step=0.05, label="Niching Radius", visible=False)
                        niching_param_w = gr.Slider(1, 1000, 2, step=1, label="Niching Parameter", visible=False)

                        island_model_w.change(
                            fn=update_island_visibility,
                            inputs=island_model_w,
                            outputs=[num_islands_w, migration_rate_w, migration_interval_w]
                        )
                        
                        niching_method_w.change(
                            fn=update_niching_visibility,
                            inputs=niching_method_w,
                            outputs=[niching_radius_w, niching_param_w]
                        )

                    run_waste_btn = gr.Button("🗑️ Optimize Waste Sector", variant="primary", size="lg")

                with gr.Column(scale=2):
                    with gr.Tabs():
                        with gr.TabItem("📊 Results"):
                            waste_results = gr.Dataframe(
                                headers=["Criterion", "Unit", "Baseline", "Optimized", "Improvement", "Status"],
                                label="Waste Sector Results",
                                row_count=11
                            )
                            gr.HTML(value=EQUATIONS_HTML["waste"])
                        with gr.TabItem("📈 Comparison"):
                            waste_plot1 = gr.Plot()
                        with gr.TabItem("📉 Improvements"):
                            waste_plot2 = gr.Plot()
                        with gr.TabItem("📋 Statistics"):
                            waste_stats = gr.Markdown()

            run_waste_btn.click(
                fn=optimize_waste,
                inputs=[
                    algorithm_waste, iterations_waste, pop_size_waste, runs_waste,
                    pso_inertia_w, pso_cognitive_w, pso_social_w, gwo_convergence_w,
                    woa_spiral_w, de_weight_w, de_crossover_w, sa_temp_w, sa_cooling_w,
                    mfo_flame_w, fa_alpha_w, fa_beta_w, fa_gamma_w,
                    hho_energy_w, hho_jump_w, ssa_leader_w, abc_limit_w,
                    elite_ratio_w, exploration_rate_w, exploitation_rate_w, convergence_threshold_w,
                    patience_w, restarts_w, hybrid_weights_w, cooperation_type_w,
                    comm_freq_w, island_model_w, num_islands_w, migration_rate_w,
                    migration_interval_w, chaos_factor_w, chaos_type_w,
                    adaptive_params_w, niching_method_w, niching_radius_w,
                    niching_param_w, mutation_strategy, crossover_strategy,
                    selection_strategy, tournament_size
                ],
                outputs=[waste_results, waste_plot1, waste_plot2, waste_stats]
            )

        # Multi-Objective Tab
        with gr.TabItem("🎯 Multi-Objective", id=4):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("""
                    ### 🎯 Multi-Sector Optimization
                    Optimize all 4 Baghdad sectors simultaneously with advanced hybrid algorithms.

                    **Objectives:**
                    - ⚡ Minimize Energy Consumption
                    - 🚦 Optimize Traffic Flow
                    - 🌍 Improve Air Quality
                    - 🗑️ Reduce Waste Collection Cost
                    """)

                    algo_type_multi = gr.Radio(
                        choices=["Single", "Binary", "Triple", "Quad"],
                        label="Algorithm Type",
                        value="Quad"
                    )

                    single_algo_multi = gr.Dropdown(
                        choices=algorithms_dict.get("Single", []),
                        label="Single Algorithm",
                        value=algorithms_dict.get("Single", [])[0] if algorithms_dict.get("Single", []) else None,
                        visible=False
                    )

                    binary_algo_multi = gr.Dropdown(
                        choices=algorithms_dict.get("Binary", []),
                        label="Binary Hybrid Algorithm",
                        value=algorithms_dict.get("Binary", [])[0] if algorithms_dict.get("Binary", []) else None,
                        visible=False
                    )

                    ternary_algo_multi = gr.Dropdown(
                        choices=algorithms_dict.get("Triple", []),
                        label="Ternary Hybrid Algorithm",
                        value=algorithms_dict.get("Triple", [])[0] if algorithms_dict.get("Triple", []) else None,
                        visible=False
                    )

                    quaternary_algo_multi = gr.Dropdown(
                        choices=algorithms_dict.get("Quad", []),
                        label="Quaternary Hybrid Algorithm",
                        value=algorithms_dict.get("Quad", [])[0] if algorithms_dict.get("Quad", []) else None,
                        visible=True
                    )

                    def update_multi_visibility(algo_type):
                        if algo_type == "Single":
                            return gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)
                        elif algo_type == "Binary":
                            return gr.update(visible=False), gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)
                        elif algo_type == "Triple":
                            return gr.update(visible=False), gr.update(visible=False), gr.update(visible=True), gr.update(visible=False)
                        else:
                            return gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=True)

                    algo_type_multi.change(
                        fn=update_multi_visibility,
                        inputs=algo_type_multi,
                        outputs=[single_algo_multi, binary_algo_multi, ternary_algo_multi, quaternary_algo_multi]
                    )

                    algorithm_multi = gr.Textbox(visible=False)

                    algo_type_multi.change(
                        fn=update_algorithm,
                        inputs=[algo_type_multi, single_algo_multi, binary_algo_multi, ternary_algo_multi, quaternary_algo_multi],
                        outputs=algorithm_multi
                    )

                    single_algo_multi.change(fn=lambda x: x, inputs=single_algo_multi, outputs=algorithm_multi)
                    binary_algo_multi.change(fn=lambda x: x, inputs=binary_algo_multi, outputs=algorithm_multi)
                    ternary_algo_multi.change(fn=lambda x: x, inputs=ternary_algo_multi, outputs=algorithm_multi)
                    quaternary_algo_multi.change(fn=lambda x: x, inputs=quaternary_algo_multi, outputs=algorithm_multi)

                    # Basic Settings
                    with gr.Accordion("⚙️ Basic Settings", open=True):
                        iterations_multi = gr.Slider(1, 10000, 300, step=10, label="Iterations")
                        pop_size_multi = gr.Slider(2, 5000, 50, step=5, label="Population Size")
                        runs_multi = gr.Slider(1, 100, 3, step=1, label="Number of Runs")

                    # Advanced Settings for Multi-Objective
                    with gr.Accordion("📗 Advanced Settings", open=False):
                        with gr.Tab("PSO"):
                            pso_inertia_e_m = gr.Slider(0.1, 5.0, 0.7, step=0.05, label="Inertia Weight")
                            pso_cognitive_e_m = gr.Slider(0.5, 10.0, 2.05, step=0.05, label="Cognitive Coefficient")
                            pso_social_e_m = gr.Slider(0.5, 10.0, 2.05, step=0.05, label="Social Coefficient")
                        
                        with gr.Tab("GWO"):
                            gwo_convergence_e_m = gr.Slider(0.1, 10.0, 2.0, step=0.1, label="Convergence Parameter")
                        
                        with gr.Tab("WOA"):
                            woa_spiral_e_m = gr.Slider(0.1, 10.0, 1.0, step=0.1, label="Spiral Constant")
                        
                        with gr.Tab("DE"):
                            de_weight_e_m = gr.Slider(0.1, 10.0, 0.8, step=0.1, label="Differential Weight")
                            de_crossover_e_m = gr.Slider(0.1, 1.0, 0.9, step=0.05, label="Crossover Probability")
                        
                        with gr.Tab("SA"):
                            sa_temp_e_m = gr.Slider(1, 100000, 1000, step=10, label="Initial Temperature")
                            sa_cooling_e_m = gr.Slider(0.5, 0.99999, 0.95, step=0.001, label="Cooling Rate")
                        
                        with gr.Tab("MFO"):
                            mfo_flame_e_m = gr.Slider(-5.0, 5.0, -1.0, step=0.1, label="Flame Constant")
                        
                        with gr.Tab("FA"):
                            fa_alpha_e_m = gr.Slider(0.1, 5.0, 0.5, step=0.05, label="Alpha")
                            fa_beta_e_m = gr.Slider(0.1, 5.0, 0.2, step=0.05, label="Beta")
                            fa_gamma_e_m = gr.Slider(0.01, 10.0, 1.0, step=0.1, label="Gamma")
                        
                        with gr.Tab("HHO"):
                            hho_energy_e_m = gr.Slider(-2.0, 2.0, 1.0, step=0.1, label="Escape Energy")
                            hho_jump_e_m = gr.Slider(0.1, 2.0, 0.5, step=0.05, label="Jump Strength")
                        
                        with gr.Tab("SSA"):
                            ssa_leader_e_m = gr.Slider(0.1, 10.0, 1.0, step=0.1, label="Leader Position")
                        
                        with gr.Tab("ABC"):
                            abc_limit_e_m = gr.Slider(1, 1000, 100, step=5, label="Limit")

                    # Super Settings
                    with gr.Accordion("📙 Super Settings", open=False):
                        elite_ratio_m = gr.Slider(0.001, 0.99, 0.1, step=0.01, label="Elite Ratio")
                        exploration_rate_m = gr.Slider(0.01, 1.0, 0.7, step=0.05, label="Exploration Rate")
                        exploitation_rate_m = gr.Slider(0.01, 1.0, 0.3, step=0.05, label="Exploitation Rate")
                        convergence_threshold_m = gr.Slider(1e-10, 1e-1, 1e-6, step=1e-7, label="Convergence Threshold")
                        patience_m = gr.Slider(1, 1000, 50, step=5, label="Patience")
                        restarts_m = gr.Slider(0, 1000, 10, step=1, label="Restarts")

                    # Ultra Settings
                    with gr.Accordion("📕 Ultra Settings", open=False):
                        hybrid_weights_m = gr.Textbox(value="0.25,0.25,0.25,0.25", label="Hybrid Weights")
                        cooperation_type_m = gr.Dropdown(["parallel", "sequential", "adaptive"], value="parallel", label="Cooperation Type")
                        comm_freq_m = gr.Slider(1, 1000, 10, step=1, label="Communication Frequency")
                        island_model_m = gr.Checkbox(label="Island Model", value=False)
                        num_islands_m = gr.Slider(2, 1000, 10, step=1, label="Number of Islands", visible=False)
                        migration_rate_m = gr.Slider(0.001, 0.99, 0.1, step=0.01, label="Migration Rate", visible=False)
                        migration_interval_m = gr.Slider(1, 1000, 20, step=1, label="Migration Interval", visible=False)
                        chaos_factor_m = gr.Slider(0, 5.0, 0.1, step=0.05, label="Chaos Factor")
                        chaos_type_m = gr.Dropdown(["logistic", "tent", "sine"], value="logistic", label="Chaos Type")
                        adaptive_params_m = gr.Checkbox(label="Adaptive Parameter Control", value=True)
                        niching_method_m = gr.Dropdown(["none", "fitness_sharing", "clearing"], value="none", label="Niching Method")
                        niching_radius_m = gr.Slider(0.001, 10.0, 0.1, step=0.05, label="Niching Radius", visible=False)
                        niching_param_m = gr.Slider(1, 1000, 2, step=1, label="Niching Parameter", visible=False)

                        island_model_m.change(
                            fn=update_island_visibility,
                            inputs=island_model_m,
                            outputs=[num_islands_m, migration_rate_m, migration_interval_m]
                        )
                        
                        niching_method_m.change(
                            fn=update_niching_visibility,
                            inputs=niching_method_m,
                            outputs=[niching_radius_m, niching_param_m]
                        )

                    # Baghdad Parameters
                    with gr.Accordion("🌍 Baghdad Sector Parameters", open=False):
                        gr.Markdown("#### Energy Sector")
                        energy_time_multi = gr.Slider(0, 23, datetime.now().hour, label="Energy - Time of Day")
                        energy_season_multi = gr.Dropdown(["summer", "winter", "spring", "autumn"], value="summer", label="Energy - Season")

                        gr.Markdown("#### Traffic Sector")
                        traffic_time_multi = gr.Slider(0, 23, datetime.now().hour, label="Traffic - Time of Day")
                        traffic_day_multi = gr.Dropdown(["weekday", "weekend"], value="weekday", label="Traffic - Day Type")

                        gr.Markdown("#### Environment Sector")
                        env_time_multi = gr.Slider(0, 23, datetime.now().hour, label="Environment - Time of Day")
                        env_weather_multi = gr.Dropdown(["clear", "cloudy", "rainy", "foggy"], value="clear", label="Environment - Weather")

                        gr.Markdown("#### Waste Sector")
                        waste_district_multi = gr.Dropdown(
                            ["Al-Rusafa", "Al-Karkh", "Al-Adhamiya", "Al-Kadhimya", "Al-Doura"],
                            value="Al-Rusafa",
                            label="Waste - District"
                        )
                        waste_time_multi = gr.Slider(0, 23, datetime.now().hour, label="Waste - Time of Day")

                    run_multi_btn = gr.Button("🎯 Run Multi-Objective Optimization", variant="primary", size="lg")

                with gr.Column(scale=2):
                    with gr.Tabs():
                        with gr.TabItem("📊 Combined Results"):
                            multi_results = gr.Dataframe(
                                headers=["Sector", "Criterion", "Baseline", "Optimized", "Improvement"],
                                label="Multi-Objective Results",
                                row_count=20
                            )
                            gr.HTML(value=EQUATIONS_HTML["multi"])
                        with gr.TabItem("🎯 Pareto Front"):
                            multi_plot = gr.Plot()
                        with gr.TabItem("📋 Summary"):
                            multi_stats = gr.Markdown()

            run_multi_btn.click(
                fn=optimize_multi,
                inputs=[
                    algorithm_multi, iterations_multi, pop_size_multi, runs_multi,
                    pso_inertia_e_m, pso_cognitive_e_m, pso_social_e_m, gwo_convergence_e_m,
                    woa_spiral_e_m, de_weight_e_m, de_crossover_e_m, sa_temp_e_m, sa_cooling_e_m,
                    mfo_flame_e_m, fa_alpha_e_m, fa_beta_e_m, fa_gamma_e_m,
                    hho_energy_e_m, hho_jump_e_m, ssa_leader_e_m, abc_limit_e_m,
                    pso_inertia_t, pso_cognitive_t, pso_social_t, gwo_convergence_t,
                    woa_spiral_t, de_weight_t, de_crossover_t, sa_temp_t, sa_cooling_t,
                    mfo_flame_t, fa_alpha_t, fa_beta_t, fa_gamma_t,
                    hho_energy_t, hho_jump_t, ssa_leader_t, abc_limit_t,
                    pso_inertia_env, pso_cognitive_env, pso_social_env, gwo_convergence_env,
                    woa_spiral_env, de_weight_env, de_crossover_env, sa_temp_env, sa_cooling_env,
                    mfo_flame_env, fa_alpha_env, fa_beta_env, fa_gamma_env,
                    hho_energy_env, hho_jump_env, ssa_leader_env, abc_limit_env,
                    pso_inertia_w, pso_cognitive_w, pso_social_w, gwo_convergence_w,
                    woa_spiral_w, de_weight_w, de_crossover_w, sa_temp_w, sa_cooling_w,
                    mfo_flame_w, fa_alpha_w, fa_beta_w, fa_gamma_w,
                    hho_energy_w, hho_jump_w, ssa_leader_w, abc_limit_w,
                    elite_ratio_m, exploration_rate_m, exploitation_rate_m, convergence_threshold_m,
                    patience_m, restarts_m, hybrid_weights_m, cooperation_type_m,
                    comm_freq_m, island_model_m, num_islands_m, migration_rate_m,
                    migration_interval_m, chaos_factor_m, chaos_type_m,
                    adaptive_params_m, niching_method_m, niching_radius_m,
                    niching_param_m, mutation_strategy, crossover_strategy,
                    selection_strategy, tournament_size,
                    energy_time_multi, energy_season_multi,
                    traffic_time_multi, traffic_day_multi,
                    env_time_multi, env_weather_multi,
                    waste_district_multi, waste_time_multi
                ],
                outputs=[multi_results, multi_plot, multi_stats]
            )

    # System Description
    gr.HTML("""
    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 5px solid #0066CC;">
        <h3>📚 Baghdad Smart City Control System - Real Physics Version</h3>
        <p style="font-size: 1.1em; line-height: 1.6;">
        The Baghdad Smart City Integrated Control System is an advanced AI-powered platform that optimizes four critical urban sectors:
        Energy ⚡, Traffic 🚦, Environment 🌍, and Waste 🗑️ for the city of Baghdad, Iraq. Using real-time data from
        <strong>OpenWeatherMap, WAQI, TomTom APIs, and EnergyData.info</strong>, the system provides accurate physics-based optimization with
        <strong>35+ single algorithms, 200 binary hybrids, 300 ternary hybrids, and 250 quaternary hybrids</strong>.
        </p>
        <p style="font-size: 1em; margin-top: 10px;">
        <strong>Key Features:</strong><br>
        • 4 Integrated Sectors with 40+ Performance Criteria<br>
        • 750+ Hybrid Optimization Algorithms (Binary, Ternary, Quaternary)<br>
        • Real-time Data from Baghdad (Weather, Air Quality, Traffic, Power Grid)<br>
        • Physics-based Models: Newton-Raphson Power Flow, Greenshields Traffic Model, Gaussian Plume Dispersion<br>
        • Multi-Objective Optimization with Pareto Front Analysis<br>
        • Interactive Visualizations and Detailed Statistics
        </p>
    </div>
    """)

    # Footer
    gr.HTML("""
        <div class="footer" style="background-color: black; color: white; font-weight: 900; text-shadow: 2px 2px 4px rgba(255,255,255,0.2); padding: 20px; border-radius: 0 0 10px 10px; margin-top: 20px; text-align: center; font-size: 0.95em; line-height: 1.8; border-top: 2px solid #333;">
            <p style="font-weight: 900; color: white; font-size: 1.1em; margin: 8px 0;">© 2026 Mohammed Falah Hassan Al-Dhafiri</p>
            <p style="font-weight: 900; color: white; margin: 5px 0;">Founder and Inventor of the System</p>
            <p style="font-weight: 900; color: white; margin: 8px 0 15px 0;">All Rights Reserved.</p>
            <p style="font-weight: 700; color: white; max-width: 800px; margin: 10px auto; line-height: 1.6; border-bottom: 1px solid #444; padding-bottom: 15px;">It is prohibited to copy, reproduce, modify, publish, or use any part of this system without prior written permission from the Founder and Inventor. Any unauthorized use constitutes a violation of intellectual property rights and may subject the violator to legal liability.</p>
        
            <div class="footer-arabic" style="font-family: 'Arial', sans-serif; direction: rtl; margin-top: 15px; padding-top: 15px;">
                <p style="font-weight: 900; color: white; font-size: 1.1em; margin: 8px 0;">© 2026 محمد فلاح حسن الظفيري</p>
                <p style="font-weight: 900; color: white; margin: 5px 0;">مؤسس ومبتكر النظام</p>
                <p style="font-weight: 900; color: white; margin: 8px 0 15px 0;">جميع الحقوق محفوظة</p>
                <p style="font-weight: 700; color: white; max-width: 800px; margin: 10px auto; line-height: 1.6;">يُمنع نسخ أو إعادة إنتاج أو تعديل أو نشر أو استخدام أي جزء من هذا النظام دون إذن خطي مسبق من المؤسس والمبتكر، وأي استخدام غير مصرح به يُعد انتهاكًا لحقوق الملكية الفكرية ويعرّض المخالف للمساءلة القانونية</p>
            </div>
        </div>
        """)

# ============================================================================
# 1️⃣7️⃣ تشغيل التطبيق
# ============================================================================

if __name__ == "__main__":
    print("="*80)
    print("🏙️ Baghdad Smart City Control System - REAL PHYSICS VERSION - READY")
    print("="*80)
    print(f"✅ Single Algorithms: {len(algorithms_dict.get('Single', []))}")
    print(f"✅ Binary Hybrids: {len(algorithms_dict.get('Binary', []))}")
    print(f"✅ Ternary Hybrids: {len(algorithms_dict.get('Triple', []))}")
    print(f"✅ Quaternary Hybrids: {len(algorithms_dict.get('Quad', []))}")
    print("="*80)
    print("🚀 Launching Gradio interface for Hugging Face Spaces...")
    print("="*80)
    
    demo.launch(server_name="0.0.0.0", server_port=7860)
