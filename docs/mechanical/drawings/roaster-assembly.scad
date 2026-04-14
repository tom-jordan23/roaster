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
// Reference: docs/system/architecture.md, design-log.md
// =============================================================

// --- Configuration -------------------------------------------

// Chamber selection: 63.5 (2.5" OD) or 76.2 (3.0" OD)
chamber_od = 63.5;  // mm — change to 76.2 for backup chamber

// Component visibility toggles
show_baseplate       = true;
show_plenum          = true;
show_baffle          = true;
show_clamping_ring   = true;
show_distributor     = true;
show_chamber         = true;
show_chaff_collector = true;
show_heater_can      = true;
show_blower          = true;
show_standoffs       = true;

// --- Derived dimensions --------------------------------------

chamber_id = chamber_od - 3.2;  // ~1.6mm wall thickness for SS exhaust tube
chamber_length = 304.8;         // 12 inches
chamber_wall = (chamber_od - chamber_id) / 2;

// --- Baseplate (M1: widened for stability) -------------------
// M1: Must be wide enough to prevent tip-over of tall asymmetric assembly.
// Widened in blower direction to 20"+ per DR-010. Add ballast weight
// and L-brackets for lateral bracing.

base_length = 508;   // 20 inches (M1: widened from 16")
base_width  = 305;   // 12 inches (M1: widened from 10")
base_thick  = 19;    // 3/4 inch (plywood) — adjust for steel

// --- Plenum (DR-007) ----------------------------------------
// 1/6 size SS steam table pan, 4" deep

plenum_length = 162.6;  // 6.4 inches
plenum_width  = 160;    // 6.3 inches
plenum_depth  = 101.6;  // 4 inches
plenum_wall   = 1.0;    // ~22 gauge SS

// Plenum position on baseplate (centered on width, offset on length
// to leave room for blower+heater on one side)
plenum_x = base_length * 0.55;  // offset toward "back" of base
plenum_y = base_width / 2;      // centered on width
plenum_z = base_thick + 25.4;   // 1" standoff above baseplate

// Side-entry hole (centered on plenum wall, low position)
side_entry_dia = 60;  // ~2.4 inches, sized to heater can outlet
side_entry_z   = plenum_depth * 0.35;  // center of hole, from plenum bottom

// --- Standoffs (under plenum) --------------------------------

standoff_height = 25.4;  // 1 inch
standoff_dia    = 10;    // M5 threaded rod or ceramic spacer
standoff_inset  = 15;    // inset from plenum corners

// --- Deflector Ramp Baffle (DR-009) --------------------------

baffle_width  = 76;     // ~3 inches
baffle_height = 101.6;  // ~4 inches
baffle_thick  = 1.2;    // ~18 gauge SS
baffle_angle  = 45;

// --- Clamping Ring (DR-008) ----------------------------------

ring_outer = min(plenum_length, plenum_width) - 10;  // fits inside pan rim
ring_inner = chamber_od + 1;  // clearance for chamber tube
ring_thick = 3;               // ~11 gauge SS flat stock

// --- Distributor Plate ---------------------------------------

plate_dia   = chamber_id;  // sits inside chamber
plate_thick = 1.5;         // perforated SS sheet

// --- Chaff Expansion Chamber (DR-006) ------------------------

chaff_od     = 101.6;  // 4 inches
chaff_height = 127;    // 5 inches
chaff_wall   = 1.0;

// --- Heater Can (from Warrior heat gun) ----------------------
// Approximate — actual dims pending teardown

heater_can_od     = 65;    // ~2.5 inches (heat gun barrel)
heater_can_length = 190;   // ~7.5 inches
heater_can_wall   = 1.5;

// --- Blower (12V brushless centrifugal) ----------------------

blower_dia    = 120;  // 120mm
blower_depth  = 32;   // 32mm
blower_outlet = 40;   // outlet port width (approx)

// =============================================================
// Modules
// =============================================================

module baseplate() {
    color("BurlyWood", 0.6)
    translate([-base_length/2, -base_width/2, 0])
        cube([base_length, base_width, base_thick]);
}

module standoffs() {
    color("Silver")
    for (dx = [-1, 1], dy = [-1, 1]) {
        translate([
            plenum_x - plenum_length/2 + (dx > 0 ? plenum_length - standoff_inset : standoff_inset) - plenum_x,
            dy * (plenum_width/2 - standoff_inset),
            base_thick
        ])
        translate([plenum_x - base_length/2, 0, 0])
            cylinder(h=standoff_height, d=standoff_dia, $fn=20);
    }
}

module plenum() {
    // Outer shell
    color("LightSteelBlue", 0.7)
    translate([0, 0, plenum_z])
    difference() {
        // Outer box
        translate([-plenum_length/2, -plenum_width/2, 0])
            cube([plenum_length, plenum_width, plenum_depth]);
        // Inner cavity
        translate([-(plenum_length-2*plenum_wall)/2, -(plenum_width-2*plenum_wall)/2, plenum_wall])
            cube([plenum_length-2*plenum_wall, plenum_width-2*plenum_wall, plenum_depth]);
        // Side-entry hole (on -X face)
        translate([-plenum_length/2 - 1, 0, side_entry_z])
            rotate([0, 90, 0])
                cylinder(h=plenum_wall+2, d=side_entry_dia, $fn=40);
    }
}

module baffle() {
    color("Orange", 0.8)
    translate([0, 0, plenum_z])
    // Position inside plenum, opposite side-entry (on +X side of cavity)
    translate([plenum_length/2 - plenum_wall - 15, 0, side_entry_z])
        rotate([0, baffle_angle, 0])
            translate([-baffle_thick/2, -baffle_width/2, -baffle_height/4])
                cube([baffle_thick, baffle_width, baffle_height/2]);
}

module clamping_ring() {
    color("DarkGray", 0.8)
    translate([0, 0, plenum_z + plenum_depth])
    difference() {
        // Outer square ring (simplified as cylinder for now)
        cylinder(h=ring_thick, d=ring_outer, $fn=60);
        // Inner hole for chamber
        translate([0, 0, -1])
            cylinder(h=ring_thick+2, d=ring_inner, $fn=60);
    }
}

module distributor_plate() {
    color("Gold", 0.6)
    translate([0, 0, plenum_z + plenum_depth + ring_thick])
        cylinder(h=plate_thick, d=plate_dia, $fn=60);
}

module chamber() {
    color("LightBlue", 0.5)
    translate([0, 0, plenum_z + plenum_depth + ring_thick + plate_thick])
    difference() {
        cylinder(h=chamber_length, d=chamber_od, $fn=60);
        translate([0, 0, -1])
            cylinder(h=chamber_length+2, d=chamber_id, $fn=60);
    }
}

module chaff_collector() {
    chamber_top_z = plenum_z + plenum_depth + ring_thick + plate_thick + chamber_length;

    // Expansion chamber body
    color("Plum", 0.5)
    translate([0, 0, chamber_top_z])
    difference() {
        cylinder(h=chaff_height, d=chaff_od, $fn=60);
        translate([0, 0, chaff_wall])
            cylinder(h=chaff_height, d=chaff_od - 2*chaff_wall, $fn=60);
    }

    // Mesh screen (thin disc near top)
    color("Gray", 0.4)
    translate([0, 0, chamber_top_z + chaff_height - 5])
        cylinder(h=1, d=chaff_od - 2*chaff_wall - 2, $fn=60);
}

module heater_can() {
    color("Tomato", 0.6)
    // Extends from plenum side-entry toward -X
    translate([-plenum_length/2, 0, plenum_z + side_entry_z])
    rotate([0, -90, 0])
    difference() {
        cylinder(h=heater_can_length, d=heater_can_od, $fn=40);
        translate([0, 0, -1])
            cylinder(h=heater_can_length+2, d=heater_can_od - 2*heater_can_wall, $fn=40);
    }
}

module blower() {
    color("CornflowerBlue", 0.7)
    // Positioned at the end of the heater can, extending further in -X
    blower_x = -plenum_length/2 - heater_can_length;
    translate([blower_x, 0, plenum_z + side_entry_z])
    rotate([0, -90, 0])
        cylinder(h=blower_depth, d=blower_dia, $fn=60);
}

// =============================================================
// Assembly
// =============================================================

// Center everything on the plenum position
translate([-(plenum_x - base_length/2), 0, 0]) {

    if (show_baseplate)       baseplate();
    if (show_standoffs)       standoffs();

    // Everything above is relative to plenum center
    translate([plenum_x - base_length/2, 0, 0]) {
        if (show_plenum)          plenum();
        if (show_baffle)          baffle();
        if (show_clamping_ring)   clamping_ring();
        if (show_distributor)     distributor_plate();
        if (show_chamber)         chamber();
        if (show_chaff_collector) chaff_collector();
        if (show_heater_can)      heater_can();
        if (show_blower)          blower();
    }
}

// =============================================================
// Annotations (console output)
// =============================================================

total_height = base_thick + standoff_height + plenum_depth + ring_thick +
               plate_thick + chamber_length + chaff_height;

echo(str("--- Assembly Summary ---"));
echo(str("Chamber OD: ", chamber_od, " mm (", chamber_od/25.4, " in)"));
echo(str("Base footprint: ", base_length, " x ", base_width, " mm (",
         base_length/25.4, " x ", base_width/25.4, " in)"));
echo(str("Total height above table: ", total_height, " mm (",
         total_height/25.4, " in)"));
echo(str("Heater+blower extension from plenum: ",
         plenum_length/2 + heater_can_length + blower_depth, " mm (",
         (plenum_length/2 + heater_can_length + blower_depth)/25.4, " in)"));
