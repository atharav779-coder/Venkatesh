import re
import json

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add CSS for buttons and modal
buttons_css = """
    /* ===== INFO BUTTONS BELOW CARDS ===== */
    .card-buttons {
      display: flex; gap: 0.6rem; margin-top: 1rem;
      flex-wrap: wrap; justify-content: center;
    }
    .info-btn {
      background: rgba(0,212,255,0.08);
      border: 1px solid rgba(0,212,255,0.25);
      color: #00d4ff; padding: 0.5rem 0.8rem;
      border-radius: 6px; cursor: pointer;
      font-family: 'Rajdhani', sans-serif; font-weight: 700;
      font-size: 0.72rem; text-transform: uppercase; letter-spacing: 1.5px;
      transition: all 0.3s; flex: 1; min-width: 0; text-align: center;
      line-height: 1.3;
    }
    .info-btn:hover {
      background: #00d4ff; color: #000;
      box-shadow: 0 0 15px rgba(0,212,255,0.5);
    }
    .info-btn .btn-icon { display: block; font-size: 1.1rem; margin-bottom: 2px; }

    /* ===== MODAL ===== */
    .modal-overlay {
      position: fixed; inset: 0; z-index: 9999;
      background: rgba(0,0,0,0.85);
      backdrop-filter: blur(8px);
      display: none; align-items: center; justify-content: center;
      padding: 2rem; opacity: 0; transition: opacity 0.3s;
    }
    .modal-overlay.active { display: flex; opacity: 1; }
    .modal-box {
      background: linear-gradient(160deg, #0c1222, #050810);
      border: 1px solid rgba(0,212,255,0.3);
      border-radius: 12px; max-width: 700px; width: 100%;
      max-height: 85vh; overflow-y: auto;
      box-shadow: 0 20px 60px rgba(0,0,0,0.8), 0 0 40px rgba(0,212,255,0.1);
      padding: 2.5rem;
    }
    .modal-box::-webkit-scrollbar { width: 5px; }
    .modal-box::-webkit-scrollbar-thumb { background: rgba(0,212,255,0.4); border-radius: 10px; }
    .modal-close {
      position: absolute; top: 1rem; right: 1.5rem;
      background: none; border: 1px solid rgba(0,212,255,0.3);
      color: #00d4ff; font-size: 1.5rem; cursor: pointer;
      width: 36px; height: 36px; border-radius: 6px;
      display: flex; align-items: center; justify-content: center;
      transition: all 0.3s;
    }
    .modal-close:hover { background: #00d4ff; color: #000; }
    .modal-title {
      font-family: 'Orbitron', sans-serif; font-size: 1.3rem; font-weight: 800;
      color: #fff; text-transform: uppercase; letter-spacing: 1px;
      margin-bottom: 0.3rem;
    }
    .modal-subtitle {
      font-family: 'Rajdhani', sans-serif; font-size: 0.85rem;
      color: #00d4ff; text-transform: uppercase; letter-spacing: 2px;
      font-weight: 700; margin-bottom: 1.5rem;
      padding-bottom: 1rem; border-bottom: 1px solid rgba(0,212,255,0.2);
    }
    .modal-section {
      margin-bottom: 1.5rem;
    }
    .modal-section h4 {
      font-family: 'Rajdhani', sans-serif; font-size: 0.85rem; font-weight: 700;
      color: #00d4ff; text-transform: uppercase; letter-spacing: 2px;
      margin-bottom: 0.6rem;
      padding-left: 0.8rem; border-left: 3px solid #00d4ff;
    }
    .modal-grid {
      display: grid; grid-template-columns: 1fr 1fr; gap: 0.6rem;
    }
    .modal-item {
      background: rgba(0,212,255,0.05);
      border: 1px solid rgba(0,212,255,0.1);
      border-radius: 4px; padding: 0.7rem 0.9rem;
    }
    .modal-item .m-label {
      font-family: 'Rajdhani', sans-serif; font-size: 0.65rem;
      color: #7a8ba8; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700;
    }
    .modal-item .m-value {
      font-family: 'Rajdhani', sans-serif; font-size: 0.9rem;
      color: #fff; font-weight: 600; letter-spacing: 1px; margin-top: 2px;
    }
    .modal-desc {
      font-size: 0.85rem; color: #8a9bb8; line-height: 1.6;
      padding: 0.8rem 1rem; background: rgba(0,0,0,0.3);
      border-radius: 6px; border-left: 3px solid rgba(0,212,255,0.4);
    }
    @media (max-width: 600px) {
      .modal-grid { grid-template-columns: 1fr; }
      .modal-box { padding: 1.5rem; }
      .card-buttons { flex-direction: column; }
    }
"""

content = content.replace('/* ===== FOOTER ===== */', buttons_css + '\n    /* ===== FOOTER ===== */')

# 2. Add the modal HTML before </body>
modal_html = """
<!-- ===== INFO MODAL ===== -->
<div class="modal-overlay" id="infoModal">
  <div class="modal-box" style="position:relative;">
    <button class="modal-close" id="modalClose">&times;</button>
    <div id="modalContent"></div>
  </div>
</div>
"""
content = content.replace('</body>', modal_html + '\n</body>')

# 3. Add detailed data for all planes
detail_data = {}

# COMMERCIAL
detail_data["Boeing 747-8"] = {
    "cabin": {"Cabin Length": "57.3 m", "Cabin Width": "6.1 m", "Seat Pitch (Econ)": "31-32 in", "Seat Pitch (Business)": "60-78 in", "Aisle Width": "Dual aisle, 51 cm each", "IFE System": "Panasonic eX3 / Thales AVANT", "Blind Spots": "Nose below cockpit, rear empennage", "Config Options": "3-class 410 / 2-class 467"},
    "airframe": {"Engine Model": "GEnx-2B67", "Engine Type": "High-bypass turbofan", "Bypass Ratio": "8.0:1", "Compressor Stages": "4 LP + 10 HP", "Turbine Stages": "2 HP + 7 LP", "Engine Dry Weight": "5,622 kg each", "Key Components": "Composite fan blades, titanium core", "Airframe Material": "Aluminum alloy + composite fairings"},
    "performance": {"MTOW": "447,696 kg (987,000 lb)", "T/W Ratio": "0.27", "Service Ceiling": "13,100 m (43,000 ft)", "Runway Required": "3,050 m (10,000 ft)", "Max Fuel": "216,840 L (57,285 US gal)", "Climb Rate": "490 m/min", "Approach Speed": "260 km/h (140 kt)", "Wing Loading": "730 kg/m2"}
}

detail_data["Airbus A380"] = {
    "cabin": {"Cabin Length": "49.9 m (main) + 44.9 m (upper)", "Cabin Width": "6.58 m (main deck)", "Seat Pitch (Econ)": "32 in", "Seat Pitch (First)": "86 in (suites)", "Aisle Width": "Dual aisle both decks", "IFE System": "Thales TopSeries / Panasonic eX3", "Blind Spots": "Below nose, wing root zones", "Config Options": "3-class 525 / 1-class 853 max"},
    "airframe": {"Engine Model": "Rolls-Royce Trent 900", "Engine Type": "High-bypass turbofan", "Bypass Ratio": "8.7:1", "Compressor Stages": "8 IP + 6 HP", "Turbine Stages": "1 HP + 1 IP + 5 LP", "Engine Dry Weight": "6,246 kg each", "Key Components": "GLARE fuselage panels, CFRP wing box", "Airframe Material": "25% composite + aluminum-lithium"},
    "performance": {"MTOW": "575,000 kg (1,268,000 lb)", "T/W Ratio": "0.22", "Service Ceiling": "13,136 m (43,100 ft)", "Runway Required": "2,900 m (9,500 ft)", "Max Fuel": "320,000 L (84,535 US gal)", "Climb Rate": "520 m/min", "Approach Speed": "260 km/h (140 kt)", "Wing Loading": "663 kg/m2"}
}

detail_data["Boeing 787 Dreamliner"] = {
    "cabin": {"Cabin Length": "50.7 m", "Cabin Width": "5.49 m", "Seat Pitch (Econ)": "31-33 in", "Seat Pitch (Business)": "60-78 in", "Aisle Width": "Dual aisle, 53 cm", "IFE System": "Panasonic eX3 / Thales AVANT", "Blind Spots": "Standard nose blind area", "Config Options": "2-class 242 / 3-class 210-330"},
    "airframe": {"Engine Model": "GEnx-1B / Rolls-Royce Trent 1000", "Engine Type": "High-bypass turbofan", "Bypass Ratio": "9.6:1 (GEnx)", "Compressor Stages": "4 LP + 10 HP", "Turbine Stages": "2 HP + 7 LP", "Engine Dry Weight": "5,812 kg each", "Key Components": "50% CFRP, one-piece barrel fuselage", "Airframe Material": "Carbon fiber reinforced polymer"},
    "performance": {"MTOW": "254,011 kg (560,000 lb)", "T/W Ratio": "0.25", "Service Ceiling": "13,100 m (43,000 ft)", "Runway Required": "2,600 m (8,500 ft)", "Max Fuel": "126,917 L (33,528 US gal)", "Climb Rate": "500 m/min", "Approach Speed": "250 km/h (135 kt)", "Wing Loading": "587 kg/m2"}
}

detail_data["Airbus A350 XWB"] = {
    "cabin": {"Cabin Length": "51.04 m (-900) / 60.76 m (-1000)", "Cabin Width": "5.61 m", "Seat Pitch (Econ)": "31-32 in", "Seat Pitch (Business)": "44-82 in", "Aisle Width": "Dual aisle, 52.5 cm", "IFE System": "Thales AVANT Up / Panasonic X-series", "Blind Spots": "Minimal — camera systems installed", "Config Options": "3-class 300 / high-density 440"},
    "airframe": {"Engine Model": "Rolls-Royce Trent XWB-84 / XWB-97", "Engine Type": "High-bypass turbofan", "Bypass Ratio": "9.6:1", "Compressor Stages": "8 IP + 6 HP", "Turbine Stages": "1 HP + 1 IP + 6 LP", "Engine Dry Weight": "7,277 kg each", "Key Components": "53% CFRP, thermoplastic wing rib", "Airframe Material": "Carbon fiber + titanium + aluminum"},
    "performance": {"MTOW": "316,000 kg (696,700 lb)", "T/W Ratio": "0.24", "Service Ceiling": "13,100 m (43,100 ft)", "Runway Required": "2,600 m (8,530 ft)", "Max Fuel": "141,000 L (37,250 US gal)", "Climb Rate": "512 m/min", "Approach Speed": "255 km/h (138 kt)", "Wing Loading": "620 kg/m2"}
}

detail_data["Boeing 777X"] = {
    "cabin": {"Cabin Length": "63.73 m", "Cabin Width": "5.87 m", "Seat Pitch (Econ)": "32 in", "Seat Pitch (Business)": "78 in", "Aisle Width": "Dual aisle, 48 cm", "IFE System": "Next-gen Panasonic Astrova", "Blind Spots": "Reduced by 4 external cameras", "Config Options": "2-class 384 / 3-class 365-426"},
    "airframe": {"Engine Model": "GE9X-105B1A", "Engine Type": "High-bypass turbofan (world's largest)", "Bypass Ratio": "10:1", "Compressor Stages": "3 LP + 11 HP", "Turbine Stages": "2 HP + 8 LP", "Engine Dry Weight": "8,296 kg each", "Key Components": "Carbon fiber composite wing, folding tips", "Airframe Material": "Aluminum + composite wing + CMC turbine"},
    "performance": {"MTOW": "351,534 kg (775,000 lb)", "T/W Ratio": "0.27", "Service Ceiling": "13,100 m (43,000 ft)", "Runway Required": "3,050 m (10,000 ft)", "Max Fuel": "197,977 L (52,300 US gal)", "Climb Rate": "530 m/min", "Approach Speed": "265 km/h (143 kt)", "Wing Loading": "700 kg/m2"}
}

detail_data["Airbus A320neo"] = {
    "cabin": {"Cabin Length": "27.51 m", "Cabin Width": "3.70 m", "Seat Pitch (Econ)": "28-32 in", "Seat Pitch (Business)": "38-52 in", "Aisle Width": "Single aisle, 50 cm", "IFE System": "Immersive / RAVE streaming", "Blind Spots": "Standard narrow-body nose area", "Config Options": "2-class 150 / high-density 194"},
    "airframe": {"Engine Model": "CFM LEAP-1A / PW1100G-JM", "Engine Type": "Geared turbofan (PW) / direct-drive (CFM)", "Bypass Ratio": "11:1 (LEAP) / 12.5:1 (PW)", "Compressor Stages": "3 LP + 10 HP (LEAP)", "Turbine Stages": "2 HP + 7 LP", "Engine Dry Weight": "2,990 kg each (LEAP)", "Key Components": "Sharklet wingtips, composite nacelles", "Airframe Material": "Aluminum alloy + composite fairings"},
    "performance": {"MTOW": "79,000 kg (174,200 lb)", "T/W Ratio": "0.31", "Service Ceiling": "11,900 m (39,100 ft)", "Runway Required": "2,100 m (6,900 ft)", "Max Fuel": "26,730 L (7,062 US gal)", "Climb Rate": "630 m/min", "Approach Speed": "230 km/h (124 kt)", "Wing Loading": "640 kg/m2"}
}

detail_data["Embraer E195-E2"] = {
    "cabin": {"Cabin Length": "33.47 m", "Cabin Width": "2.74 m", "Seat Pitch (Econ)": "31-32 in", "Seat Pitch (Business)": "36-38 in", "Aisle Width": "Single aisle, 48 cm", "IFE System": "Wireless streaming (BYOD)", "Blind Spots": "Standard regional jet configuration", "Config Options": "1-class 146 / 2-class 120"},
    "airframe": {"Engine Model": "PW1919G (Geared Turbofan)", "Engine Type": "Geared turbofan", "Bypass Ratio": "12.5:1", "Compressor Stages": "3 LP + 8 HP", "Turbine Stages": "2 HP + 3 LP", "Engine Dry Weight": "2,857 kg each", "Key Components": "4th-gen swept wing, new landing gear", "Airframe Material": "Aluminum-lithium + composite empennage"},
    "performance": {"MTOW": "62,500 kg (137,800 lb)", "T/W Ratio": "0.33", "Service Ceiling": "12,500 m (41,000 ft)", "Runway Required": "1,970 m (6,463 ft)", "Max Fuel": "14,280 L (3,772 US gal)", "Climb Rate": "680 m/min", "Approach Speed": "225 km/h (121 kt)", "Wing Loading": "560 kg/m2"}
}

# FIGHTER JETS
detail_data["F-22 Raptor"] = {
    "cabin": {"Cockpit Type": "Single-seat, bubble canopy", "HUD System": "Kaiser AN/AVQ-34 wide-angle", "HMDS": "Not standard (HMD planned)", "Ejection Seat": "ACES II zero-zero", "Cockpit Displays": "6 LCD color MFDs", "Night Vision": "NVG-compatible lighting", "Oxygen System": "OBOGS (On-Board)", "Blind Spots": "Minimal — 360-degree canopy"},
    "airframe": {"Engine Model": "Pratt & Whitney F119-PW-100", "Engine Type": "Low-bypass afterburning turbofan", "Bypass Ratio": "0.30:1", "Compressor Stages": "3 fan + 6 HP", "Turbine Stages": "1 HP + 1 LP", "Engine Dry Weight": "1,800 kg each", "Key Components": "2D thrust-vectoring nozzles, radar-absorbent skin", "Airframe Material": "Titanium (39%) + composite (24%) + aluminum (16%)"},
    "performance": {"MTOW": "38,000 kg (83,500 lb)", "T/W Ratio": "1.08 (loaded)", "Service Ceiling": "19,812 m (65,000 ft)", "Runway Required": "914 m (3,000 ft)", "Max Fuel": "8,200 kg internal", "Climb Rate": ">315 m/s", "Approach Speed": "280 km/h (150 kt)", "Wing Loading": "375 kg/m2"}
}

detail_data["F-35 Lightning II"] = {
    "cabin": {"Cockpit Type": "Single-seat glass cockpit", "HUD System": "No HUD — uses helmet-mounted display", "HMDS": "AN/PVS-21 Gen III HMDS", "Ejection Seat": "Martin-Baker US16E", "Cockpit Displays": "20x8 in panoramic touchscreen", "Night Vision": "Integrated DAS (6 IR cameras)", "Oxygen System": "OBIGGS + OBOGS", "Blind Spots": "Zero — DAS provides 360° sphere"},
    "airframe": {"Engine Model": "Pratt & Whitney F135-PW-100/400/600", "Engine Type": "Low-bypass afterburning turbofan", "Bypass Ratio": "0.57:1", "Compressor Stages": "3 fan + 6 HP", "Turbine Stages": "1 HP + 2 LP", "Engine Dry Weight": "1,701 kg", "Key Components": "EOTS sensor, internal weapon bays, LO coatings", "Airframe Material": "Carbon fiber (35%) + titanium + aluminum"},
    "performance": {"MTOW": "31,751 kg (70,000 lb)", "T/W Ratio": "0.87 (loaded A-variant)", "Service Ceiling": "15,240 m (50,000 ft)", "Runway Required": "168 m (550 ft, STOVL B)", "Max Fuel": "8,382 kg (A-variant internal)", "Climb Rate": "254 m/s", "Approach Speed": "250 km/h (135 kt)", "Wing Loading": "526 kg/m2"}
}

detail_data["Su-57 Felon"] = {
    "cabin": {"Cockpit Type": "Single-seat tandem displays", "HUD System": "Wide-angle HUD + HMDS", "HMDS": "Sura helmet-mounted system", "Ejection Seat": "NPP Zvezda K-36D-5", "Cockpit Displays": "2 MFI-35 15-in LCDs + HUD", "Night Vision": "NVG-compatible cockpit", "Oxygen System": "OBOGS", "Blind Spots": "Rear hemisphere partially blocked"},
    "airframe": {"Engine Model": "Saturn AL-41F1 (interim) / Izdeliye 30 (final)", "Engine Type": "Low-bypass afterburning turbofan", "Bypass Ratio": "0.59:1", "Compressor Stages": "4 LP + 9 HP", "Turbine Stages": "1 HP + 1 LP", "Engine Dry Weight": "1,600 kg each", "Key Components": "3D TVC nozzles, internal bays, 101KS EO suite", "Airframe Material": "25% composite + titanium + aluminum"},
    "performance": {"MTOW": "35,000 kg (77,162 lb)", "T/W Ratio": "1.02 (loaded)", "Service Ceiling": "20,000 m (65,600 ft)", "Runway Required": "1,000 m (3,280 ft)", "Max Fuel": "10,300 kg internal", "Climb Rate": ">330 m/s", "Approach Speed": "265 km/h (143 kt)", "Wing Loading": "330 kg/m2"}
}

detail_data["Eurofighter Typhoon"] = {
    "cabin": {"Cockpit Type": "Single/twin-seat tandem", "HUD System": "BAE Wide-Angle HUD", "HMDS": "Striker II helmet display", "Ejection Seat": "Martin-Baker Mk.16A", "Cockpit Displays": "3 MHDDs + DASS panel", "Night Vision": "NVG + Striker II integrated", "Oxygen System": "OBOGS", "Blind Spots": "6 o'clock partially blocked by fin"},
    "airframe": {"Engine Model": "Eurojet EJ200", "Engine Type": "Low-bypass afterburning turbofan", "Bypass Ratio": "0.4:1", "Compressor Stages": "3 LP + 5 HP", "Turbine Stages": "1 HP + 1 LP", "Engine Dry Weight": "1,000 kg each", "Key Components": "Canard-delta, Captor-E AESA radar", "Airframe Material": "Carbon fiber (40%) + glass fiber + aluminum"},
    "performance": {"MTOW": "23,500 kg (51,809 lb)", "T/W Ratio": "1.15 (loaded)", "Service Ceiling": "19,812 m (65,000 ft)", "Runway Required": "700 m (2,300 ft)", "Max Fuel": "4,996 kg internal", "Climb Rate": ">315 m/s", "Approach Speed": "240 km/h (130 kt)", "Wing Loading": "311 kg/m2"}
}

detail_data["Dassault Rafale"] = {
    "cabin": {"Cockpit Type": "Single/twin-seat (B/C/M)", "HUD System": "Thales CTH 3022 wide-angle", "HMDS": "TopSight-I helmet system", "Ejection Seat": "Martin-Baker Mk.16F", "Cockpit Displays": "1 wide HMD + touchscreen MFD", "Night Vision": "NVG + Damocles pod", "Oxygen System": "OBOGS", "Blind Spots": "Canard creates minor lower-front occlusion"},
    "airframe": {"Engine Model": "Safran M88-2", "Engine Type": "Low-bypass afterburning turbofan", "Bypass Ratio": "0.30:1", "Compressor Stages": "3 LP + 6 HP", "Turbine Stages": "1 HP + 1 LP", "Engine Dry Weight": "897 kg each", "Key Components": "RBE2 AESA radar, SPECTRA EW suite, OSF", "Airframe Material": "Carbon fiber + Kevlar + aluminum-lithium"},
    "performance": {"MTOW": "24,500 kg (54,000 lb)", "T/W Ratio": "0.98 (loaded)", "Service Ceiling": "15,235 m (50,000 ft)", "Runway Required": "450 m (1,475 ft) with catapult", "Max Fuel": "4,700 kg internal", "Climb Rate": ">305 m/s", "Approach Speed": "230 km/h (124 kt)", "Wing Loading": "306 kg/m2"}
}

detail_data["F-16 Fighting Falcon"] = {
    "cabin": {"Cockpit Type": "Single-seat (C) / twin-seat (D)", "HUD System": "Lockheed Martin AN/AVQ-34", "HMDS": "JHMCS (Joint Helmet-Mounted Cueing)", "Ejection Seat": "ACES II zero-zero", "Cockpit Displays": "2 MFDs + center display (Block 70/72)", "Night Vision": "NVG + Sniper XR pod", "Oxygen System": "OBOGS (Block 50+)", "Blind Spots": "360° bubble canopy — minimal blind spots"},
    "airframe": {"Engine Model": "GE F110-GE-132 / PW F100-PW-229", "Engine Type": "Low-bypass afterburning turbofan", "Bypass Ratio": "0.76:1 (F110)", "Compressor Stages": "3 fan + 9 HP (F110)", "Turbine Stages": "1 HP + 2 LP", "Engine Dry Weight": "1,996 kg (F110)", "Key Components": "Fly-by-wire, blended wing-body, ventral fin", "Airframe Material": "Aluminum alloy + graphite epoxy composites"},
    "performance": {"MTOW": "21,772 kg (48,000 lb)", "T/W Ratio": "1.095 (loaded Block 50)", "Service Ceiling": "15,240 m (50,000 ft)", "Runway Required": "457 m (1,500 ft)", "Max Fuel": "3,175 kg internal", "Climb Rate": ">254 m/s", "Approach Speed": "230 km/h (124 kt)", "Wing Loading": "431 kg/m2"}
}

detail_data["F/A-18E/F Super Hornet"] = {
    "cabin": {"Cockpit Type": "Single-seat (E) / twin-seat (F)", "HUD System": "Kaiser AVQ-28(V) HUD", "HMDS": "JHMCS II (Joint Helmet-Mounted)", "Ejection Seat": "Martin-Baker SJU-17/A", "Cockpit Displays": "3 color MFDs + touchscreen (Block III)", "Night Vision": "NVG + ATFLIR pod", "Oxygen System": "OBOGS", "Blind Spots": "Slightly restricted rear by twin tails"},
    "airframe": {"Engine Model": "GE F414-GE-400", "Engine Type": "Low-bypass afterburning turbofan", "Bypass Ratio": "0.25:1", "Compressor Stages": "3 fan + 7 HP", "Turbine Stages": "1 HP + 1 LP", "Engine Dry Weight": "1,110 kg each", "Key Components": "AN/APG-79 AESA, conformal fuel tanks (Block III)", "Airframe Material": "Aluminum-lithium + carbon fiber composites"},
    "performance": {"MTOW": "29,937 kg (66,000 lb)", "T/W Ratio": "0.93 (loaded)", "Service Ceiling": "15,240 m (50,000 ft)", "Runway Required": "427 m (1,400 ft) catapult", "Max Fuel": "6,780 kg internal", "Climb Rate": ">254 m/s", "Approach Speed": "250 km/h (135 kt)", "Wing Loading": "459 kg/m2"}
}

detail_data["Chengdu J-20 Mighty Dragon"] = {
    "cabin": {"Cockpit Type": "Single-seat wide canopy", "HUD System": "Holographic wide-angle HUD", "HMDS": "Integrated HMDS (classified)", "Ejection Seat": "Martin-Baker derived zero-zero", "Cockpit Displays": "Large-area panoramic MFD", "Night Vision": "EOTS + EODAS (6 cameras)", "Oxygen System": "OBOGS", "Blind Spots": "Canard-delta creates minor low-front occlusion"},
    "airframe": {"Engine Model": "WS-10C (current) / WS-15 (planned)", "Engine Type": "Low-bypass afterburning turbofan", "Bypass Ratio": "0.57:1 (estimated)", "Compressor Stages": "3 fan + 9 HP", "Turbine Stages": "1 HP + 2 LP", "Engine Dry Weight": "1,850 kg each (estimated)", "Key Components": "DSI intakes, internal bays, KLJ-5 AESA radar", "Airframe Material": "Composite + RAM coatings + titanium"},
    "performance": {"MTOW": "~37,000 kg (81,571 lb)", "T/W Ratio": "~0.89 (loaded, WS-10C)", "Service Ceiling": "20,000 m (65,600 ft)", "Runway Required": "~700 m (2,300 ft)", "Max Fuel": "~11,100 kg internal", "Climb Rate": ">300 m/s (estimated)", "Approach Speed": "270 km/h (146 kt)", "Wing Loading": "340 kg/m2"}
}

# PRIVATE JETS
detail_data["Gulfstream G700"] = {
    "cabin": {"Cabin Length": "17.35 m (56.92 ft)", "Cabin Width": "2.49 m (8.17 ft)", "Cabin Height": "1.93 m (6.33 ft)", "Seat Config": "Up to 5 living areas", "IFE System": "Gulfstream Cabin Management System", "Blind Spots": "N/A — business jet", "Cabin Volume": "175.2 m3", "Features": "Master suite, shower, circadian lighting"},
    "airframe": {"Engine Model": "Rolls-Royce Pearl 700", "Engine Type": "High-bypass turbofan", "Bypass Ratio": "5.2:1", "Compressor Stages": "1 fan + 5 IP + 6 HP", "Turbine Stages": "2 HP + 3 LP", "Engine Dry Weight": "889 kg each", "Key Components": "Symmetry Flight Deck, active winglets", "Airframe Material": "Aluminum + advanced composites"},
    "performance": {"MTOW": "48,807 kg (107,600 lb)", "T/W Ratio": "0.38", "Service Ceiling": "15,545 m (51,000 ft)", "Runway Required": "1,875 m (6,250 ft)", "Max Fuel": "20,050 kg", "Climb Rate": "1,128 m/min", "Approach Speed": "215 km/h (116 kt)", "Wing Loading": "410 kg/m2"}
}

detail_data["Bombardier Global 7500"] = {
    "cabin": {"Cabin Length": "16.62 m (54.53 ft)", "Cabin Width": "2.44 m (8.0 ft)", "Cabin Height": "1.88 m (6.17 ft)", "Seat Config": "4 true cabin zones", "IFE System": "Bombardier nice HD CMS", "Blind Spots": "N/A — business jet", "Cabin Volume": "172.3 m3", "Features": "Pur Air system, full kitchen, crew rest"},
    "airframe": {"Engine Model": "GE Passport 20-19BB1A", "Engine Type": "High-bypass turbofan", "Bypass Ratio": "5.6:1", "Compressor Stages": "1 fan + 5 HP", "Turbine Stages": "2 HP + 3 LP", "Engine Dry Weight": "1,028 kg each", "Key Components": "Nu Wave wing, composite empennage", "Airframe Material": "Advanced composites + aluminum"},
    "performance": {"MTOW": "48,806 kg (107,600 lb)", "T/W Ratio": "0.36", "Service Ceiling": "15,545 m (51,000 ft)", "Runway Required": "1,768 m (5,800 ft)", "Max Fuel": "20,048 kg", "Climb Rate": "1,082 m/min", "Approach Speed": "220 km/h (119 kt)", "Wing Loading": "425 kg/m2"}
}

detail_data["Dassault Falcon 10X"] = {
    "cabin": {"Cabin Length": "16.5 m (54.1 ft)", "Cabin Width": "2.77 m (9.1 ft) widest ever", "Cabin Height": "2.03 m (6.67 ft)", "Seat Config": "Up to 4 zones + crew", "IFE System": "FalconCabin HD smart system", "Blind Spots": "N/A — business jet", "Cabin Volume": "78.7 m3", "Features": "Standing shower, pressurized to 3,000 ft"},
    "airframe": {"Engine Model": "Rolls-Royce Pearl 10X", "Engine Type": "High-bypass turbofan", "Bypass Ratio": "5.5:1", "Compressor Stages": "1 fan + 5 IP + 6 HP", "Turbine Stages": "2 HP + 3 LP", "Engine Dry Weight": "920 kg each", "Key Components": "FalconEye HUD, carbon fiber wing", "Airframe Material": "All-composite wing + aluminum fuselage"},
    "performance": {"MTOW": "47,400 kg (104,500 lb)", "T/W Ratio": "0.36", "Service Ceiling": "15,545 m (51,000 ft)", "Runway Required": "1,820 m (5,970 ft)", "Max Fuel": "18,800 kg", "Climb Rate": "1,100 m/min", "Approach Speed": "210 km/h (113 kt)", "Wing Loading": "400 kg/m2"}
}

detail_data["Cessna Citation Longitude"] = {
    "cabin": {"Cabin Length": "7.62 m (25.0 ft)", "Cabin Width": "1.93 m (6.33 ft)", "Cabin Height": "1.83 m (6.0 ft)", "Seat Config": "Up to 12 passengers", "IFE System": "Garmin G5000 integrated", "Blind Spots": "N/A — business jet", "Cabin Volume": "37.0 m3", "Features": "Flat floor, full refreshment center"},
    "airframe": {"Engine Model": "Honeywell HTF7700L", "Engine Type": "High-bypass turbofan", "Bypass Ratio": "4.4:1", "Compressor Stages": "1 fan + 5 HP", "Turbine Stages": "2 HP + 3 LP", "Engine Dry Weight": "499 kg each", "Key Components": "Garmin G5000 touchscreen avionics", "Airframe Material": "Aluminum + composite empennage"},
    "performance": {"MTOW": "17,917 kg (39,500 lb)", "T/W Ratio": "0.41", "Service Ceiling": "13,716 m (45,000 ft)", "Runway Required": "1,091 m (3,580 ft)", "Max Fuel": "6,108 kg", "Climb Rate": "1,006 m/min", "Approach Speed": "195 km/h (105 kt)", "Wing Loading": "350 kg/m2"}
}

# CARGO
detail_data["Antonov An-225 Mriya"] = {
    "cabin": {"Cargo Bay Length": "43.35 m (142.2 ft)", "Cargo Bay Width": "6.4 m (21.0 ft)", "Cargo Bay Height": "4.4 m (14.4 ft)", "Cargo Volume": "1,300 m3", "Loading System": "Front visor nose door", "IFE System": "N/A — cargo", "Blind Spots": "Massive forward blind zone", "Config Options": "Cargo only — no passenger variant"},
    "airframe": {"Engine Model": "ZMKB Progress D-18T", "Engine Type": "High-bypass turbofan", "Bypass Ratio": "5.7:1", "Compressor Stages": "7 LP + 7 HP", "Turbine Stages": "1 HP + 4 LP", "Engine Dry Weight": "4,100 kg each", "Key Components": "6 engines, twin tail, external payload mount", "Airframe Material": "Aluminum alloy + titanium critical structures"},
    "performance": {"MTOW": "640,000 kg (1,411,000 lb)", "T/W Ratio": "0.23", "Service Ceiling": "11,000 m (36,100 ft)", "Runway Required": "3,500 m (11,500 ft)", "Max Fuel": "300,000 kg", "Climb Rate": "360 m/min", "Approach Speed": "275 km/h (148 kt)", "Wing Loading": "662 kg/m2"}
}

detail_data["Boeing 747-8 Freighter"] = {
    "cabin": {"Cargo Bay Length": "41.0 m (main) + 14.4 m (lower)", "Cargo Bay Width": "6.1 m (main deck)", "Cargo Bay Height": "3.04 m (main deck)", "Cargo Volume": "858 m3", "Loading System": "Nose door + side cargo door", "IFE System": "N/A — cargo", "Blind Spots": "Large forward area below nose", "Config Options": "Full freighter / Combi variant"},
    "airframe": {"Engine Model": "GEnx-2B67", "Engine Type": "High-bypass turbofan", "Bypass Ratio": "8.0:1", "Compressor Stages": "4 LP + 10 HP", "Turbine Stages": "2 HP + 7 LP", "Engine Dry Weight": "5,622 kg each", "Key Components": "Nose-loading door, pallet conveyor system", "Airframe Material": "Aluminum alloy + composite fairings"},
    "performance": {"MTOW": "447,696 kg (987,000 lb)", "T/W Ratio": "0.27", "Service Ceiling": "13,100 m (43,000 ft)", "Runway Required": "3,050 m (10,000 ft)", "Max Fuel": "216,840 L (57,285 US gal)", "Climb Rate": "490 m/min", "Approach Speed": "260 km/h (140 kt)", "Wing Loading": "730 kg/m2"}
}

detail_data["Airbus BelugaXL"] = {
    "cabin": {"Cargo Bay Length": "Unknown (classified Airbus logistics)", "Cargo Bay Width": "7.10 m (internal)", "Cargo Bay Height": "6.70 m (internal)", "Cargo Volume": "2,209 m3", "Loading System": "Upper-fuselage hinged nose door", "IFE System": "N/A — cargo", "Blind Spots": "Massive nose area when open", "Config Options": "Specialized Airbus component transport only"},
    "airframe": {"Engine Model": "GE CF6-80E1A4", "Engine Type": "High-bypass turbofan", "Bypass Ratio": "5.1:1", "Compressor Stages": "1 fan + 14 HP", "Turbine Stages": "2 HP + 5 LP", "Engine Dry Weight": "4,290 kg each", "Key Components": "Lowered cockpit, whale-shaped upper fuselage", "Airframe Material": "Aluminum alloy (A330 derived structure)"},
    "performance": {"MTOW": "227,000 kg (500,400 lb)", "T/W Ratio": "0.24", "Service Ceiling": "10,700 m (35,100 ft)", "Runway Required": "2,700 m (8,860 ft)", "Max Fuel": "139,090 L", "Climb Rate": "400 m/min", "Approach Speed": "255 km/h (138 kt)", "Wing Loading": "590 kg/m2"}
}

detail_data["Lockheed C-5M Super Galaxy"] = {
    "cabin": {"Cargo Bay Length": "36.91 m (121.1 ft)", "Cargo Bay Width": "5.79 m (19.0 ft)", "Cargo Bay Height": "4.11 m (13.5 ft)", "Cargo Volume": "876 m3", "Loading System": "Nose visor + aft ramp (drive-through)", "IFE System": "N/A — military cargo", "Blind Spots": "Large T-tail area, nose below", "Config Options": "Cargo only — 36 pallets / 2 M1 tanks"},
    "airframe": {"Engine Model": "GE CF6-80C2L1F", "Engine Type": "High-bypass turbofan", "Bypass Ratio": "5.1:1", "Compressor Stages": "1 fan + 14 HP", "Turbine Stages": "2 HP + 5 LP", "Engine Dry Weight": "4,290 kg each", "Key Components": "Kneeling landing gear, drive-through loading", "Airframe Material": "Aluminum alloy + titanium substructure"},
    "performance": {"MTOW": "381,018 kg (840,000 lb)", "T/W Ratio": "0.22", "Service Ceiling": "10,895 m (35,745 ft)", "Runway Required": "2,530 m (8,300 ft)", "Max Fuel": "150,820 L", "Climb Rate": "520 m/min", "Approach Speed": "265 km/h (143 kt)", "Wing Loading": "610 kg/m2"}
}

# MILITARY TRANSPORT
detail_data["Boeing C-17 Globemaster III"] = {
    "cabin": {"Cargo Bay Length": "26.82 m (88.0 ft)", "Cargo Bay Width": "5.49 m (18.0 ft)", "Cargo Bay Height": "3.76 m (12.3 ft)", "Cargo Volume": "592 m3", "Loading System": "Rear ramp + airdrop capable", "IFE System": "N/A — military", "Blind Spots": "T-tail area, rear below ramp", "Config Options": "18 pallets / 1 M1 tank / 102 paratroopers"},
    "airframe": {"Engine Model": "Pratt & Whitney F117-PW-100", "Engine Type": "High-bypass turbofan (PW2040 military)", "Bypass Ratio": "6.0:1", "Compressor Stages": "1 fan + 12 HP", "Turbine Stages": "2 HP + 5 LP", "Engine Dry Weight": "3,311 kg each", "Key Components": "Externally blown flap STOL system", "Airframe Material": "Aluminum alloy + composite empennage"},
    "performance": {"MTOW": "265,350 kg (585,000 lb)", "T/W Ratio": "0.25", "Service Ceiling": "13,716 m (45,000 ft)", "Runway Required": "1,064 m (3,500 ft) tactical", "Max Fuel": "134,556 L", "Climb Rate": "580 m/min", "Approach Speed": "240 km/h (130 kt)", "Wing Loading": "540 kg/m2"}
}

detail_data["Lockheed C-130J Super Hercules"] = {
    "cabin": {"Cargo Bay Length": "12.31 m (40.4 ft)", "Cargo Bay Width": "3.12 m (10.3 ft)", "Cargo Bay Height": "2.74 m (9.0 ft)", "Cargo Volume": "131.6 m3", "Loading System": "Rear ramp + paradrop door", "IFE System": "N/A — military", "Blind Spots": "Under nose, behind empennage", "Config Options": "6 pallets / 92 troops / 64 paratroopers"},
    "airframe": {"Engine Model": "Rolls-Royce AE2100D3", "Engine Type": "Turboprop", "Propeller": "Dowty R391 6-blade composite", "Compressor Stages": "14-stage axial compressor", "Turbine Stages": "2 HP + 2 power", "Engine Dry Weight": "745 kg each", "Key Components": "Digital avionics, NP2000 prop, LAIRCM", "Airframe Material": "Aluminum alloy + composite center wing box"},
    "performance": {"MTOW": "79,378 kg (175,000 lb)", "T/W Ratio": "0.28", "Service Ceiling": "8,615 m (28,000 ft)", "Runway Required": "1,093 m (3,586 ft)", "Max Fuel": "20,820 kg", "Climb Rate": "580 m/min", "Approach Speed": "200 km/h (108 kt)", "Wing Loading": "350 kg/m2"}
}

detail_data["Airbus A400M Atlas"] = {
    "cabin": {"Cargo Bay Length": "17.71 m (58.1 ft)", "Cargo Bay Width": "4.0 m (13.1 ft)", "Cargo Bay Height": "3.85 m (12.6 ft)", "Cargo Volume": "340 m3", "Loading System": "Rear ramp + paradrop side doors", "IFE System": "N/A — military", "Blind Spots": "Under nose, empennage area", "Config Options": "9 pallets / 116 troops / 2 APCs"},
    "airframe": {"Engine Model": "Europrop TP400-D6", "Engine Type": "Turboprop (most powerful Western)", "Propeller": "Ratier-Figeac FH386 8-blade", "Compressor Stages": "5 LP + 6 HP axial", "Turbine Stages": "1 HP + 1 LP + 3 power", "Engine Dry Weight": "1,854 kg each", "Key Components": "FBW flight controls, aerial refueling boom", "Airframe Material": "Composite + aluminum alloy fuselage"},
    "performance": {"MTOW": "141,000 kg (310,852 lb)", "T/W Ratio": "0.26", "Service Ceiling": "11,300 m (37,000 ft)", "Runway Required": "980 m (3,215 ft) tactical", "Max Fuel": "50,500 kg", "Climb Rate": "600 m/min", "Approach Speed": "225 km/h (121 kt)", "Wing Loading": "450 kg/m2"}
}

detail_data["Bell Boeing V-22 Osprey"] = {
    "cabin": {"Cargo Bay Length": "7.37 m (24.2 ft)", "Cargo Bay Width": "1.83 m (6.0 ft)", "Cargo Bay Height": "1.68 m (5.5 ft)", "Cargo Volume": "24.3 m3", "Loading System": "Rear ramp + belly hook", "IFE System": "N/A — military", "Blind Spots": "Large engine nacelles block lateral view", "Config Options": "24 troops / 12 litters / 10,000 lb cargo"},
    "airframe": {"Engine Model": "Rolls-Royce T406-AD-400 (AE1107C)", "Engine Type": "Turboshaft (drives proprotors)", "Power Output": "4,586 kW (6,150 shp) each", "Compressor Stages": "14-stage axial", "Turbine Stages": "2 HP + 2 power", "Engine Dry Weight": "441 kg each", "Key Components": "Tilt nacelles, interconnect driveshaft (OEI)", "Airframe Material": "Graphite-epoxy composite (43%) + aluminum"},
    "performance": {"MTOW": "27,442 kg (60,500 lb)", "T/W Ratio": "N/A (rotorcraft)", "Service Ceiling": "7,620 m (25,000 ft)", "Runway Required": "0 m (VTOL capable)", "Max Fuel": "6,513 kg", "Climb Rate": "686 m/min", "Approach Speed": "185 km/h (100 kt)", "Disc Loading": "129 kg/m2"}
}

# TRAINERS
detail_data["BAE Hawk T.2"] = {
    "cabin": {"Cockpit Type": "Tandem two-seat", "HUD System": "BAE Wide-Angle HUD", "HMDS": "Not standard", "Ejection Seat": "Martin-Baker Mk.16L", "Cockpit Displays": "3 color MFDs + HUD", "Night Vision": "NVG-compatible", "Oxygen System": "LOX (liquid oxygen)", "Blind Spots": "Rear seat slightly restricted forward"},
    "airframe": {"Engine Model": "Rolls-Royce Adour Mk 951", "Engine Type": "Low-bypass turbofan (non-afterburning)", "Bypass Ratio": "0.75:1", "Compressor Stages": "2 LP + 5 HP", "Turbine Stages": "1 HP + 1 LP", "Engine Dry Weight": "580 kg", "Key Components": "Robust airframe for +8g, wing hardpoints", "Airframe Material": "Aluminum alloy + composite fairings"},
    "performance": {"MTOW": "9,100 kg (20,062 lb)", "T/W Ratio": "0.63", "Service Ceiling": "15,240 m (50,000 ft)", "Runway Required": "600 m (1,970 ft)", "Max Fuel": "1,361 kg", "Climb Rate": "2,640 m/min", "Approach Speed": "195 km/h (105 kt)", "Wing Loading": "370 kg/m2"}
}

detail_data["Beechcraft T-6 Texan II"] = {
    "cabin": {"Cockpit Type": "Tandem two-seat pressurized", "HUD System": "Optional HUD", "HMDS": "Not equipped", "Ejection Seat": "Martin-Baker US16LA", "Cockpit Displays": "2 MFDs + standby instruments", "Night Vision": "NVG-compatible", "Oxygen System": "OBOGS", "Blind Spots": "Canopy arch limits top-rear view"},
    "airframe": {"Engine Model": "Pratt & Whitney Canada PT6A-68", "Engine Type": "Free turbine turboprop", "Power Output": "820 kW (1,100 shp)", "Propeller": "Hartzell 4-blade constant speed", "Turbine Stages": "1 compressor + 1 power", "Engine Dry Weight": "215 kg", "Key Components": "Pressurized cockpit, HOTAS controls", "Airframe Material": "Aluminum alloy + composite cowling"},
    "performance": {"MTOW": "3,311 kg (7,300 lb)", "T/W Ratio": "0.34", "Service Ceiling": "9,449 m (31,000 ft)", "Runway Required": "536 m (1,758 ft)", "Max Fuel": "564 kg", "Climb Rate": "1,036 m/min", "Approach Speed": "170 km/h (92 kt)", "Wing Loading": "240 kg/m2"}
}

detail_data["Pilatus PC-21"] = {
    "cabin": {"Cockpit Type": "Tandem two-seat", "HUD System": "Elbit HUD (optional)", "HMDS": "Embedded simulation HMDS option", "Ejection Seat": "Martin-Baker Mk.16 (CH16)", "Cockpit Displays": "3 large MFDs + mission computer", "Night Vision": "NVG-compatible", "Oxygen System": "OBOGS", "Blind Spots": "Standard tandem — rear seat restricted"},
    "airframe": {"Engine Model": "Pratt & Whitney Canada PT6A-68B", "Engine Type": "Free turbine turboprop", "Power Output": "1,193 kW (1,600 shp)", "Propeller": "5-blade composite constant-speed", "Turbine Stages": "1 CT + 1 PT", "Engine Dry Weight": "224 kg", "Key Components": "Embedded tactical simulation, data link", "Airframe Material": "Aluminum alloy + carbon fiber composites"},
    "performance": {"MTOW": "4,250 kg (9,370 lb)", "T/W Ratio": "0.38", "Service Ceiling": "11,582 m (38,000 ft)", "Runway Required": "690 m (2,264 ft)", "Max Fuel": "680 kg", "Climb Rate": "1,220 m/min", "Approach Speed": "175 km/h (95 kt)", "Wing Loading": "260 kg/m2"}
}

detail_data["KAI T-50 Golden Eagle"] = {
    "cabin": {"Cockpit Type": "Tandem two-seat (single in FA-50)", "HUD System": "BAE Systems wide-angle HUD", "HMDS": "JHMCS option", "Ejection Seat": "Martin-Baker Mk.16K", "Cockpit Displays": "2 MFDs + UFC + HUD", "Night Vision": "NVG + targeting pod (FA-50)", "Oxygen System": "OBOGS", "Blind Spots": "Twin tail slightly restricts 6 o'clock"},
    "airframe": {"Engine Model": "GE F404-GE-102", "Engine Type": "Low-bypass afterburning turbofan", "Bypass Ratio": "0.34:1", "Compressor Stages": "3 fan + 7 HP", "Turbine Stages": "1 HP + 1 LP", "Engine Dry Weight": "1,036 kg", "Key Components": "F-16 derived FBW, EL/M-2032 radar (FA-50)", "Airframe Material": "Aluminum alloy + carbon fiber composites"},
    "performance": {"MTOW": "12,300 kg (27,100 lb)", "T/W Ratio": "0.85 (clean)", "Service Ceiling": "14,630 m (48,000 ft)", "Runway Required": "500 m (1,640 ft)", "Max Fuel": "2,490 kg internal", "Climb Rate": "3,900 m/min", "Approach Speed": "240 km/h (130 kt)", "Wing Loading": "370 kg/m2"}
}

# HELICOPTERS
detail_data["AH-64E Apache Guardian"] = {
    "cabin": {"Cockpit Type": "Tandem two-seat (CPG front, pilot rear)", "HUD System": "IHADSS helmet-mounted monocle", "HMDS": "Integrated Helmet & Display Sight", "Ejection Seat": "N/A — crash-resistant seats", "Cockpit Displays": "2 MFDs per cockpit (4 total)", "Night Vision": "TADS/PNVS (FLIR + DTV)", "Oxygen System": "N/A (low altitude ops)", "Blind Spots": "Below + directly behind tail boom"},
    "airframe": {"Engine Model": "GE T700-GE-701D", "Engine Type": "Turboshaft", "Power Output": "1,490 kW (2,000 shp) each", "Compressor Stages": "5 axial + 1 centrifugal", "Turbine Stages": "2 gas gen + 2 power", "Engine Dry Weight": "204 kg each", "Key Components": "Longbow FCR, 30mm M230 chain gun", "Airframe Material": "Kevlar + boron + graphite composites"},
    "performance": {"MTOW": "10,433 kg (23,000 lb)", "T/W Ratio": "N/A (rotorcraft)", "Service Ceiling": "6,400 m (21,000 ft)", "Runway Required": "0 m (VTOL)", "Max Fuel": "1,421 L", "Climb Rate": "762 m/min", "Approach Speed": "N/A (hover capable)", "Max VNE": "293 km/h (158 kt)"}
}

detail_data["UH-60M Black Hawk"] = {
    "cabin": {"Cargo Bay Length": "3.68 m (12.1 ft)", "Cargo Bay Width": "2.21 m (7.25 ft)", "Cargo Bay Height": "1.37 m (4.5 ft)", "Seat Config": "11 troops + 3 crew", "Loading System": "Side sliding doors + external hook", "IFE System": "N/A — military", "Blind Spots": "Below tail boom + behind empennage", "Config Options": "Assault / medevac (4 litters) / VIP"},
    "airframe": {"Engine Model": "GE T700-GE-701D", "Engine Type": "Turboshaft", "Power Output": "1,410 kW (1,890 shp) each", "Compressor Stages": "5 axial + 1 centrifugal", "Turbine Stages": "2 gas gen + 2 power", "Engine Dry Weight": "204 kg each", "Key Components": "Ballistic-tolerant fuel system, crashworthy seats", "Airframe Material": "Aluminum + composite panels + Nomex"},
    "performance": {"MTOW": "10,660 kg (23,500 lb)", "T/W Ratio": "N/A (rotorcraft)", "Service Ceiling": "5,790 m (19,000 ft)", "Runway Required": "0 m (VTOL)", "Max Fuel": "1,362 L (internal)", "Climb Rate": "472 m/min", "Approach Speed": "N/A (hover capable)", "Max VNE": "294 km/h (159 kt)"}
}

detail_data["Mi-24 Hind"] = {
    "cabin": {"Cargo Bay Length": "2.62 m (8.6 ft) troop cabin", "Cargo Bay Width": "1.5 m (4.9 ft)", "Seat Config": "8 troops in center cabin", "Cockpit Type": "Tandem stepped (gunner/pilot)", "Loading System": "Side doors for troops", "IFE System": "N/A — military", "Blind Spots": "Below and behind main rotor hub", "Config Options": "Attack / transport / medevac"},
    "airframe": {"Engine Model": "Isotov TV3-117VMA", "Engine Type": "Turboshaft", "Power Output": "1,640 kW (2,200 shp) each", "Compressor Stages": "12-stage axial", "Turbine Stages": "2 gas gen + 2 power", "Engine Dry Weight": "285 kg each", "Key Components": "Titanium rotor head, stub wings for weapons", "Airframe Material": "Aluminum alloy + armored cockpit tub"},
    "performance": {"MTOW": "12,000 kg (26,455 lb)", "T/W Ratio": "N/A (rotorcraft)", "Service Ceiling": "4,500 m (14,750 ft)", "Runway Required": "0 m (VTOL) / short run preferred", "Max Fuel": "1,500 L (internal)", "Climb Rate": "750 m/min", "Approach Speed": "N/A (hover capable)", "Max VNE": "335 km/h (181 kt)"}
}

detail_data["CH-47F Chinook"] = {
    "cabin": {"Cargo Bay Length": "9.20 m (30.2 ft)", "Cargo Bay Width": "2.31 m (7.58 ft)", "Cargo Bay Height": "1.98 m (6.5 ft)", "Seat Config": "33-55 troops", "Loading System": "Rear ramp + 3 external hooks", "IFE System": "N/A — military", "Blind Spots": "Between tandem rotor discs", "Config Options": "Troop / cargo / sling load / medevac 24 litters"},
    "airframe": {"Engine Model": "Honeywell T55-GA-714A", "Engine Type": "Turboshaft", "Power Output": "3,529 kW (4,733 shp) each", "Compressor Stages": "14-stage axial + 1 centrifugal", "Turbine Stages": "2 gas gen + 2 power", "Engine Dry Weight": "379 kg each", "Key Components": "Tandem rotor system, digital AFCS", "Airframe Material": "Aluminum + fiberglass + Kevlar panels"},
    "performance": {"MTOW": "22,680 kg (50,000 lb)", "T/W Ratio": "N/A (rotorcraft)", "Service Ceiling": "5,640 m (18,500 ft)", "Runway Required": "0 m (VTOL)", "Max Fuel": "3,899 L (internal)", "Climb Rate": "561 m/min", "Approach Speed": "N/A (hover capable)", "Max VNE": "315 km/h (170 kt)"}
}

detail_data["Airbus H145"] = {
    "cabin": {"Cabin Length": "3.60 m (11.8 ft)", "Cabin Width": "1.58 m (5.2 ft)", "Cabin Height": "1.30 m (4.3 ft)", "Seat Config": "Up to 10 passengers", "Loading System": "Sliding doors + rear clamshell", "IFE System": "N/A — utility helicopter", "Blind Spots": "Below tail boom / Fenestron area", "Config Options": "EMS / police / corporate / training"},
    "airframe": {"Engine Model": "Safran Arriel 2E", "Engine Type": "Turboshaft (FADEC)", "Power Output": "574 kW (770 shp) each", "Compressor Stages": "1 axial + 1 centrifugal", "Turbine Stages": "1 gas gen + 1 power", "Engine Dry Weight": "112 kg each", "Key Components": "Fenestron shrouded tail rotor, Helionix avionics", "Airframe Material": "Composite + aluminum fuselage"},
    "performance": {"MTOW": "3,800 kg (8,377 lb)", "T/W Ratio": "N/A (rotorcraft)", "Service Ceiling": "5,485 m (18,000 ft)", "Runway Required": "0 m (VTOL)", "Max Fuel": "879 L", "Climb Rate": "488 m/min", "Approach Speed": "N/A (hover capable)", "Max VNE": "267 km/h (144 kt)"}
}

# SEAPLANES
detail_data["Canadair CL-415 SuperScooper"] = {
    "cabin": {"Cargo Bay Type": "Water tank system", "Tank Capacity": "6,137 L (1,621 US gal)", "Cockpit Type": "Side-by-side two-seat", "Scoop Probes": "2 retractable hull probes", "Loading System": "Water scoop from lakes/ocean", "IFE System": "N/A — firefighting aircraft", "Blind Spots": "Below hull + aft fuselage", "Config Options": "Firefighting / SAR / maritime patrol"},
    "airframe": {"Engine Model": "Pratt & Whitney Canada PW123AF", "Engine Type": "Turboprop", "Power Output": "1,775 kW (2,380 shp) each", "Propeller": "Hamilton Std 14SF-23 4-blade", "Turbine Stages": "2 centrifugal + 1 power", "Engine Dry Weight": "465 kg each", "Key Components": "Retractable scoop probes, corrosion-resistant hull", "Airframe Material": "Aluminum alloy (marine-grade anticorrosion)"},
    "performance": {"MTOW": "19,890 kg (43,850 lb)", "T/W Ratio": "0.24", "Service Ceiling": "4,480 m (14,700 ft)", "Runway Required": "800 m water (2,625 ft)", "Max Fuel": "5,680 L", "Climb Rate": "408 m/min", "Approach Speed": "155 km/h (84 kt)", "Water Scoop Distance": "1,340 m at 130 km/h"}
}

detail_data["ShinMaywa US-2"] = {
    "cabin": {"Cabin Type": "Rescue/utility cabin", "Rescue Capacity": "20 survivors", "Cockpit Type": "Side-by-side multi-crew (11 total)", "Rescue Equipment": "Life rafts, hoist, medical bay", "Loading System": "Side hatches + rear door", "IFE System": "N/A — SAR aircraft", "Blind Spots": "Below hull, engine nacelle zones", "Config Options": "SAR / maritime patrol / transport"},
    "airframe": {"Engine Model": "Rolls-Royce AE2100J", "Engine Type": "Turboprop", "Power Output": "3,424 kW (4,591 shp) each", "Propeller": "Dowty R391 6-blade", "Turbine Stages": "14-stage axial + 2 power", "Engine Dry Weight": "745 kg each", "Key Components": "BLC (Boundary Layer Control), spray suppressor", "Airframe Material": "Aluminum alloy + corrosion-resistant coatings"},
    "performance": {"MTOW": "47,700 kg (105,160 lb)", "T/W Ratio": "0.29", "Service Ceiling": "7,195 m (23,600 ft)", "Runway Required": "490 m water (1,600 ft)", "Max Fuel": "20,000 L", "Climb Rate": "610 m/min", "Approach Speed": "185 km/h (100 kt)", "Min Water Takeoff Speed": "90 km/h (49 kt)"}
}

detail_data["AVIC AG600 Kunlong"] = {
    "cabin": {"Cabin Type": "Firefighting / rescue cabin", "Tank Capacity": "12,000 L (3,170 US gal)", "Cockpit Type": "Side-by-side multi-crew", "Rescue Capacity": "50 survivors", "Loading System": "Water scoop + hull doors", "IFE System": "N/A — firefighting/SAR", "Blind Spots": "Below hull, engine nacelle areas", "Config Options": "Firefighting / SAR / maritime patrol"},
    "airframe": {"Engine Model": "WJ-6 (domestic turboprop)", "Engine Type": "Turboprop", "Power Output": "3,126 kW (4,192 shp) each", "Propeller": "6-blade constant speed", "Turbine Stages": "10-stage axial + 2 power", "Engine Dry Weight": "1,050 kg each", "Key Components": "T-tail, retractable landing gear, hull boat design", "Airframe Material": "Aluminum alloy + composite fairings"},
    "performance": {"MTOW": "60,000 kg (132,277 lb)", "T/W Ratio": "0.21", "Service Ceiling": "6,000 m (19,685 ft)", "Runway Required": "1,500 m water", "Max Fuel": "18,000 L", "Climb Rate": "480 m/min", "Approach Speed": "195 km/h (105 kt)", "Water Scoop Distance": "1,500 m at 150 km/h"}
}

detail_data["de Havilland DHC-6 Twin Otter (Floats)"] = {
    "cabin": {"Cabin Length": "5.94 m (19.5 ft)", "Cabin Width": "1.60 m (5.25 ft)", "Cabin Height": "1.50 m (4.9 ft)", "Seat Config": "Up to 19 passengers", "Loading System": "Large cargo door + nose baggage", "IFE System": "N/A — bush plane", "Blind Spots": "High wing blocks upward view", "Config Options": "Wheels / skis / amphibious floats"},
    "airframe": {"Engine Model": "Pratt & Whitney Canada PT6A-34", "Engine Type": "Free turbine turboprop", "Power Output": "462 kW (620 shp) each", "Propeller": "Hartzell HC-B3TN 3-blade", "Turbine Stages": "3 axial + 1 centrifugal CT + 1 PT", "Engine Dry Weight": "153 kg each", "Key Components": "Fixed leading-edge slats, double-slotted flaps", "Airframe Material": "Aluminum alloy + fabric control surfaces"},
    "performance": {"MTOW": "5,670 kg (12,500 lb)", "T/W Ratio": "0.22", "Service Ceiling": "7,620 m (25,000 ft)", "Runway Required": "366 m (1,200 ft) land / 500 m water", "Max Fuel": "1,136 L", "Climb Rate": "490 m/min", "Approach Speed": "130 km/h (70 kt)", "Stall Speed": "100 km/h (54 kt)"}
}

# 4. Now inject the JS data + modal logic
detail_json = json.dumps(detail_data, indent=2)

modal_js = f"""
// ============ DETAIL MODAL DATA ============
const detailData = {detail_json};

function openModal(planeName, tab) {{
  const data = detailData[planeName];
  if (!data) {{
    document.getElementById('modalContent').innerHTML = '<p style="color:#8a9bb8;">Detailed data coming soon for ' + planeName + '</p>';
    showModal();
    return;
  }}

  let tabData, tabTitle, tabIcon;
  if (tab === 'cabin') {{
    tabData = data.cabin;
    tabTitle = 'Cabin & Passenger Experience';
    tabIcon = '🛩️';
  }} else if (tab === 'airframe') {{
    tabData = data.airframe;
    tabTitle = 'Airframe History & Engine Details';
    tabIcon = '⚙️';
  }} else {{
    tabData = data.performance;
    tabTitle = 'Operational Performance & Load Specs';
    tabIcon = '📊';
  }}

  let gridHTML = Object.entries(tabData).map(([k,v]) => `
    <div class="modal-item">
      <div class="m-label">${{k}}</div>
      <div class="m-value">${{v}}</div>
    </div>
  `).join('');

  document.getElementById('modalContent').innerHTML = `
    <div class="modal-title">${{tabIcon}} ${{planeName}}</div>
    <div class="modal-subtitle">${{tabTitle}}</div>
    <div class="modal-grid">${{gridHTML}}</div>
  `;
  showModal();
}}

function showModal() {{
  const m = document.getElementById('infoModal');
  m.style.display = 'flex';
  setTimeout(() => m.classList.add('active'), 10);
}}

document.getElementById('modalClose').addEventListener('click', () => {{
  const m = document.getElementById('infoModal');
  m.classList.remove('active');
  setTimeout(() => m.style.display = 'none', 300);
}});

document.getElementById('infoModal').addEventListener('click', (e) => {{
  if (e.target === e.currentTarget) {{
    const m = document.getElementById('infoModal');
    m.classList.remove('active');
    setTimeout(() => m.style.display = 'none', 300);
  }}
}});
"""

# Insert the modal JS before the closing </script> tag
content = content.replace('</script>', modal_js + '\n</script>')

# 5. Update the createCard function to add buttons below the card
# We need to wrap the flashcard + buttons in a container
old_card_class = "card.className = 'flashcard reveal';"
new_card_class = """card.className = 'flashcard-wrapper reveal';
  const fc = document.createElement('div');
  fc.className = 'flashcard';"""

content = content.replace(old_card_class, new_card_class)

# Replace the card.innerHTML with fc.innerHTML
content = content.replace("card.innerHTML = `", "fc.innerHTML = `")

# Replace the click listener and return
old_end = """card.addEventListener('click', () => card.classList.toggle('flipped'));
  return card;"""
new_end = """fc.addEventListener('click', () => fc.classList.toggle('flipped'));

  // Add info buttons below card
  const btnContainer = document.createElement('div');
  btnContainer.className = 'card-buttons';
  btnContainer.innerHTML = `
    <button class="info-btn" onclick="event.stopPropagation(); openModal('${plane.name}', 'cabin')">
      <span class="btn-icon">🛩️</span>Cabin & Pax Experience
    </button>
    <button class="info-btn" onclick="event.stopPropagation(); openModal('${plane.name}', 'airframe')">
      <span class="btn-icon">⚙️</span>Airframe & Engine
    </button>
    <button class="info-btn" onclick="event.stopPropagation(); openModal('${plane.name}', 'performance')">
      <span class="btn-icon">📊</span>Performance & Load
    </button>
  `;

  card.appendChild(fc);
  card.appendChild(btnContainer);
  return card;"""

content = content.replace(old_end, new_end)

# Add CSS for wrapper
wrapper_css = """
    .flashcard-wrapper {
      display: flex; flex-direction: column;
    }
    .flashcard-wrapper .flashcard {
      flex: 1;
    }
"""
content = content.replace('/* ===== FLASHCARD ===== */', wrapper_css + '\n    /* ===== FLASHCARD ===== */')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done! Added 3 info buttons + modal for ALL 40 planes with full aviation data.")
