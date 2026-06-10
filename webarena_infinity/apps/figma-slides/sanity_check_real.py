#!/usr/bin/env python3
"""
Sanity check for Figma Slides real-task verifiers.

For each task, directly constructs the expected end-state (bypassing the agent),
then runs the verifier and asserts it returns True.

Usage:
    python3 sanity_check_real.py                      # All tasks, sequential
    python3 sanity_check_real.py --workers N           # N parallel environments
    python3 sanity_check_real.py --task-id <id>        # Single task (for debugging)
    python3 sanity_check_real.py --port <base>         # Custom base port
"""
import argparse
import importlib.util
import json
import os
import socket
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

APP_DIR = Path(__file__).resolve().parent
TASKS_FILE = APP_DIR / "real-tasks.json"

# JS snippet to evaluate data.js and emit the seed state as JSON
_SEED_STATE_JS = """
const fs = require('fs');
const vm = require('vm');
const code = fs.readFileSync(process.argv[1], 'utf8');
vm.runInThisContext(code);

const state = {
    slides: JSON.parse(JSON.stringify(SLIDES)),
    deckSettings: JSON.parse(JSON.stringify(DECK_SETTINGS)),
    templateStyles: JSON.parse(JSON.stringify(TEMPLATE_STYLES)),
    comments: JSON.parse(JSON.stringify(COMMENTS)),
    libraries: JSON.parse(JSON.stringify(LIBRARIES)),
    collaborators: JSON.parse(JSON.stringify(COLLABORATORS)),
    currentUser: JSON.parse(JSON.stringify(CURRENT_USER)),
    exportHistory: JSON.parse(JSON.stringify(EXPORT_HISTORY)),
    versionHistory: JSON.parse(JSON.stringify(VERSION_HISTORY)),
    availableTemplates: JSON.parse(JSON.stringify(AVAILABLE_TEMPLATES)),
    _seedVersion: SEED_DATA_VERSION,
    _nextSlideOrder: 16,
    _nextCommentId: 7,
    _nextObjectId: 200
};
process.stdout.write(JSON.stringify(state));
"""


# ── helpers ──────────────────────────────────────────────────────────

def find_slide(state, title):
    for s in state["slides"]:
        if s["title"] == title:
            return s
    raise ValueError(f"Slide not found: {title}")


def find_object(slide, name):
    for o in slide["objects"]:
        if o["name"] == name:
            return o
    raise ValueError(f"Object '{name}' not found on slide '{slide['title']}'")


def find_object_by_type(slide, obj_type):
    for o in slide["objects"]:
        if o["type"] == obj_type:
            return o
    raise ValueError(f"Object of type '{obj_type}' not found on slide '{slide['title']}'")


def find_collaborator(state, name):
    for c in state["collaborators"]:
        if c["name"] == name:
            return c
    raise ValueError(f"Collaborator not found: {name}")


def find_comment_by_author(state, author_name, text_fragment=None):
    for c in state["comments"]:
        if c["userName"] == author_name:
            if text_fragment is None or text_fragment in c.get("text", ""):
                return c
    raise ValueError(f"Comment not found: author={author_name}, text contains '{text_fragment}'")


def find_library(state, name):
    for lib in state["libraries"]:
        if lib["name"] == name:
            return lib
    raise ValueError(f"Library not found: {name}")


def find_template_style(state, name=None, style_id=None):
    for ts in state["templateStyles"]:
        if name and ts["name"] == name:
            return ts
        if style_id and ts["id"] == style_id:
            return ts
    raise ValueError(f"Template style not found: name={name}, id={style_id}")


def find_color(template_style, color_name):
    for c in template_style["colors"]:
        if c["name"] == color_name:
            return c
    raise ValueError(f"Color '{color_name}' not found in template style '{template_style['name']}'")


def find_text_style(template_style, style_name):
    for ts in template_style["textStyles"]:
        if ts["name"] == style_name:
            return ts
    raise ValueError(f"Text style '{style_name}' not found in template style '{template_style['name']}'")


# ── solve functions ──────────────────────────────────────────────────

# Easy tasks

def solve_task_e1(state):
    """Skip the Competitive Landscape slide."""
    slide = find_slide(state, "Competitive Landscape")
    slide["skipped"] = True


def solve_task_e2(state):
    """Rename the presentation to 'Q4 2025 Strategy Update'."""
    state["deckSettings"]["name"] = "Q4 2025 Strategy Update"


def solve_task_e3(state):
    """Resolve Marcus's comment about the uptime number."""
    comment = find_comment_by_author(state, "Marcus Rivera", "uptime")
    comment["resolved"] = True


def solve_task_e4(state):
    """Remove Tom Nguyen from the collaborators."""
    state["collaborators"] = [c for c in state["collaborators"] if c["name"] != "Tom Nguyen"]


def solve_task_e5(state):
    """Disable the Presentation Icons Pack library."""
    lib = find_library(state, "Presentation Icons Pack")
    lib["enabled"] = False


def solve_task_e6(state):
    """Change the title slide's background color to #2D1B69."""
    slide = find_slide(state, "Q4 2025 Product Strategy")
    slide["background"] = {"type": "solid", "color": "#2D1B69"}


def solve_task_e7(state):
    """Rename the Q3 Review group to 'Q3 Performance'."""
    q3_titles = {"Q3 Highlights", "Growth Metrics", "Customer Feedback"}
    for s in state["slides"]:
        if s["title"] in q3_titles:
            s["groupName"] = "Q3 Performance"


def solve_task_e8(state):
    """Delete David Park's comment about the slide design."""
    state["comments"] = [
        c for c in state["comments"]
        if not (c["userName"] == "David Park" and "slide design" in c.get("text", ""))
    ]


def solve_task_e9(state):
    """Make the deck available offline."""
    state["deckSettings"]["availableOffline"] = True


def solve_task_e10(state):
    """Increase the section title font size to 72 on the Q4 Roadmap slide."""
    slide = find_slide(state, "Q4 Roadmap")
    obj = find_object(slide, "Section Title")
    obj["fontSize"] = 72


def solve_task_e11(state):
    """Lock the main title on the first slide."""
    slide = find_slide(state, "Q4 2025 Product Strategy")
    obj = find_object(slide, "Title")
    obj["locked"] = True


def solve_task_e12(state):
    """Unskip the Sprint Timeline slide."""
    slide = find_slide(state, "Sprint Timeline")
    slide["skipped"] = False


def solve_task_e13(state):
    """Switch the code example's theme to Dracula."""
    slide = find_slide(state, "API Reference")
    obj = find_object_by_type(slide, "code")
    obj["theme"] = "dracula"


def solve_task_e14(state):
    """Change the link sharing permission to 'can edit'."""
    state["deckSettings"]["shareSettings"]["linkRole"] = "can_edit"


def solve_task_e15(state):
    """Change James O'Brien's role to Editor."""
    collab = find_collaborator(state, "James O'Brien")
    collab["role"] = "Editor"


def solve_task_e16(state):
    """Remove the Brand Assets 2025 library."""
    state["libraries"] = [lib for lib in state["libraries"] if lib["name"] != "Brand Assets 2025"]


def solve_task_e17(state):
    """Rename the Agenda slide to 'Meeting Agenda'."""
    slide = find_slide(state, "Agenda")
    slide["title"] = "Meeting Agenda"


def solve_task_e18(state):
    """Set the presentation aspect ratio to 4:3."""
    state["deckSettings"]["aspectRatio"] = "4:3"
    state["deckSettings"]["width"] = 1024
    state["deckSettings"]["height"] = 768


def solve_task_e19(state):
    """Disable slide numbers on the Thank You slide."""
    slide = find_slide(state, "Thank You")
    slide["slideNumberEnabled"] = False


def solve_task_e20(state):
    """Change the Thank You slide's transition type to push."""
    slide = find_slide(state, "Thank You")
    slide["transition"]["type"] = "push"
    slide["transition"]["direction"] = "left"


# Medium tasks

def solve_task_m1(state):
    """Change Aiko Tanaka's role to Viewer and remove Elena Kowalski."""
    collab = find_collaborator(state, "Aiko Tanaka")
    collab["role"] = "Viewer"
    state["collaborators"] = [c for c in state["collaborators"] if c["name"] != "Elena Kowalski"]


def solve_task_m2(state):
    """Resolve all open comments."""
    for c in state["comments"]:
        c["resolved"] = True


def solve_task_m3(state):
    """Switch Customer Feedback bg to solid #1A1A2E and transition to smart animate."""
    slide = find_slide(state, "Customer Feedback")
    slide["background"] = {"type": "solid", "color": "#1A1A2E"}
    slide["transition"]["type"] = "smart_animate"


def solve_task_m4(state):
    """Add fade-in animation to Action Items and lock it."""
    slide = find_slide(state, "Next Steps")
    obj = find_object(slide, "Action Items")
    obj["animation"] = {
        "style": "fade",
        "duration": 400,
        "timing": "on_click",
        "direction": "in",
        "order": 0
    }
    obj["locked"] = True


def solve_task_m5(state):
    """Change code example language to Python and theme to GitHub."""
    slide = find_slide(state, "API Reference")
    obj = find_object_by_type(slide, "code")
    obj["language"] = "Python"
    obj["theme"] = "github"


def solve_task_m6(state):
    """Rename Minimal Dark to 'Dark Mode Pro' and Primary color to #6C5CE7."""
    ts = find_template_style(state, style_id="ts_001")
    ts["name"] = "Dark Mode Pro"
    color = find_color(ts, "Primary")
    color["value"] = "#6C5CE7"


def solve_task_m7(state):
    """Turn off copy and download in share settings."""
    state["deckSettings"]["shareSettings"]["allowCopy"] = False
    state["deckSettings"]["shareSettings"]["allowDownload"] = False


def solve_task_m8(state):
    """Remove all Viewer collaborators."""
    state["collaborators"] = [c for c in state["collaborators"] if c["role"] != "Viewer"]


def solve_task_m9(state):
    """Update feature adoption table cells."""
    slide = find_slide(state, "Data Comparison")
    obj = find_object(slide, "Adoption Table")
    obj["cells"][1][3] = "85%"
    obj["cells"][2][4] = "65%"


def solve_task_m10(state):
    """Delete Sprint Timeline slide and resolve Elena's comment."""
    state["slides"] = [s for s in state["slides"] if s["title"] != "Sprint Timeline"]
    # Reorder remaining slides
    ordered = sorted(state["slides"], key=lambda s: s["order"])
    for i, s in enumerate(ordered):
        s["order"] = i
    # Remove comments on deleted slide
    state["comments"] = [c for c in state["comments"] if c["slideId"] != "slide_012"]
    # Resolve Elena's comment
    comment = find_comment_by_author(state, "Elena Kowalski", "Mobile team")
    comment["resolved"] = True


def solve_task_m11(state):
    """Q4 Roadmap section bg to #0052CC and subtitle text."""
    slide = find_slide(state, "Q4 Roadmap")
    slide["background"] = {"type": "solid", "color": "#0052CC"}
    obj = find_object(slide, "Section Subtitle")
    obj["text"] = "Building the next generation"


def solve_task_m12(state):
    """Enable slide numbers on Thank You with 'with total' format."""
    slide = find_slide(state, "Thank You")
    slide["slideNumberEnabled"] = True
    slide["slideNumberFormat"] = "with_total"


def solve_task_m13(state):
    """Vote for AI features in poll, submit confidence 5."""
    slide = find_slide(state, "Team Survey Results")
    for obj in slide["objects"]:
        if obj.get("type") == "liveInteraction":
            if obj.get("interactionType") == "poll":
                for opt in obj["options"]:
                    if opt["text"] == "AI features":
                        opt["votes"] += 1
            elif obj.get("interactionType") == "alignment":
                obj["responses"].append({"userId": "user_001", "value": 5})


def solve_task_m14(state):
    """Disable all three libraries."""
    for lib in state["libraries"]:
        lib["enabled"] = False


def solve_task_m15(state):
    """Change closing title to 'Questions?' and font size to 48."""
    slide = find_slide(state, "Thank You")
    obj = find_object(slide, "Closing Title")
    obj["text"] = "Questions?"
    obj["fontSize"] = 48


def solve_task_m16(state):
    """Add slide-up animation (800ms) to comparison table."""
    slide = find_slide(state, "Competitive Landscape")
    obj = find_object(slide, "Comparison Table")
    obj["animation"] = {
        "style": "slide_up",
        "duration": 800,
        "timing": "on_click",
        "direction": "in",
        "order": 0
    }


def solve_task_m17(state):
    """Set link access to 'anyone' and role to 'can edit'."""
    state["deckSettings"]["shareSettings"]["linkAccess"] = "anyone"
    state["deckSettings"]["shareSettings"]["linkRole"] = "can_edit"


def solve_task_m18(state):
    """Rename Q4 Planning group to 'Product Roadmap' and section bg."""
    for s in state["slides"]:
        if s.get("groupName") == "Q4 Planning":
            s["groupName"] = "Product Roadmap"
    slide = find_slide(state, "Q4 Roadmap")
    slide["background"] = {"type": "solid", "color": "#0D1B2A"}


def solve_task_m19(state):
    """Delete James's comment, resolve Aiko's comment."""
    state["comments"] = [
        c for c in state["comments"]
        if not (c["userName"] == "James O'Brien" and "competitive" in c.get("text", "").lower())
    ]
    comment = find_comment_by_author(state, "Aiko Tanaka", "token")
    comment["resolved"] = True


def solve_task_m20(state):
    """Change default deck transition to push, left, 600ms."""
    state["deckSettings"]["defaultTransition"] = {
        "type": "push",
        "direction": "left",
        "easing": "ease",
        "duration": 600,
        "timing": "immediately"
    }


# Hard tasks

def solve_task_h1(state):
    """Update Q3 metric cards: 2.8M +40%, $22.3M +35%, fill #383838."""
    slide = find_slide(state, "Q3 Highlights")
    card1 = find_object(slide, "Metric Card 1")
    card2 = find_object(slide, "Metric Card 2")
    card3 = find_object(slide, "Metric Card 3")
    card1["text"] = "2.8M\nActive Users\n+40% YoY"
    card2["text"] = "$22.3M\nARR\n+35% YoY"
    card1["fill"] = "#383838"
    card2["fill"] = "#383838"
    card3["fill"] = "#383838"


def solve_task_h2(state):
    """Remove everyone offline from collaborators."""
    state["collaborators"] = [c for c in state["collaborators"] if c.get("online") is not False]


def solve_task_h3(state):
    """Switch Q3 Review slides to Corporate Blue + white backgrounds."""
    q3_titles = {"Q3 Highlights", "Growth Metrics", "Customer Feedback"}
    for s in state["slides"]:
        if s["title"] in q3_titles:
            s["templateStyle"] = "ts_002"
            s["background"] = {"type": "solid", "color": "#FFFFFF"}


def solve_task_h4(state):
    """Lock all title slide objects, disable page number, dissolve 800ms."""
    slide = find_slide(state, "Q4 2025 Product Strategy")
    for obj in slide["objects"]:
        obj["locked"] = True
    slide["slideNumberEnabled"] = False
    slide["transition"] = {
        "type": "dissolve",
        "direction": None,
        "easing": "ease",
        "duration": 800,
        "timing": "immediately"
    }


def solve_task_h5(state):
    """Delete resolved comments, resolve remaining."""
    state["comments"] = [c for c in state["comments"] if c.get("resolved") is not True]
    for c in state["comments"]:
        c["resolved"] = True


def solve_task_h6(state):
    """Replace every dissolve transition with push-left."""
    for s in state["slides"]:
        if s.get("transition", {}).get("type") == "dissolve":
            s["transition"]["type"] = "push"
            s["transition"]["direction"] = "left"


def solve_task_h7(state):
    """Update competitive comparison table cells."""
    slide = find_slide(state, "Competitive Landscape")
    obj = find_object(slide, "Comparison Table")
    obj["cells"][2][2] = "Native"       # Design Tokens, Competitor A
    obj["cells"][4][3] = "In Beta"      # AI Features, Competitor B
    obj["cells"][5][1] = "$12/user/mo"  # Pricing, DesignCraft


def solve_task_h8(state):
    """Rename deck, Q4 Planning group, and section title."""
    state["deckSettings"]["name"] = "Q4 2025 Product Roadmap"
    for s in state["slides"]:
        if s.get("groupName") == "Q4 Planning":
            s["groupName"] = "Product Roadmap"
    slide = find_slide(state, "Q4 Roadmap")
    obj = find_object(slide, "Section Title")
    obj["text"] = "Product Roadmap"


def solve_task_h9(state):
    """Remove Viewers, restrict sharing, disable copy/download."""
    state["collaborators"] = [c for c in state["collaborators"] if c["role"] != "Viewer"]
    state["deckSettings"]["shareSettings"]["linkAccess"] = "restricted"
    state["deckSettings"]["shareSettings"]["allowCopy"] = False
    state["deckSettings"]["shareSettings"]["allowDownload"] = False


def solve_task_h10(state):
    """Add bounce animations to all three team cards."""
    slide = find_slide(state, "Resource Allocation")
    for card_name in ("Team A Card", "Team B Card", "Team C Card"):
        obj = find_object(slide, card_name)
        obj["animation"] = {
            "style": "bounce",
            "duration": 500,
            "timing": "on_click",
            "direction": "in",
            "order": 0
        }


def solve_task_h11(state):
    """Change code example to TypeScript, GitHub theme, font size 16."""
    slide = find_slide(state, "API Reference")
    obj = find_object_by_type(slide, "code")
    obj["language"] = "TypeScript"
    obj["theme"] = "github"
    obj["fontSize"] = 16


def solve_task_h12(state):
    """Delete comments from Viewers, resolve comments from Editors."""
    # In seed data, Viewers are: James O'Brien (user_004), Tom Nguyen (user_006)
    viewer_ids = {"user_004", "user_006"}
    state["comments"] = [c for c in state["comments"] if c["userId"] not in viewer_ids]
    for c in state["comments"]:
        c["resolved"] = True


def solve_task_h13(state):
    """Apply Corporate Blue to ungrouped slides and set as deck default."""
    for s in state["slides"]:
        if s.get("groupId") is None:
            s["templateStyle"] = "ts_002"
    state["deckSettings"]["defaultTemplateStyle"] = "ts_002"


def solve_task_h14(state):
    """Lock risk cards, corner radius 16, fade animation 400ms."""
    slide = find_slide(state, "Key Risks & Mitigations")
    for risk_name in ("Risk 1", "Risk 2", "Risk 3"):
        obj = find_object(slide, risk_name)
        obj["locked"] = True
        obj["cornerRadius"] = 16
        obj["animation"] = {
            "style": "fade",
            "duration": 400,
            "timing": "on_click",
            "direction": "in",
            "order": 0
        }


def solve_task_h15(state):
    """Remove Presentation Icons Pack, disable DesignCraft, delete comments on Competitive Landscape."""
    state["libraries"] = [lib for lib in state["libraries"] if lib["name"] != "Presentation Icons Pack"]
    lib = find_library(state, "DesignCraft Component Library")
    lib["enabled"] = False
    # Find the Competitive Landscape slide ID
    comp_slide = find_slide(state, "Competitive Landscape")
    slide_id = comp_slide["id"]
    state["comments"] = [c for c in state["comments"] if c["slideId"] != slide_id]


def solve_task_h16(state):
    """Enable slide numbers on all slides with 'with total', aspect ratio 4:3."""
    for s in state["slides"]:
        s["slideNumberEnabled"] = True
        s["slideNumberFormat"] = "with_total"
    state["deckSettings"]["aspectRatio"] = "4:3"
    state["deckSettings"]["width"] = 1024
    state["deckSettings"]["height"] = 768


def solve_task_h17(state):
    """Increase Q3 2025 adoption values by 5 points."""
    slide = find_slide(state, "Data Comparison")
    obj = find_object(slide, "Adoption Table")
    obj["cells"][1][3] = "86%"
    obj["cells"][2][3] = "46%"
    obj["cells"][3][3] = "63%"
    obj["cells"][4][3] = "27%"
    obj["cells"][5][3] = "72%"


def solve_task_h18(state):
    """Remove animations from title slide, add scale to Q4 Roadmap title."""
    slide = find_slide(state, "Q4 2025 Product Strategy")
    for obj in slide["objects"]:
        obj["animation"] = None
    q4_slide = find_slide(state, "Q4 Roadmap")
    section_title = find_object(q4_slide, "Section Title")
    section_title["animation"] = {
        "style": "scale",
        "duration": 500,
        "timing": "on_click",
        "direction": "in",
        "order": 0
    }


def solve_task_h19(state):
    """Rename Warm Sunset to 'Sunset Red', Primary to #E63946, remove Caption."""
    ts = find_template_style(state, style_id="ts_003")
    ts["name"] = "Sunset Red"
    color = find_color(ts, "Primary")
    color["value"] = "#E63946"
    ts["textStyles"] = [t for t in ts["textStyles"] if t["name"] != "Caption"]


def solve_task_h20(state):
    """Delete Sprint Timeline, resolve all comments, restrict sharing."""
    state["slides"] = [s for s in state["slides"] if s["title"] != "Sprint Timeline"]
    # Reorder remaining slides
    ordered = sorted(state["slides"], key=lambda s: s["order"])
    for i, s in enumerate(ordered):
        s["order"] = i
    # Remove comments on deleted slide
    state["comments"] = [c for c in state["comments"] if c["slideId"] != "slide_012"]
    # Resolve all remaining comments
    for c in state["comments"]:
        c["resolved"] = True
    state["deckSettings"]["shareSettings"]["linkAccess"] = "restricted"
    state["deckSettings"]["shareSettings"]["linkRole"] = "can_view"


def solve_task_h21(state):
    """Q4 Roadmap: gradient bg, subtitle text, smart_animate transition."""
    slide = find_slide(state, "Q4 Roadmap")
    slide["background"] = {
        "type": "gradient",
        "gradient": {
            "type": "linear",
            "angle": 180,
            "stops": [
                {"color": "#0A0A2A", "position": 0},
                {"color": "#1E1E1E", "position": 100}
            ]
        }
    }
    obj = find_object(slide, "Section Subtitle")
    obj["text"] = "Innovation Starts Here"
    slide["transition"]["type"] = "smart_animate"
    slide["transition"]["direction"] = None
    slide["transition"]["duration"] = 600


def solve_task_h22(state):
    """Dissolve->slide_in right; push->spring easing 600ms."""
    for s in state["slides"]:
        trans = s.get("transition", {})
        if trans.get("type") == "dissolve":
            trans["type"] = "slide_in"
            trans["direction"] = "right"
        elif trans.get("type") == "push":
            trans["easing"] = "spring"
            trans["duration"] = 600


def solve_task_h23(state):
    """At-risk team card fill + animation; team lead role to Viewer."""
    slide = find_slide(state, "Resource Allocation")
    obj = find_object(slide, "Team B Card")
    obj["fill"] = "#1A1A2E"
    obj["animation"] = {
        "style": "pop",
        "duration": 500,
        "timing": "on_click",
        "direction": "in",
        "order": 0
    }
    collab = find_collaborator(state, "Marcus Rivera")
    collab["role"] = "Viewer"


def solve_task_h24(state):
    """YoY cards get stroke; SLA card gets fill change."""
    slide = find_slide(state, "Q3 Highlights")
    for card_name in ("Metric Card 1", "Metric Card 2"):
        obj = find_object(slide, card_name)
        obj["stroke"] = {"color": "#0ACF83", "width": 2}
    obj3 = find_object(slide, "Metric Card 3")
    obj3["fill"] = "#F24E1E"


def solve_task_h25(state):
    """Skip slides with unresolved comments; restrict link access."""
    slides_with_unresolved = set()
    for c in state["comments"]:
        if c.get("resolved") is not True:
            slides_with_unresolved.add(c["slideId"])
    for s in state["slides"]:
        if s["id"] in slides_with_unresolved:
            s["skipped"] = True
    state["deckSettings"]["shareSettings"]["linkAccess"] = "restricted"


def solve_task_h26(state):
    """Remove no-styles library; code theme solarized; Thank You push-bottom."""
    state["libraries"] = [
        lib for lib in state["libraries"]
        if not (lib.get("styleCount", 0) == 0 and lib.get("variableCount", 0) == 0)
    ]
    slide = find_slide(state, "API Reference")
    obj = find_object_by_type(slide, "code")
    obj["theme"] = "solarized"
    ty_slide = find_slide(state, "Thank You")
    ty_slide["transition"]["type"] = "push"
    ty_slide["transition"]["direction"] = "bottom"
    ty_slide["transition"]["duration"] = 500


def solve_task_h27(state):
    """Title slide: animated objects opacity 80; non-animated locked."""
    slide = find_slide(state, "Q4 2025 Product Strategy")
    for obj in slide["objects"]:
        if obj.get("animation") is not None:
            obj["opacity"] = 80
        else:
            obj["locked"] = True


def solve_task_h28(state):
    """Deck defaults: Corporate Blue, move_in/top/ease_in, with_total."""
    state["deckSettings"]["defaultTemplateStyle"] = "ts_002"
    state["deckSettings"]["defaultTransition"] = {
        "type": "move_in",
        "direction": "top",
        "easing": "ease_in",
        "duration": 400,
        "timing": "immediately"
    }
    state["deckSettings"]["slideNumberFormat"] = "with_total"


def solve_task_h29(state):
    """Q3 Review Title objects: Georgia, fontWeight 600."""
    q3_titles = {"Q3 Highlights", "Growth Metrics"}
    for s in state["slides"]:
        if s["title"] in q3_titles:
            for obj in s["objects"]:
                if obj["name"] == "Title":
                    obj["fontFamily"] = "Georgia"
                    obj["fontWeight"] = 600


def solve_task_h30(state):
    """Resolve offline collaborators' comments; rename Warm Sunset."""
    offline_ids = {"user_004", "user_005", "user_007"}
    for c in state["comments"]:
        if c["userId"] in offline_ids:
            c["resolved"] = True
    ts = find_template_style(state, style_id="ts_003")
    ts["name"] = "Coral Reef"


def solve_task_h31(state):
    """Adoption table '--' to '0%'; comparison 'None'->'Planned', 'Limited'->'Partial'."""
    slide = find_slide(state, "Data Comparison")
    table = find_object(slide, "Adoption Table")
    for r, row in enumerate(table["cells"]):
        for c, val in enumerate(row):
            if val == "--":
                table["cells"][r][c] = "0%"

    comp_slide = find_slide(state, "Competitive Landscape")
    comp_table = find_object(comp_slide, "Comparison Table")
    for r, row in enumerate(comp_table["cells"]):
        for c, val in enumerate(row):
            if val == "None":
                comp_table["cells"][r][c] = "Planned"
            elif val == "Limited":
                comp_table["cells"][r][c] = "Partial"


def solve_task_h32(state):
    """Lock adoption table; comparison table header bg #0052CC."""
    slide = find_slide(state, "Data Comparison")
    table = find_object(slide, "Adoption Table")
    table["locked"] = True

    comp_slide = find_slide(state, "Competitive Landscape")
    comp_table = find_object(comp_slide, "Comparison Table")
    comp_table["headerStyle"]["background"] = "#0052CC"


def solve_task_h33(state):
    """Online Editors to Viewer; delete resolved comments."""
    online_editor_names = {"Marcus Rivera", "Aiko Tanaka", "David Park"}
    for c in state["collaborators"]:
        if c["name"] in online_editor_names:
            c["role"] = "Viewer"
    state["comments"] = [c for c in state["comments"] if c.get("resolved") is not True]


def solve_task_h34(state):
    """Customer Feedback: remove all animations, add slide_left to Attribution."""
    slide = find_slide(state, "Customer Feedback")
    for obj in slide["objects"]:
        obj["animation"] = None
    attr = find_object(slide, "Attribution")
    attr["animation"] = {
        "style": "slide_left",
        "duration": 500,
        "timing": "after_previous",
        "direction": "in",
        "order": 0
    }


def solve_task_h35(state):
    """Ungrouped slides: gradient bg, dissolve 500ms."""
    for s in state["slides"]:
        if s.get("groupId") is None:
            s["background"] = {
                "type": "gradient",
                "gradient": {
                    "type": "linear",
                    "angle": 180,
                    "stops": [
                        {"color": "#1E1E1E", "position": 0},
                        {"color": "#2D1B69", "position": 100}
                    ]
                }
            }
            s["transition"]["type"] = "dissolve"
            s["transition"]["direction"] = None
            s["transition"]["duration"] = 500


def solve_task_h36(state):
    """Swap Q2 (col 2) and Q3 (col 3) in adoption table."""
    slide = find_slide(state, "Data Comparison")
    table = find_object(slide, "Adoption Table")
    for r in range(1, len(table["cells"])):
        table["cells"][r][2], table["cells"][r][3] = table["cells"][r][3], table["cells"][r][2]


def solve_task_h37(state):
    """Offline prep: offline=true, disable libs, remove Viewers, padded format."""
    state["deckSettings"]["availableOffline"] = True
    for lib in state["libraries"]:
        lib["enabled"] = False
    state["collaborators"] = [c for c in state["collaborators"] if c["role"] != "Viewer"]
    state["deckSettings"]["slideNumberFormat"] = "padded"


def solve_task_h38(state):
    """Design System 2.0 badges: text + fill changes."""
    slide = find_slide(state, "Design System 2.0")
    timeline = find_object(slide, "Timeline Badge")
    timeline["text"] = "Beta: Dec 2025"
    timeline["fill"] = "#F24E1E"
    ga = find_object(slide, "GA Badge")
    ga["text"] = "GA: Mar 2026"
    ga["fill"] = "#FF6B35"


def solve_task_h39(state):
    """Add pop animation to Title objects in Q4 Planning that lack one."""
    q4_titles = {"Design System 2.0", "API Reference", "Team Survey Results", "Data Comparison"}
    for s in state["slides"]:
        if s["title"] in q4_titles:
            for obj in s["objects"]:
                if obj["name"] == "Title" and obj.get("animation") is None:
                    obj["animation"] = {
                        "style": "pop",
                        "duration": 300,
                        "timing": "on_click",
                        "direction": "in",
                        "order": 0
                    }


def solve_task_h40(state):
    """Team Updates: Corporate Blue, white bg, move_in bottom; remove Elena."""
    team_updates_titles = {"Resource Allocation", "Sprint Timeline"}
    for s in state["slides"]:
        if s["title"] in team_updates_titles:
            s["templateStyle"] = "ts_002"
            s["background"] = {"type": "solid", "color": "#FFFFFF"}
            s["transition"] = {
                "type": "move_in",
                "direction": "bottom",
                "easing": "ease",
                "duration": 400,
                "timing": "immediately"
            }
    state["collaborators"] = [c for c in state["collaborators"] if c["name"] != "Elena Kowalski"]


def solve_task_h41(state):
    """Sensitive slide (Competitive Landscape): skip, lock all, disable slide numbers."""
    slide = find_slide(state, "Competitive Landscape")
    slide["skipped"] = True
    for obj in slide["objects"]:
        obj["locked"] = True
    slide["slideNumberEnabled"] = False


def solve_task_h42(state):
    """Remove commenter who flagged outdated competitive data; flag table header."""
    state["collaborators"] = [c for c in state["collaborators"] if c["name"] != "James O'Brien"]
    slide = find_slide(state, "Competitive Landscape")
    obj = find_object(slide, "Comparison Table")
    obj["headerStyle"]["background"] = "#F24E1E"


def solve_task_h43(state):
    """Q4 Planning content-type standardization."""
    slide = find_slide(state, "API Reference")
    obj = find_object_by_type(slide, "code")
    obj["theme"] = "solarized"

    slide = find_slide(state, "Data Comparison")
    obj = find_object(slide, "Adoption Table")
    obj["headerStyle"]["background"] = "#172B4D"

    slide = find_slide(state, "Team Survey Results")
    for obj in slide["objects"]:
        if obj.get("type") == "liveInteraction":
            obj["hideResults"] = True


def solve_task_h44(state):
    """Flag Metric Card 3 with stroke (below SLA); resolve uptime comment."""
    slide = find_slide(state, "Q3 Highlights")
    obj = find_object(slide, "Metric Card 3")
    obj["stroke"] = {"color": "#F24E1E", "width": 2}
    comment = find_comment_by_author(state, "Marcus Rivera", "uptime")
    comment["resolved"] = True


def solve_task_h45(state):
    """Highest priority slide (Design System 2.0): Corporate Blue, white bg, push left."""
    slide = find_slide(state, "Design System 2.0")
    slide["templateStyle"] = "ts_002"
    slide["background"] = {"type": "solid", "color": "#FFFFFF"}
    slide["transition"] = {
        "type": "push",
        "direction": "left",
        "easing": "ease_in",
        "duration": 600,
        "timing": "immediately"
    }


def solve_task_h46(state):
    """Lock competitive comparison table; Adoption Table fontSize to 16."""
    slide = find_slide(state, "Competitive Landscape")
    obj = find_object(slide, "Comparison Table")
    obj["locked"] = True

    slide = find_slide(state, "Data Comparison")
    obj = find_object(slide, "Adoption Table")
    obj["fontSize"] = 16


def solve_task_h47(state):
    """Animated slides: ease_in_out easing. Non-animated slides: transition none."""
    for s in state["slides"]:
        has_animation = any(
            obj.get("animation") is not None for obj in s.get("objects", [])
        )
        if has_animation:
            s["transition"]["easing"] = "ease_in_out"
        else:
            s["transition"]["type"] = "none"


def solve_task_h48(state):
    """Planning team card (Team C): fill #3D1010, stroke #FF6B6B, pop animation."""
    slide = find_slide(state, "Resource Allocation")
    obj = find_object(slide, "Team C Card")
    obj["fill"] = "#3D1010"
    obj["stroke"] = {"color": "#FF6B6B", "width": 2}
    obj["animation"] = {
        "style": "pop",
        "duration": 600,
        "timing": "on_click",
        "direction": "in",
        "order": 0
    }


def solve_task_h49(state):
    """Disable most-components library; remove library with pending updates."""
    lib = find_library(state, "Presentation Icons Pack")
    lib["enabled"] = False
    state["libraries"] = [
        lib for lib in state["libraries"]
        if lib["name"] != "DesignCraft Component Library"
    ]


def solve_task_h50(state):
    """Thank You: Closing Title text + weight; hide Reaction Stamps."""
    slide = find_slide(state, "Thank You")
    obj = find_object(slide, "Closing Title")
    obj["text"] = "Questions & Discussion"
    obj["fontWeight"] = 800
    stamps = find_object(slide, "Reaction Stamps")
    stamps["visible"] = False


def solve_task_h51(state):
    """Reverse all directional transition directions."""
    reverse_map = {"left": "right", "right": "left", "top": "bottom", "bottom": "top"}
    directional_types = {"push", "slide_in", "slide_out", "move_in", "move_out"}
    for s in state["slides"]:
        trans = s.get("transition", {})
        if trans.get("type") in directional_types and trans.get("direction") in reverse_map:
            trans["direction"] = reverse_map[trans["direction"]]


def solve_task_h52(state):
    """Risk cards: HIGH->#5C1010, MED->#5C3D10, LOW unchanged; push top spring 500ms."""
    slide = find_slide(state, "Key Risks & Mitigations")
    find_object(slide, "Risk 1")["fill"] = "#5C1010"
    find_object(slide, "Risk 2")["fill"] = "#5C3D10"
    slide["transition"] = {
        "type": "push",
        "direction": "top",
        "easing": "spring",
        "duration": 500,
        "timing": "immediately"
    }


def solve_task_h53(state):
    """Title text with winning poll option; poll question to closed."""
    slide = find_slide(state, "Team Survey Results")
    title_obj = find_object(slide, "Title")
    title_obj["text"] = "Team Survey Results \u2014 AI features"
    for obj in slide["objects"]:
        if obj.get("type") == "liveInteraction" and obj.get("interactionType") == "poll":
            obj["question"] = "Q4 Priorities (Closed)"


def solve_task_h54(state):
    """Q4 Roadmap: notes, Section Title rotation+align, Subtitle opacity."""
    slide = find_slide(state, "Q4 Roadmap")
    slide["presenterNotes"] = "Key deliverables and milestones for Q4."
    section_title = find_object(slide, "Section Title")
    section_title["rotation"] = -5
    section_title["textAlign"] = "left"
    section_subtitle = find_object(slide, "Section Subtitle")
    section_subtitle["opacity"] = 60


def solve_task_h55(state):
    """All objects named exactly 'Title' -> color #A78BFA."""
    for s in state["slides"]:
        for obj in s["objects"]:
            if obj["name"] == "Title":
                obj["color"] = "#A78BFA"


def solve_task_h56(state):
    """Borrowing team (Team C) stroke #FFAC33; lending team (Team B) stroke #FF6B6B."""
    slide = find_slide(state, "Resource Allocation")
    team_c = find_object(slide, "Team C Card")
    team_c["stroke"] = {"color": "#FFAC33", "width": 2}
    team_b = find_object(slide, "Team B Card")
    team_b["stroke"] = {"color": "#FF6B6B", "width": 2}


def solve_task_h57(state):
    """Offline Editors with unresolved comments: resolve + Viewer."""
    for c in state["comments"]:
        if c["userId"] == "user_007" and c.get("resolved") is not True:
            c["resolved"] = True
    collab = find_collaborator(state, "Elena Kowalski")
    collab["role"] = "Viewer"


def solve_task_h58(state):
    """Deck defaults: Warm Sunset, slide_out/bottom/bounce/500ms; Minimal Dark slides: with_total."""
    state["deckSettings"]["defaultTemplateStyle"] = "ts_003"
    state["deckSettings"]["defaultTransition"] = {
        "type": "slide_out",
        "direction": "bottom",
        "easing": "bounce",
        "duration": 500,
        "timing": "immediately"
    }
    for s in state["slides"]:
        if s.get("templateStyle") == "ts_001":
            s["slideNumberFormat"] = "with_total"


def solve_task_h59(state):
    """Growth Metrics Right Column: weight 700, size 18; notes update."""
    slide = find_slide(state, "Growth Metrics")
    obj = find_object(slide, "Right Column")
    obj["fontWeight"] = 700
    obj["fontSize"] = 18
    slide["presenterNotes"] = "Enterprise growth is our Q4 focus area."


def solve_task_h60(state):
    """Shapes with cornerRadius: +4. Shapes with 'Status' in text: fontWeight 700."""
    for s in state["slides"]:
        for obj in s["objects"]:
            if obj.get("type") == "shape" and obj.get("cornerRadius") is not None:
                obj["cornerRadius"] += 4
            if obj.get("type") == "shape" and "Status" in obj.get("text", ""):
                obj["fontWeight"] = 700


def solve_task_h61(state):
    """Group-based transition standardization."""
    for s in state["slides"]:
        group = s.get("groupName")
        if group == "Q3 Review":
            s["transition"] = {
                "type": "smart_animate", "direction": None,
                "easing": "ease_in_out", "duration": 500, "timing": "immediately"
            }
        elif group == "Q4 Planning":
            s["transition"] = {
                "type": "push", "direction": "left",
                "easing": "spring", "duration": 600, "timing": "immediately"
            }
        elif group == "Team Updates":
            s["transition"] = {
                "type": "move_in", "direction": "bottom",
                "easing": "bounce", "duration": 400, "timing": "immediately"
            }
        else:
            s["transition"] = {
                "type": "dissolve", "direction": None,
                "easing": "ease", "duration": 400, "timing": "immediately"
            }


def solve_task_h62(state):
    """Alignment survey confidence <= 3 -> Viewer; hide poll + alignment results."""
    low_confidence_ids = set()
    for s in state["slides"]:
        if s["title"] == "Team Survey Results":
            for obj in s["objects"]:
                if obj.get("type") == "liveInteraction":
                    if obj.get("interactionType") == "alignment":
                        for resp in obj.get("responses", []):
                            if resp.get("value", 10) <= 3:
                                low_confidence_ids.add(resp["userId"])
                    obj["hideResults"] = True
            break

    for c in state["collaborators"]:
        if c["id"] in low_confidence_ids:
            c["role"] = "Viewer"


def solve_task_h63(state):
    """Append ' [REVIEW]' to slides with unresolved comments; resolve all."""
    slides_with_unresolved = set()
    for c in state["comments"]:
        if c.get("resolved") is not True:
            slides_with_unresolved.add(c["slideId"])

    for s in state["slides"]:
        if s["id"] in slides_with_unresolved:
            s["title"] = s["title"] + " [REVIEW]"

    for c in state["comments"]:
        c["resolved"] = True


def solve_task_h64(state):
    """Swap HIGH and LOW risk card fills."""
    slide = find_slide(state, "Key Risks & Mitigations")
    risk1 = find_object(slide, "Risk 1")
    risk3 = find_object(slide, "Risk 3")
    risk1["fill"], risk3["fill"] = risk3["fill"], risk1["fill"]


def solve_task_h65(state):
    """Animated slides -> gradient bg; non-animated -> solid #2C2C2C."""
    import copy
    gradient_bg = {
        "type": "gradient",
        "gradient": {
            "type": "linear",
            "angle": 180,
            "stops": [
                {"color": "#0A0A2A", "position": 0},
                {"color": "#1E1E1E", "position": 100}
            ]
        }
    }
    solid_bg = {"type": "solid", "color": "#2C2C2C"}

    for s in state["slides"]:
        has_anim = any(
            obj.get("animation") is not None for obj in s.get("objects", [])
        )
        s["background"] = copy.deepcopy(gradient_bg) if has_anim else dict(solid_bg)


def solve_task_h66(state):
    """Largest team (Team A, 8 eng) -> gold stroke; smallest (Team C, 4 eng) -> fill."""
    slide = find_slide(state, "Resource Allocation")
    team_a = find_object(slide, "Team A Card")
    team_a["stroke"]["color"] = "#F7C948"
    team_c = find_object(slide, "Team C Card")
    team_c["fill"] = "#1A1A2E"


def solve_task_h67(state):
    """Hide all live interactions; dissolve 800ms on affected slides."""
    affected_slide_ids = set()
    for s in state["slides"]:
        for obj in s["objects"]:
            if obj.get("type") == "liveInteraction":
                obj["visible"] = False
                affected_slide_ids.add(s["id"])

    for s in state["slides"]:
        if s["id"] in affected_slide_ids:
            s["transition"]["type"] = "dissolve"
            s["transition"]["direction"] = None
            s["transition"]["duration"] = 800


def solve_task_h68(state):
    """Shapes with stroke: +1 width. Shapes without: add {#404040, 1}."""
    for s in state["slides"]:
        for obj in s["objects"]:
            if obj.get("type") == "shape":
                stroke = obj.get("stroke")
                if stroke and isinstance(stroke, dict) and "width" in stroke:
                    stroke["width"] += 1
                else:
                    obj["stroke"] = {"color": "#404040", "width": 1}


def solve_task_h69(state):
    """Cross-reference adoption Q3 values into competitive table."""
    comp_slide = find_slide(state, "Competitive Landscape")
    comp_table = find_object(comp_slide, "Comparison Table")
    comp_table["cells"][1][1] = "Full (81%)"
    comp_table["cells"][2][1] = "Native (41%)"


def solve_task_h70(state):
    """Q3 Review text objects: add fade 400ms if no anim; set duration 600ms if has."""
    q3_titles = {"Q3 Highlights", "Growth Metrics", "Customer Feedback"}
    for s in state["slides"]:
        if s["title"] in q3_titles:
            for obj in s["objects"]:
                if obj.get("type") != "text":
                    continue
                if obj.get("animation") is None:
                    obj["animation"] = {
                        "style": "fade", "duration": 400,
                        "timing": "after_previous", "direction": "in", "order": 0
                    }
                else:
                    obj["animation"]["duration"] = 600


def solve_task_h71(state):
    """Unresolved commenters -> red avatar; resolved-only -> green avatar."""
    has_unresolved = set()
    has_comment = set()
    for c in state["comments"]:
        has_comment.add(c["userId"])
        if c.get("resolved") is not True:
            has_unresolved.add(c["userId"])
    resolved_only = has_comment - has_unresolved

    for c in state["collaborators"]:
        if c["id"] in has_unresolved:
            c["avatarColor"] = "#F24E1E"
        elif c["id"] in resolved_only:
            c["avatarColor"] = "#0ACF83"


def solve_task_h72(state):
    """title_content: center Title; section: Subtitle weight 600, size 24."""
    for s in state["slides"]:
        layout = s.get("layout", "")
        if layout == "layout_title_content":
            for obj in s["objects"]:
                if obj["name"] == "Title":
                    obj["textAlign"] = "center"
                    break
        elif layout == "layout_section":
            for obj in s["objects"]:
                if obj["name"] == "Section Subtitle":
                    obj["fontWeight"] = 600
                    obj["fontSize"] = 24
                    break


def solve_task_h73(state):
    """Design System 2.0: remove animations, opacity 85 for pop, 90 for others."""
    slide = find_slide(state, "Design System 2.0")
    for obj in slide["objects"]:
        anim = obj.get("animation")
        if anim is not None:
            if anim.get("style") == "pop":
                obj["opacity"] = 85
            else:
                obj["opacity"] = 90
            obj["animation"] = None


def solve_task_h74(state):
    """Notes 'Let Aiko take over' -> smart_animate; 'hiring timeline' -> skip."""
    for s in state["slides"]:
        notes = s.get("presenterNotes", "")
        if "Let Aiko take over" in notes:
            s["transition"] = {
                "type": "smart_animate", "direction": None,
                "easing": "ease_in_out", "duration": 600, "timing": "immediately"
            }
        if "hiring timeline" in notes:
            s["skipped"] = True


def solve_task_h75(state):
    """Gradient/skipped -> disable slide numbers; others -> padded."""
    for s in state["slides"]:
        bg = s.get("background", {})
        is_gradient = bg.get("type") == "gradient"
        is_skipped = s.get("skipped") is True
        if is_gradient or is_skipped:
            s["slideNumberEnabled"] = False
        else:
            s["slideNumberEnabled"] = True
            s["slideNumberFormat"] = "padded"


def solve_task_h76(state):
    """Update Accent colors per template; Corporate Blue Heading 2 size 28."""
    accent_map = {"ts_001": "#FF6B35", "ts_002": "#F7C948", "ts_003": "#7B61FF"}
    for ts in state["templateStyles"]:
        ts_id = ts["id"]
        if ts_id in accent_map:
            for color in ts["colors"]:
                if color["name"] == "Accent":
                    color["value"] = accent_map[ts_id]
                    break
        if ts_id == "ts_002":
            for text_style in ts["textStyles"]:
                if text_style["name"] == "Heading 2":
                    text_style["fontSize"] = 28
                    break


def solve_task_h77(state):
    """Normalize: ease_in_out everywhere; directional 500ms; directionless 400ms."""
    directional = {"push", "slide_in", "slide_out", "move_in", "move_out"}
    directionless = {"dissolve", "smart_animate"}
    for s in state["slides"]:
        trans = s["transition"]
        trans["easing"] = "ease_in_out"
        t_type = trans.get("type", "none")
        if t_type in directional:
            trans["duration"] = 500
        elif t_type in directionless:
            trans["duration"] = 400


def solve_task_h78(state):
    """Largest group (Q4 Planning) -> Corporate Blue + Plus Jakarta Sans titles."""
    q4_planning_titles = {
        "Q4 Roadmap", "Design System 2.0", "API Reference",
        "Team Survey Results", "Data Comparison"
    }
    for s in state["slides"]:
        if s["title"] in q4_planning_titles:
            s["templateStyle"] = "ts_002"
            for obj in s["objects"]:
                if obj["name"] == "Title":
                    obj["fontFamily"] = "Plus Jakarta Sans"


def solve_task_h79(state):
    """Highest Target Q4 feature -> 'Market Leader' in competitive; target to 95%."""
    adoption_slide = find_slide(state, "Data Comparison")
    adoption_table = find_object(adoption_slide, "Adoption Table")
    adoption_table["cells"][1][4] = "95%"

    comp_slide = find_slide(state, "Competitive Landscape")
    comp_table = find_object(comp_slide, "Comparison Table")
    comp_table["cells"][1][1] = "Market Leader"


def solve_task_h80(state):
    """Adoption table: cells ending in '0%' -> end in '5%'."""
    slide = find_slide(state, "Data Comparison")
    table = find_object(slide, "Adoption Table")
    for r in range(1, len(table["cells"])):
        for c in range(len(table["cells"][r])):
            val = table["cells"][r][c]
            if val.endswith("0%"):
                table["cells"][r][c] = val[:-2] + "5%"


SOLVERS = {}
for _difficulty in ("e", "m", "h"):
    for _i in range(1, 81):
        _task_id = f"task_{_difficulty}{_i}"
        _fn_name = f"solve_task_{_difficulty}{_i}"
        if _fn_name in globals():
            SOLVERS[_task_id] = globals()[_fn_name]


# ── server management ────────────────────────────────────────────────

def generate_seed_state():
    data_js = str(APP_DIR / "js" / "data.js")
    result = subprocess.run(
        ["node", "-e", _SEED_STATE_JS, data_js],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to generate seed state:\n{result.stderr}")
    return json.loads(result.stdout)


def seed_server(server_url, seed_state):
    resp = requests.put(
        f"{server_url}/api/state",
        json=seed_state,
        headers={"Content-Type": "application/json"},
    )
    if resp.status_code != 200:
        raise RuntimeError(f"Failed to seed server: HTTP {resp.status_code}")


def find_free_port(start=9000):
    port = start
    while port < start + 200:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))
                return port
            except OSError:
                port += 1
    raise RuntimeError(f"No free port found in range {start}-{start+200}")


def start_server(port):
    proc = subprocess.Popen(
        [sys.executable, "server.py", "--port", str(port)],
        cwd=str(APP_DIR),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    for _ in range(30):
        try:
            requests.get(f"http://localhost:{port}/", timeout=1)
            return proc
        except (requests.ConnectionError, requests.Timeout):
            time.sleep(0.2)
    proc.kill()
    raise RuntimeError(f"Server failed to start on port {port}")


def stop_server(proc):
    if proc and proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


# ── task runner ──────────────────────────────────────────────────────

def load_tasks():
    with open(TASKS_FILE) as f:
        return json.load(f)


def load_verifier(verify_path):
    full_path = APP_DIR / verify_path
    spec = importlib.util.spec_from_file_location("verifier", str(full_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.verify


def run_single_task(task, server_url):
    task_id = task["id"]
    solver = SOLVERS.get(task_id)
    if not solver:
        return task_id, False, f"No solver defined for {task_id}"

    try:
        # 1. Reset to seed state
        resp = requests.post(f"{server_url}/api/reset")
        if resp.status_code != 200:
            return task_id, False, f"Reset failed: HTTP {resp.status_code}"

        time.sleep(0.3)

        # 2. Read seed state
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return task_id, False, f"Could not read state after reset: HTTP {resp.status_code}"
        state = resp.json()

        # 3. Apply the solve function
        solver(state)

        # 4. Write solved state back
        resp = requests.put(
            f"{server_url}/api/state",
            json=state,
            headers={"Content-Type": "application/json"},
        )
        if resp.status_code != 200:
            return task_id, False, f"Could not write state: HTTP {resp.status_code}"

        # 5. Run the verifier
        verify_fn = load_verifier(task["verify"])
        passed, message = verify_fn(server_url)
        return task_id, passed, message

    except Exception as e:
        return task_id, False, f"Exception: {e}"


def run_tasks_sequential(tasks, port, seed_state):
    proc = start_server(port)
    server_url = f"http://localhost:{port}"
    results = []
    try:
        seed_server(server_url, seed_state)
        for task in tasks:
            result = run_single_task(task, server_url)
            results.append(result)
            status = "\033[32m  PASS\033[0m" if result[1] else "\033[31m  FAIL\033[0m"
            print(f"{status}  {result[0]:12s}  {result[2]}")
    finally:
        stop_server(proc)
    return results


def run_tasks_parallel(tasks, workers, base_port, seed_state):
    results = []

    def worker_fn(task, port):
        proc = start_server(port)
        server_url = f"http://localhost:{port}"
        try:
            seed_server(server_url, seed_state)
            return run_single_task(task, server_url)
        finally:
            stop_server(proc)

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {}
        for i, task in enumerate(tasks):
            port = base_port + i
            future = executor.submit(worker_fn, task, port)
            futures[future] = task["id"]

        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            status = "\033[32m  PASS\033[0m" if result[1] else "\033[31m  FAIL\033[0m"
            print(f"{status}  {result[0]:12s}  {result[2]}")

    return results


# ── main ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Figma Slides real-task sanity check")
    parser.add_argument("--task-id", type=str, help="Run a single task by ID")
    parser.add_argument("--workers", type=int, default=1, help="Number of parallel workers")
    parser.add_argument("--port", type=int, default=9600, help="Base port for servers")
    args = parser.parse_args()

    tasks = load_tasks()
    if args.task_id:
        tasks = [t for t in tasks if t["id"] == args.task_id]
        if not tasks:
            print(f"Task '{args.task_id}' not found.")
            sys.exit(1)

    print("Generating seed state from JS data...")
    seed_state = generate_seed_state()
    print(f"Running {len(tasks)} task(s)...\n")

    if args.workers <= 1:
        port = find_free_port(args.port)
        results = run_tasks_sequential(tasks, port, seed_state)
    else:
        results = run_tasks_parallel(tasks, args.workers, args.port, seed_state)

    # Summary
    passed = sum(1 for _, p, _ in results if p)
    total = len(results)
    failed = [tid for tid, p, _ in results if not p]

    print(f"\n{passed}/{total} passed")
    if failed:
        print(f"Failed: {', '.join(failed)}")
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
