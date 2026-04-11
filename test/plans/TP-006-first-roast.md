# TP-006: First Roast Commissioning

## Purpose
Execute the first real coffee roast. The goal is to safely reach and pass first
crack, collect a complete dataset, and identify improvements for subsequent roasts.
This is NOT about producing great coffee — it is about proving the system works
end-to-end and collecting characterization data.

## Prerequisites
- TP-005 passed (full integration test)
- All safety systems verified under load
- Artisan connected and logging
- Operator has read and understands safety interlock behavior
- Operator has reviewed TP-002 thermal data (knows expected temp ranges)

## Equipment
- Complete roaster assembly
- 113g green coffee beans (suggest a forgiving single-origin, medium density)
- Cooling tray or colander for dumping roasted beans
- Fire extinguisher within arm's reach (mandatory, non-negotiable)
- Timer
- Notebook for manual observations
- Optional: sound recorder or phone for first-crack audio

## Pre-Roast Checklist

- [ ] TP-005 passed within the last 7 days
- [ ] All mechanical fasteners checked
- [ ] Exhaust path clear of chaff from prior tests
- [ ] Fire extinguisher present and charged
- [ ] Artisan connected and logging confirmed
- [ ] Room ventilation adequate (open window or range hood)
- [ ] Hard disconnect accessible
- [ ] Operator is not distracted

## Roast Procedure

### Phase 1: Startup
1. Power on system, verify ESP32 boot and sensor readings
2. Set blower to fluidization speed (from TP-001/TP-005)
3. Load 113g green coffee beans
4. Verify fluidization is good (visual)
5. Record initial TC1, TC2, TC3 readings

### Phase 2: Heat Application (Conservative Ramp)
6. Command HEAT 20 — hold for 60 seconds, observe TC1 rise
7. Command HEAT 40 — hold for 60 seconds
8. Command HEAT 60 — hold for 60 seconds
9. Command HEAT 80 — hold and monitor
10. Continue adjusting heater to maintain TC1 in a safe climbing range
11. **Do not exceed 100% for extended periods on first roast**

### Phase 3: Drying Phase
12. Observe TC2 (bean bed temp) — beans are drying when TC2 climbs through ~150°C
13. Note any color change or grassy smell (drying to yellowing transition)
14. Record TC2 at color-change observation

### Phase 4: Maillard / Development
15. Beans transition from yellow to light brown
16. TC2 climbing through ~170-190°C
17. Monitor rate of TC2 change — should be accelerating
18. Listen for first crack (sharp popping sounds, ~195-205°C on TC2, depends on setup)

### Phase 5: First Crack
19. **Record TC2 at first crack onset**
20. Note time from heat-on to first crack
21. Reduce heater to 40-50% (or lower) to slow development
22. Let first crack complete (popping tapers off, ~30-90 seconds)
23. **For first roast: stop here.** Do not push to second crack.

### Phase 6: Cool-Down
24. Command HEAT 0
25. Keep blower running at full speed
26. Monitor TC2 descent
27. When TC2 < 50°C, dump beans to cooling tray
28. Continue blower for 30 seconds to cool internals
29. Power down

## Key Data Points to Record

| Event | TC1 (°C) | TC2 (°C) | TC3 (°C) | Time (mm:ss) | Heater % | Notes |
|-------|----------|----------|----------|--------------|----------|-------|
| Heat on | | | | 0:00 | | |
| Yellowing | | | | | | |
| First crack start | | | | | | |
| First crack end | | | | | | |
| Heater off | | | | | | |
| Beans dumped | | | | | | |

## Post-Roast Review

### Immediate
- [ ] Save Artisan log file
- [ ] Photograph the roasted beans
- [ ] Note roast color and uniformity (even vs. tipping/scorching)
- [ ] Note any off-smells during roast
- [ ] Inspect distributor plate for obstructions
- [ ] Inspect exhaust path for chaff accumulation
- [ ] Check all external surface temps (IR thermometer)

### Analysis (within 24 hours)
- [ ] Review Artisan curves: are they smooth and physically coherent?
- [ ] Calculate rate-of-rise (RoR) from TC2 data
- [ ] Compare TC1/TC2/TC3 relationships to TP-002 empty-chamber data
- [ ] Identify the effective heat transfer: how much did beans affect thermal behavior?
- [ ] Document total roast time, development time ratio
- [ ] List what went well and what needs changing

### Taste (24-48 hours post-roast)
- [ ] Brew and taste the coffee
- [ ] Note: underdeveloped / well-developed / overdeveloped
- [ ] This is not about quality — it's about whether the roast reached the intended level

## Failure Modes During Roast

| Symptom | Action |
|---------|--------|
| Safety shutdown triggers | Note temps, do not override. Cool down. Investigate. |
| Beans stop fluidizing | Reduce heater, increase blower. If stuck: STOP. |
| Smoke beyond normal roast smoke | Reduce heater. If excessive: STOP. |
| Strange electrical smell | STOP immediately. Disconnect power. Investigate. |
| First crack doesn't arrive by 20 min | Heater may be undersized. End roast, review data. |
| TC readings go erratic | STOP. Check TC connections. |

## Success Criteria

This first roast is successful if:
1. The system operated safely from start to finish
2. Beans reached at least first crack
3. A complete data log was captured
4. No mechanical, electrical, or firmware failures occurred
5. Enough data was collected to plan improvements for roast #2

## Traceability
- All prior test plans: TP-001 through TP-005
- Design: `claude.md` (v1 build intent)
- Thermal data: TP-002 results
