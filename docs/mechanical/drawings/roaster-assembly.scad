// =============================================================
// Fluid-Bed Coffee Roaster v1 — Assembly Model
// =============================================================
// Parametric model for visualization and fit-checking.
// All dimensions in millimeters. Render with OpenSCAD.
//
// Usage:
//   - Open in OpenSCAD and press F5 (preview) or F6 (render)
//   - Toggle components on/off with show_* variables below
//   - Switch chamber size with chamber_od variable
//
// Reference: docs/system/architecture.md, docs/mechanical/baseplate-layout.md,
// docs/system/design-log.md (DR-008, DR-009, DR-011, DR-012, DR-013).
//
// Geometry as of 2026-05-07: motor + heater element measured and in hand;
// 12" × 18" steel deck cut from BASE-001 stock; angle-iron frame with rear
// (motor) and front (electronics) extensions.
// =============================================================

// --- Configuration -------------------------------------------

// Chamber selection: 63.5 (2.5" OD) or 76.2 (3.0" OD)
chamber_od = 63.5;  // mm — change to 76.2 for backup chamber

// Component visibility toggles
show_deck            = true;
show_frame           = true;
show_extensions      = true;
show_legs            = true;       // DR-013 tripod legs
show_plenum          = true;
show_top_cap         = true;
show_bottom_cap      = true;
show_clamp_ring      = true;
show_distributor     = true;
show_baffle          = true;
show_chamber         = true;
show_cone_reducer    = true;
show_chaff_collector = true;
show_heater_can      = true;
show_blower          = true;
show_electronics_box = true;
show_heat_barrier    = true;
show_zone_e          = true;       // DR-017 Pi 5 + display riser

// --- Origin convention --------------------------------------
// (0, 0, 0) is the rear-left corner of the steel deck, at the deck top
// surface. +X is to the operator's right (across the long edge);
// +Y is forward (toward the operator); +Z is up.

// --- Deck (BASE-001 cut) ------------------------------------

deck_width   = 305;     // 12 inches (X)
deck_length  = 457;     // 18 inches (Y)
deck_thick   = 1.6;     // ~16 ga steel sheet (visual only)

// --- Frame and extensions (angle iron) ----------------------

frame_angle_h    = 25.4;    // 1" angle iron
frame_angle_t    = 3.2;     // ~1/8" leg
rear_ext_length  = 152;     // 6" rear extension for motor (Zone A)
front_ext_length = 125;     // 5" front extension for electronics (Zone D)

// --- Tripod legs (DR-013) -----------------------------------

leg_rod_dia      = 9.5;     // 3/8" threaded rod
leg_below        = 100;     // exposed length below deck (adjustable feet)
leg_above        = 380;     // length above deck up to chamber-band clamp

// Leg X/Y positions: front pair straddles the plenum on the deck, rear leg
// sits on the rear extension behind the motor (forming a triangle).
front_leg_y      = 380;
rear_leg_y       = -120;
leg_x_offset     = 110;     // distance from deck centerline (X = 152.5)
deck_cx          = deck_width / 2;

// --- Plenum body (DR-012) -----------------------------------

plenum_dia       = 203;     // 8" round black stovepipe
plenum_height    = 152;     // 6" tall
plenum_wall      = 0.5;     // ~26 ga
cap_skirt        = 12;      // pipe-cap skirt depth
cap_thick        = 1.0;     // cap face thickness
plenum_y         = 329;     // CL on long axis (deck Y, see baseplate-layout.md §1)
standoff_h       = 25.4;    // 1" standoff between deck and plenum bottom cap
plenum_bot_z     = standoff_h;
plenum_top_z     = plenum_bot_z + plenum_height;

// Side-entry hole on the rear face (-Y side of the cylindrical wall),
// centerline ~2" above plenum floor (DR-009 ramp clearance).
side_entry_dia   = 64;      // 2.5" — heater-can OD
side_entry_z     = plenum_bot_z + 50;   // 50 mm above plenum floor
side_entry_y     = plenum_y - plenum_dia/2;

// --- Heater can (HTR-CAN-001, DR-002 + 2026-05-07 measurement) ---

heater_can_od    = 64;      // 2.5" SS exhaust pipe
heater_can_id    = 60;      // ~2.37"
heater_can_len   = 178;     // 7" — fits 1.5" × 6" Warrior element + ~0.5" each end

// Heater can axis sits at the same elevation as the plenum side-entry
// centerline. Heater can extends from ~Y=25 to Y=203 (measured along deck Y).
heater_y_rear    = 25;
heater_y_front   = heater_y_rear + heater_can_len;   // = 203
heater_z         = side_entry_z;

// --- Blower (BLW-001 — measured 2026-05-07) -----------------

blower_dia       = 152;     // 6" body
blower_height    = 152;     // 6" tall
blower_outlet_dia = 38;     // 1.5" / 38.10mm pipe — BLW-HOUS-001 fan shell outlet is AXIAL
                            // (off-center on dome face, parallel to motor shaft); BLW-ELBOW-001
                            // 90° silicone elbow redirects horizontal-forward to BLW-COUP-001
blower_y         = -75;     // CL ~75 mm rear of deck rear edge (on rear extension)
blower_x         = deck_cx;
blower_bot_z     = 0;       // sits on rear extension (same Z as deck top)
blower_top_z     = blower_bot_z + blower_height;
blower_outlet_z  = heater_z;   // outlet at heater-can axis elevation

// --- Clamping ring (DR-008 Option A) ------------------------

ring_outer       = chamber_od + 60;     // ~4" exhaust flange OD
ring_inner       = (chamber_od == 63.5) ? 50.8 : 63.5;  // 2" / 2.5" ID
ring_thick       = 3;

// --- Distributor plate (DR-013 D1: FengYoo plate as-is) -----

plate_dia        = chamber_od - 3.2;    // chamber ID
plate_thick      = 1.06;                // 19 ga FengYoo

// --- Roast chamber ------------------------------------------

chamber_id       = chamber_od - 3.2;
chamber_length   = 304.8;   // 12"

// --- Cone reducer (EXH-004) and chaff collector (DR-006) ----

cone_height      = 50;
chaff_od         = 101.6;   // 4"
chaff_height     = 127;     // 5"

// --- Heat barrier (between Zones C and D) -------------------

barrier_thick    = 1.5;
barrier_height   = 200;
barrier_y        = deck_length - 12;   // bolted just inside front edge

// --- Electronics tray (Zone D) ------------------------------

ebox_w           = 280;
ebox_d           = 100;
ebox_h           = 90;
ebox_y           = deck_length + 12;   // on front extension, ~12 mm past barrier

// --- Zone E: Pi 5 host + 5x7" HDMI display riser (DR-017) ---

// Display: on-hand 5x7" HDMI touch panel (HDMI in + USB power/touch in).
// Exact perimeter unmeasured (G3) — placeholder dimensions match the
// active area (5" x 7") plus an estimated 0.5" bezel each side.
display_w        = 178;     // 7" wide (X)
display_h        = 152;     // 5" tall (Z, when standing)
display_thick    = 12;      // ~12 mm panel + bezel depth
display_bezel    = 13;      // 0.5" bezel allowance on every edge (already included in w/h)

// Pi 5 PCB mounts on standoffs behind the display. M2.5 standoff stack
// raises the Pi ~12 mm clear of the back of the display for cooling
// clearance over the active cooler intake.
pi5_w            = 85;
pi5_d            = 56;
pi5_h            = 18;      // Pi 5 board + active cooler stack
pi5_standoff     = 12;

// Riser geometry: vertical stalk from the front extension. Display
// centerline targets ~1100 mm above floor (operator eye-level when
// standing), which with the DR-013 leg height puts the display centerline
// roughly leg_above - 20 mm above the deck top.
zone_e_stalk_w   = 20;      // 3/4" angle-iron / flat-bar stalk visualization
zone_e_stalk_t   = 6;       // stalk thickness
zone_e_stalk_h   = 320;     // height above deck top to display bottom edge
zone_e_tilt      = 18;      // backward tilt of display, degrees

// Position: stalk roots at the front edge of the front extension,
// centered across X.
zone_e_y         = deck_length + front_ext_length - 15;   // 15 mm back from front extension edge
zone_e_x_center  = deck_cx;

// --- Deflector ramp baffle (DR-009) -------------------------

baffle_w         = 76;
baffle_h         = 100;
baffle_t         = 1.2;
baffle_angle     = 45;

// =============================================================
// Modules
// =============================================================

module deck() {
    color("Gainsboro")
    translate([0, 0, -deck_thick])
        cube([deck_width, deck_length, deck_thick]);
}

module angle_iron(length) {
    // Angle iron section running along Y, leg up + leg out
    color("DimGray")
    union() {
        cube([frame_angle_h, length, frame_angle_t]);
        cube([frame_angle_t, length, frame_angle_h]);
    }
}

module frame() {
    // Two long-edge angles running the full assembly length (deck +
    // extensions). Cross-members at deck rear and front edges and at the
    // outer ends of the extensions.
    total_y_start = -rear_ext_length;
    total_y_len   = rear_ext_length + deck_length + front_ext_length;

    // Long-edge angles on -X and +X sides
    translate([0, total_y_start, -deck_thick - frame_angle_h])
        angle_iron(total_y_len);
    translate([deck_width - frame_angle_h, total_y_start, -deck_thick - frame_angle_h])
        rotate([0, 0, 90])
            translate([0, -frame_angle_h, 0])
                angle_iron(total_y_len);

    // Cross-members (4 total: rear-of-extension, deck-rear, deck-front,
    // front-of-extension) — drawn as simple bars
    color("DimGray")
    for (yy = [total_y_start, 0, deck_length, total_y_start + total_y_len - frame_angle_h]) {
        translate([0, yy, -deck_thick - frame_angle_h])
            cube([deck_width, frame_angle_h, frame_angle_t]);
    }
}

module extensions() {
    // Visual rendering of the rear and front extension "decks" (could
    // be sheet-metal infill or just open angle-iron framing — here drawn
    // as a thin sheet panel for clarity).
    color("Silver", 0.6) {
        // Rear extension panel
        translate([0, -rear_ext_length, -deck_thick])
            cube([deck_width, rear_ext_length, deck_thick]);
        // Front extension panel
        translate([0, deck_length, -deck_thick])
            cube([deck_width, front_ext_length, deck_thick]);
    }
}

module legs() {
    color("DarkGray")
    for (pos = [
        [deck_cx - leg_x_offset, front_leg_y],
        [deck_cx + leg_x_offset, front_leg_y],
        [deck_cx,                rear_leg_y]
    ]) {
        translate([pos[0], pos[1], -leg_below])
            cylinder(h = leg_below + leg_above, d = leg_rod_dia, $fn = 16);
    }

    // Chamber-band clamp at top — visualized as a flat ring above the
    // chamber/cone-reducer transition
    band_z = leg_above - 60;
    color("DimGray")
    translate([deck_cx, plenum_y, band_z])
    difference() {
        cylinder(h = 6, d = chaff_od + 20, $fn = 60);
        translate([0, 0, -1]) cylinder(h = 8, d = chaff_od + 6, $fn = 60);
    }
}

module plenum_body() {
    // Cylindrical wall of the stovepipe plenum
    color("LightSteelBlue", 0.5)
    translate([deck_cx, plenum_y, plenum_bot_z])
    difference() {
        cylinder(h = plenum_height, d = plenum_dia, $fn = 64);
        translate([0, 0, -1])
            cylinder(h = plenum_height + 2, d = plenum_dia - 2*plenum_wall, $fn = 64);
        // Side-entry hole (rear face = -Y direction)
        translate([0, -plenum_dia/2 - 1, 50])
            rotate([-90, 0, 0])
                cylinder(h = plenum_wall + 2, d = side_entry_dia, $fn = 32);
    }
}

module bottom_cap() {
    // Slip-fit pipe cap on plenum bottom
    color("LightSteelBlue", 0.7)
    translate([deck_cx, plenum_y, plenum_bot_z - cap_thick]) {
        // cap face
        cylinder(h = cap_thick, d = plenum_dia + 4, $fn = 64);
        // skirt (drawn as a ring above the cap face, hugging plenum exterior)
        difference() {
            cylinder(h = cap_skirt, d = plenum_dia + 4, $fn = 64);
            translate([0, 0, -1])
                cylinder(h = cap_skirt + 2, d = plenum_dia, $fn = 64);
        }
    }
}

module top_cap() {
    // Top pipe cap, drilled to chamber OD; clamp ring attaches underneath
    color("LightSteelBlue", 0.7)
    translate([deck_cx, plenum_y, plenum_top_z]) {
        difference() {
            // cap face
            cylinder(h = cap_thick, d = plenum_dia + 4, $fn = 64);
            translate([0, 0, -1])
                cylinder(h = cap_thick + 2, d = chamber_od, $fn = 60);
        }
        // skirt
        translate([0, 0, -cap_skirt])
        difference() {
            cylinder(h = cap_skirt, d = plenum_dia + 4, $fn = 64);
            translate([0, 0, -1])
                cylinder(h = cap_skirt + 2, d = plenum_dia, $fn = 64);
        }
    }
}

module clamp_ring() {
    // Annular ring tapped for M4, mounted on underside of top cap face
    color("DimGray")
    translate([deck_cx, plenum_y, plenum_top_z - ring_thick])
    difference() {
        cylinder(h = ring_thick, d = ring_outer, $fn = 48);
        translate([0, 0, -1])
            cylinder(h = ring_thick + 2, d = ring_inner, $fn = 48);
    }
}

module distributor_plate() {
    color("Goldenrod", 0.7)
    translate([deck_cx, plenum_y, plenum_top_z])
        cylinder(h = plate_thick, d = plate_dia, $fn = 60);
}

module chamber() {
    color("LightBlue", 0.4)
    translate([deck_cx, plenum_y, plenum_top_z + plate_thick])
    difference() {
        cylinder(h = chamber_length, d = chamber_od, $fn = 60);
        translate([0, 0, -1])
            cylinder(h = chamber_length + 2, d = chamber_id, $fn = 60);
    }
}

module cone_reducer() {
    z0 = plenum_top_z + plate_thick + chamber_length;
    color("LightSlateGray", 0.5)
    translate([deck_cx, plenum_y, z0])
        cylinder(h = cone_height, d1 = chamber_od, d2 = chaff_od, $fn = 60);
}

module chaff_collector() {
    z0 = plenum_top_z + plate_thick + chamber_length + cone_height;
    color("Plum", 0.5)
    translate([deck_cx, plenum_y, z0])
    difference() {
        cylinder(h = chaff_height, d = chaff_od, $fn = 60);
        translate([0, 0, 1])
            cylinder(h = chaff_height, d = chaff_od - 2*plenum_wall, $fn = 60);
    }
    // Mesh disc near the top
    color("Gray", 0.5)
    translate([deck_cx, plenum_y, z0 + chaff_height - 6])
        cylinder(h = 1, d = chaff_od - 4, $fn = 60);
}

module heater_can() {
    // Horizontal can along Y axis between blower outlet and plenum side-entry
    color("Tomato", 0.7)
    translate([deck_cx, heater_y_rear, heater_z])
    rotate([-90, 0, 0])
    difference() {
        cylinder(h = heater_can_len, d = heater_can_od, $fn = 40);
        translate([0, 0, -1])
            cylinder(h = heater_can_len + 2, d = heater_can_id, $fn = 40);
    }

    // Visualize the nichrome element pack as a rectangular volume inside
    color("OrangeRed", 0.6)
    translate([deck_cx - 19, heater_y_rear + 13, heater_z - 5])
        cube([38, 152, 10]);   // 1.5" × 6" element
}

module blower() {
    // Cylindrical body, vertical axis, on rear extension
    color("CornflowerBlue", 0.7)
    translate([blower_x, blower_y, blower_bot_z])
        cylinder(h = blower_height, d = blower_dia, $fn = 60);

    // Axial outlet stub from BLW-HOUS-001 fan shell — exits vertically off-center
    // on top of the motor (offset ~30mm forward of shaft axis).
    blower_pipe_offset = 30;     // axial-outlet pipe is off-center on the dome
    blower_pipe_h      = 25;     // vertical pipe length out of housing dome
    color("CornflowerBlue", 0.85)
    translate([blower_x, blower_y + blower_pipe_offset, blower_top_z])
        cylinder(h = blower_pipe_h, d = blower_outlet_dia, $fn = 32);

    // BLW-ELBOW-001 turn — represented as a horizontal stub forward (+Y) from
    // the top of the vertical pipe, at heater-can centerline elevation.
    color("CornflowerBlue", 0.85)
    translate([blower_x, blower_y + blower_pipe_offset, blower_top_z + blower_pipe_h])
    rotate([-90, 0, 0])
        cylinder(h = blower_dia/2 + 30, d = blower_outlet_dia, $fn = 32);
}

module heat_barrier() {
    color("Silver", 0.4)
    translate([0, barrier_y, 0])
        cube([deck_width, barrier_thick, barrier_height]);
}

module electronics_box() {
    color("PaleGreen", 0.5)
    translate([(deck_width - ebox_w)/2, ebox_y, 0])
        cube([ebox_w, ebox_d, ebox_h]);
}

module zone_e() {
    // Zone E: Pi 5 + 5x7" HDMI display on a tilt-back vertical stalk.
    //
    // Construction:
    //   1. Vertical stalk (flat-bar visualization) rising from front
    //      extension at the front edge.
    //   2. Tilt mount at the top of the stalk.
    //   3. Display panel rotated ~zone_e_tilt deg backward from vertical.
    //   4. Pi 5 PCB (with active cooler) on standoffs behind the display.
    //
    // Cables (visualized as a thin bundle from Pi back down the stalk):
    //   - USB-C power in (Pi -> mains-side PSU)
    //   - USB-A out to ESP32 (Pi -> Zone D)
    //   - micro-HDMI -> HDMI (Pi -> display, lives entirely in Zone E)

    // Stalk: vertical flat-bar
    color("DimGray")
    translate([zone_e_x_center - zone_e_stalk_w/2,
               zone_e_y - zone_e_stalk_t/2,
               0])
        cube([zone_e_stalk_w, zone_e_stalk_t, zone_e_stalk_h]);

    // Tilt-mount + display + Pi 5 form a rigid assembly that rotates
    // backward (toward -Y) by zone_e_tilt degrees around the X axis.
    translate([zone_e_x_center, zone_e_y, zone_e_stalk_h])
    rotate([-zone_e_tilt, 0, 0]) {
        // Display panel (facing operator = facing +Y face of the rotated block)
        color("MidnightBlue", 0.9)
        translate([-display_w/2, -display_thick, 0])
            cube([display_w, display_thick, display_h]);

        // Active touch surface (slight inset, brighter)
        color("DeepSkyBlue", 0.6)
        translate([-display_w/2 + display_bezel,
                   -display_thick - 0.4,
                   display_bezel])
            cube([display_w - 2*display_bezel, 0.4, display_h - 2*display_bezel]);

        // Pi 5 PCB on standoffs behind the display
        color("DarkGreen", 0.85)
        translate([-pi5_w/2,
                   pi5_standoff,
                   (display_h - pi5_d)/2])
            cube([pi5_w, pi5_d, pi5_h]);

        // Active cooler nub on top of Pi 5
        color("Silver", 0.7)
        translate([-30, pi5_standoff + 10, (display_h - pi5_d)/2 + pi5_h])
            cube([60, 36, 8]);
    }

    // Cable bundle running back down the stalk (visualization)
    color("Black", 0.5)
    translate([zone_e_x_center - 4,
               zone_e_y + zone_e_stalk_t/2,
               20])
        cube([8, 4, zone_e_stalk_h - 40]);
}

module baffle() {
    color("Orange", 0.8)
    translate([deck_cx, plenum_y + plenum_dia/2 - 30, plenum_bot_z + 10])
    rotate([0, 0, 0])
    rotate([baffle_angle, 0, 0])
    translate([-baffle_w/2, -baffle_t/2, 0])
        cube([baffle_w, baffle_t, baffle_h]);
}

// =============================================================
// Assembly
// =============================================================

if (show_deck)            deck();
if (show_frame)           frame();
if (show_extensions)      extensions();
if (show_legs)            legs();
if (show_blower)          blower();
if (show_heater_can)      heater_can();
if (show_plenum)          plenum_body();
if (show_bottom_cap)      bottom_cap();
if (show_baffle)          baffle();
if (show_top_cap)         top_cap();
if (show_clamp_ring)      clamp_ring();
if (show_distributor)     distributor_plate();
if (show_chamber)         chamber();
if (show_cone_reducer)    cone_reducer();
if (show_chaff_collector) chaff_collector();
if (show_heat_barrier)    heat_barrier();
if (show_electronics_box) electronics_box();
if (show_zone_e)          zone_e();

// =============================================================
// Annotations (console output)
// =============================================================

total_height = plenum_top_z + plate_thick + chamber_length + cone_height + chaff_height;
total_y_len  = rear_ext_length + deck_length + front_ext_length;

echo(str("--- Assembly Summary ---"));
echo(str("Chamber OD: ", chamber_od, " mm (", chamber_od/25.4, " in)"));
echo(str("Deck: ", deck_width, " x ", deck_length, " mm (",
         deck_width/25.4, " x ", deck_length/25.4, " in)"));
echo(str("Total frame length (rear ext + deck + front ext): ",
         total_y_len, " mm (", total_y_len/25.4, " in)"));
echo(str("Total assembly height above deck: ", total_height, " mm (",
         total_height/25.4, " in)"));
echo(str("Plenum CL on long axis (deck Y): ", plenum_y, " mm"));
echo(str("Heater can: Y=", heater_y_rear, " to Y=", heater_y_front,
         " (", heater_can_len, " mm long)"));
echo(str("Blower: dia ", blower_dia, " x ", blower_height,
         " mm; CL at Y=", blower_y, " (", -blower_y, " mm rear of deck rear edge)"));
echo(str("Zone E (DR-017): display ", display_w, "x", display_h,
         " mm, Pi 5 ", pi5_w, "x", pi5_d, "x", pi5_h,
         " mm, stalk Y=", zone_e_y, " Z to ", zone_e_stalk_h, " mm"));
