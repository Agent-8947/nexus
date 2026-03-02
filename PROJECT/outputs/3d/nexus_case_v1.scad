// NEXUS-FORGE: Parametric Controller Case v1.0
// Language: OpenSCAD

$fn = 100;

// Dimensions
width = 60;
length = 100;
height = 25;
wall_thickness = 2;
corner_radius = 5;

// Logo Text
nexus_text = "NEXUS-V2";

module base_shape(w, l, h, r) {
    hull() {
        translate([r, r, 0]) cylinder(r=r, h=h);
        translate([w-r, r, 0]) cylinder(r=r, h=h);
        translate([r, l-r, 0]) cylinder(r=r, h=h);
        translate([w-r, l-r, 0]) cylinder(r=r, h=h);
    }
}

difference() {
    // Outer Shell
    base_shape(width, length, height, corner_radius);
    
    // Inner Cavity
    translate([wall_thickness, wall_thickness, wall_thickness])
        base_shape(width-wall_thickness*2, length-wall_thickness*2, height, corner_radius-wall_thickness);
        
    // Venting / Branding Cutout
    translate([width/2, length/2, -1])
        linear_extrude(height=wall_thickness+2)
            text(nexus_text, size=8, halign="center", valign="center", font="Arial:style=Bold");
            
    // Side Access Ports
    translate([-1, 10, 5]) cube([wall_thickness+2, 15, 10]); // USB port placeholder
}

// Internal Mounting Pillars
mount_radius = 2.5;
translate([8, 8, 0]) cylinder(r=mount_radius, h=5);
translate([width-8, 8, 0]) cylinder(r=mount_radius, h=5);
translate([8, length-8, 0]) cylinder(r=mount_radius, h=5);
translate([width-8, length-8, 0]) cylinder(r=mount_radius, h=5);
