import re
import json

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix scrolling on flashcard-back - make height bigger and ensure overflow-y works
content = content.replace(
    'height: 520px;',
    'height: 620px;'
)

# Fix the back card to scroll properly - the ::before pseudo-element can block scroll
old_back_before = """.flashcard-back::before {
      content: ''; position: absolute; inset: 0; pointer-events: none;
      background-image: radial-gradient(rgba(0,212,255,0.15) 1px, transparent 1px);
      background-size: 20px 20px; opacity: 0.5;
    }"""
new_back_before = """.flashcard-back::before {
      content: ''; position: absolute; top: 0; left: 0; right: 0; height: 100%;
      pointer-events: none; z-index: 0;
      background-image: radial-gradient(rgba(0,212,255,0.15) 1px, transparent 1px);
      background-size: 20px 20px; opacity: 0.3;
    }"""
content = content.replace(old_back_before, new_back_before)

# Also fix the responsive 600px flashcard height
content = content.replace(
    '.flashcard { height: 560px; }',
    '.flashcard { height: 640px; }'
)

# 2. Add pros/cons CSS
pros_cons_css = """
    .pros-cons { position: relative; z-index: 2; margin-top: 0.8rem; }
    .pros-cons h4 {
      font-family: 'Rajdhani', sans-serif; font-size: .8rem; font-weight: 700;
      text-transform: uppercase; letter-spacing: 2px; margin-bottom: .4rem;
    }
    .pros-cons .pros h4 { color: #00ff88; }
    .pros-cons .cons h4 { color: #ff4466; }
    .pros-cons ul {
      list-style: none; padding: 0; margin: 0 0 .6rem 0;
    }
    .pros-cons li {
      font-size: .78rem; color: #8a9bb8; padding: .2rem 0 .2rem 1rem;
      position: relative; line-height: 1.4;
    }
    .pros li::before { content: '✓'; position: absolute; left: 0; color: #00ff88; font-weight: 700; }
    .cons li::before { content: '✗'; position: absolute; left: 0; color: #ff4466; font-weight: 700; }
"""
content = content.replace('.flip-back-hint {', pros_cons_css + '\n    .flip-back-hint {')

# 3. Add advantages/disadvantages data for ALL planes and update the card renderer
# We'll add a "pros" and "cons" field to each plane

pros_cons_data = {
    "Boeing 747-8": {
        "pros": ["Massive payload capacity", "Proven reliability over decades", "Nose-loading cargo variant available"],
        "cons": ["High fuel consumption (4 engines)", "Being phased out by twin-engine jets", "High operating costs"]
    },
    "Airbus A380": {
        "pros": ["Largest passenger capacity (853 max)", "Extremely quiet cabin", "Unmatched passenger comfort & space"],
        "cons": ["Production discontinued (2021)", "Requires special airport infrastructure", "Very high operating cost per flight"]
    },
    "Boeing 787 Dreamliner": {
        "pros": ["50% composite = lighter & fuel-efficient", "Higher cabin humidity & pressure", "20% less fuel than predecessors"],
        "cons": ["Battery fire issues (early models)", "Slower than legacy wide-bodies", "Production quality concerns"]
    },
    "Airbus A350 XWB": {
        "pros": ["53% composite airframe", "Ultra-long range (16,100 km)", "Lower noise footprint"],
        "cons": ["Relatively new fleet = less data", "Expensive list price", "Limited freighter variant availability"]
    },
    "Boeing 777X": {
        "pros": ["World's most powerful engine (GE9X)", "Folding wingtips for gate compatibility", "Exceptional range for twin-engine"],
        "cons": ["Significant certification delays", "Heavy competition from A350", "High development cost overruns"]
    },
    "Airbus A320neo": {
        "pros": ["Best-selling single-aisle ever", "20% fuel savings over ceo", "Massive global support network"],
        "cons": ["Limited range for transatlantic", "Narrow cabin for long flights", "Engine delivery bottlenecks"]
    },
    "Embraer E195-E2": {
        "pros": ["Lowest seat-mile cost in class", "Quietest cabin in regional jets", "Excellent short-runway performance"],
        "cons": ["Smaller passenger capacity", "Limited brand recognition vs Airbus/Boeing", "Fewer operator networks"]
    },
    "F-22 Raptor": {
        "pros": ["Unmatched stealth & supercruise", "Thrust vectoring for extreme agility", "Dominant air superiority record"],
        "cons": ["Extremely expensive ($150M+ each)", "Export banned by US law", "Production line closed (187 built)"]
    },
    "F-35 Lightning II": {
        "pros": ["Most advanced sensor fusion ever", "Three variants (CTOL/STOVL/CV)", "Massive international coalition"],
        "cons": ["Most expensive weapons program in history", "Limited sustained speed (Mach 1.6)", "Ongoing software & reliability issues"]
    },
    "Su-57 Felon": {
        "pros": ["3D thrust vectoring", "Very long combat range", "Advanced AESA radar suite"],
        "cons": ["Very limited production numbers", "Engine still being upgraded", "Stealth inferior to F-22/F-35"]
    },
    "Eurofighter Typhoon": {
        "pros": ["Exceptional high-altitude performance", "Proven in NATO operations", "Continuous upgrades (Captor-E AESA)"],
        "cons": ["Multi-nation politics slow upgrades", "Higher maintenance than single-engine jets", "Limited stealth capability"]
    },
    "Dassault Rafale": {
        "pros": ["True omnirole capability", "Nuclear deterrence certified", "Battle-proven in 5+ conflicts"],
        "cons": ["Smaller payload than twin-engine peers", "Higher cost than F-16 class", "Limited export base (growing)"]
    },
    "F-16 Fighting Falcon": {
        "pros": ["4,600+ built = massive support network", "Extremely affordable per unit", "50+ years of continuous upgrades"],
        "cons": ["Single engine = less survivability", "4th-gen = limited stealth", "Aging airframe design"]
    },
    "F/A-18E/F Super Hornet": {
        "pros": ["Carrier-capable multirole fighter", "Excellent low-speed handling", "Advanced Super Hornet upgrade path"],
        "cons": ["Slower than land-based peers", "Higher drag from carrier hardware", "Being replaced by F-35C"]
    },
    "Chengdu J-20 Mighty Dragon": {
        "pros": ["Long-range interception capability", "Large internal weapons bays", "Rapidly improving Chinese avionics"],
        "cons": ["Engine performance still developing", "Limited combat-proven record", "Classified specs = uncertain data"]
    },
    "Gulfstream G700": {
        "pros": ["Tallest, widest, longest cabin ever", "5 living areas + master suite", "Ultra-quiet cabin environment"],
        "cons": ["$75M+ price tag", "High fuel burn for private jet", "Limited airport access due to size"]
    },
    "Bombardier Global 7500": {
        "pros": ["Longest range in business aviation", "4 true cabin zones", "Smooth-ride Nu Wave wing"],
        "cons": ["Very high acquisition cost", "Large ramp footprint", "Limited cabin crew facilities"]
    },
    "Dassault Falcon 10X": {
        "pros": ["Widest cabin cross-section", "Fighter-derived FalconEye HUD", "Exceptional low-speed handling"],
        "cons": ["Still entering service", "Limited service network vs G700", "Premium pricing"]
    },
    "Cessna Citation Longitude": {
        "pros": ["Quietest cabin in super-midsize class", "Flat floor cabin", "Lower operating costs than peers"],
        "cons": ["Smaller cabin than large-cabin jets", "Limited transcontinental range", "Fewer amenities than flagships"]
    },
    "Antonov An-225 Mriya": {
        "pros": ["Largest aircraft ever built", "250-ton payload capacity", "Carried space shuttle on its back"],
        "cons": ["Destroyed in 2022 (irreplaceable)", "Only 1 ever completed", "Extremely expensive to operate"]
    },
    "Boeing 747-8 Freighter": {
        "pros": ["Nose-loading door for outsized cargo", "Largest commercial freighter in production", "Proven backbone of global freight"],
        "cons": ["4-engine fuel consumption", "Being challenged by 777F", "High crew & maintenance costs"]
    },
    "Airbus BelugaXL": {
        "pros": ["Enormous 2,209 m3 cargo bay", "Can carry 2 A350 wings at once", "Purpose-built for outsized loads"],
        "cons": ["Very limited range (4,000 km)", "Not commercially available", "Specialized = no versatility"]
    },
    "Lockheed C-5M Super Galaxy": {
        "pros": ["Front AND rear loading ramps", "Can carry 2 M1 Abrams tanks", "Intercontinental strategic range"],
        "cons": ["Very high maintenance hours per flight", "Aging airframe (1960s design)", "Limited fleet size"]
    },
    "Boeing C-17 Globemaster III": {
        "pros": ["Lands on short austere runways", "Carries M1 tanks & helicopters", "Excellent tactical flexibility"],
        "cons": ["Production ended (2015)", "High unit cost ($218M)", "Limited to military operators"]
    },
    "Lockheed C-130J Super Hercules": {
        "pros": ["Longest military production run ever", "70+ nations operate it", "Dozens of specialized variants"],
        "cons": ["Turboprop = slower than jets", "Limited payload vs C-17", "Pressurized but not comfortable"]
    },
    "Airbus A400M Atlas": {
        "pros": ["Turboprop efficiency + jet speed", "Aerial refueling capable", "Bridges C-130 and C-17 gap"],
        "cons": ["Troubled development history", "Engine reliability issues early on", "Higher cost than planned"]
    },
    "Bell Boeing V-22 Osprey": {
        "pros": ["Unique tiltrotor = VTOL + speed", "2x faster than helicopters", "Long-range special operations capable"],
        "cons": ["Controversial safety record", "Very high maintenance costs", "Complex & expensive to operate"]
    },
    "BAE Hawk T.2": {
        "pros": ["Trained more pilots than any trainer", "Red Arrows display team aircraft", "Combat-capable light attack variant"],
        "cons": ["Subsonic only", "Aging design (1974)", "Limited avionics vs modern trainers"]
    },
    "Beechcraft T-6 Texan II": {
        "pros": ["Every US military pilot's first aircraft", "Pressurized cockpit", "Aerobatic capable"],
        "cons": ["Oxygen system safety concerns", "Turboprop = limited speed envelope", "Not lead-in fighter capable"]
    },
    "Pilatus PC-21": {
        "pros": ["Can replace lead-in jet trainers", "Embedded tactical simulation", "Extremely cost-effective training"],
        "cons": ["Turboprop = no actual jet experience", "Swiss export restrictions", "Small cockpit for larger pilots"]
    },
    "KAI T-50 Golden Eagle": {
        "pros": ["First supersonic trainer ever", "F-16 derived = real fighter feel", "FA-50 light combat variant"],
        "cons": ["Single engine = less safe for training", "Limited export success so far", "Higher cost than turboprop trainers"]
    },
    "AH-64E Apache Guardian": {
        "pros": ["Longbow radar = fire-and-forget", "Helmet-mounted target acquisition", "16 Hellfire missiles capacity"],
        "cons": ["Very expensive ($35M+ each)", "Complex maintenance requirements", "Vulnerable to MANPADS"]
    },
    "UH-60M Black Hawk": {
        "pros": ["4,000+ built worldwide", "Extremely versatile (medevac/assault/VIP)", "28 nations operate it"],
        "cons": ["Not heavily armed by default", "Tail rotor vulnerability", "High acquisition cost for allies"]
    },
    "Mi-24 Hind": {
        "pros": ["Unique gunship + troop carrier combo", "Heavily armored 'flying tank'", "Affordable & widely available"],
        "cons": ["Less maneuverable than pure gunships", "Outdated avionics in base models", "High fuel consumption"]
    },
    "CH-47F Chinook": {
        "pros": ["Unmatched heavy-lift capability", "60+ years of proven service", "High-altitude operations capable"],
        "cons": ["Very large & hard to conceal", "Tandem rotors = complex maintenance", "Slow compared to tiltrotors"]
    },
    "Airbus H145": {
        "pros": ["Fenestron tail rotor = very safe", "Excellent air ambulance platform", "Low noise footprint for urban ops"],
        "cons": ["Light utility = limited payload", "Not suitable for heavy combat", "Higher cost than single-engine options"]
    },
    "Canadair CL-415 SuperScooper": {
        "pros": ["Scoops 6,137L in 12 seconds", "Purpose-built aerial firefighter", "Amphibious landing capability"],
        "cons": ["Very limited non-firefighting use", "Slow cruise speed", "Aging design (1993)"]
    },
    "ShinMaywa US-2": {
        "pros": ["Lands in 3m ocean swells", "Advanced boundary layer control", "Deep-sea rescue capability"],
        "cons": ["Extremely expensive ($150M+)", "Only operated by Japan", "Very limited production"]
    },
    "AVIC AG600 Kunlong": {
        "pros": ["Largest amphibious aircraft in production", "12,000L water capacity", "Multi-role (SAR + firefighting)"],
        "cons": ["Still in testing/certification", "Unproven in operational service", "Limited international interest"]
    },
    "de Havilland DHC-6 Twin Otter (Floats)": {
        "pros": ["Legendary bush plane reliability", "Operates on wheels/skis/floats", "STOL from shortest strips"],
        "cons": ["Small passenger capacity (19)", "Unpressurized cabin", "Slow cruise speed"]
    }
}

# Now update the JS to include pros/cons in the data and render them
# Add pros/cons to each plane object in the JS
for plane_name, pc in pros_cons_data.items():
    escaped_name = re.escape(plane_name)
    pros_str = json.dumps(pc["pros"])
    cons_str = json.dumps(pc["cons"])
    
    # Find the desc line for this plane and append pros/cons after it
    pattern = rf'(name: "{re.escape(plane_name)}".*?desc: "[^"]*")'
    replacement = rf'\1,\n    pros: {pros_str},\n    cons: {cons_str}'
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Update the createCard function to render pros/cons
old_render = """const specsHTML = Object.entries(plane.specs).map(([k,v]) =>
    `<div class="spec-item"><div class="spec-label">${k}</div><div class="spec-val">${v}</div></div>`
  ).join('');"""

new_render = """const specsHTML = Object.entries(plane.specs).map(([k,v]) =>
    `<div class="spec-item"><div class="spec-label">${k}</div><div class="spec-val">${v}</div></div>`
  ).join('');

  const prosHTML = (plane.pros || []).map(p => `<li>${p}</li>`).join('');
  const consHTML = (plane.cons || []).map(c => `<li>${c}</li>`).join('');
  const prosConsHTML = (prosHTML || consHTML) ? `
    <div class="pros-cons">
      <div class="pros"><h4>✦ Advantages</h4><ul>${prosHTML}</ul></div>
      <div class="cons"><h4>✦ Disadvantages</h4><ul>${consHTML}</ul></div>
    </div>` : '';"""

content = content.replace(old_render, new_render)

# Update the back card template to include prosConsHTML
old_back = '<div class="back-desc">${plane.desc}</div>'
new_back = '<div class="back-desc">${plane.desc}</div>\n        ${prosConsHTML}'
content = content.replace(old_back, new_back)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done! Added scrolling fix + pros/cons for ALL 40 planes.")
