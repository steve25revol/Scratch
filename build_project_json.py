"""Build the complete project.json for the Scratch stickman animation."""

import uuid
import json


def _uid():
    """Generate a unique block ID."""
    return uuid.uuid4().hex[:20]


class BlockBuilder:
    """Helper to build Scratch 3.0 block chains."""

    def __init__(self):
        self.blocks = {}
        self._chain_stack = []  # stack of (chain_head_id, chain_tail_id)

    def _add_block(self, opcode, fields=None, inputs=None,
                   top_level=False, parent=None, shadow=False, x=0, y=0):
        bid = _uid()
        block = {
            "opcode": opcode,
            "next": None,
            "parent": parent,
            "inputs": inputs or {},
            "fields": fields or {},
            "shadow": shadow,
            "topLevel": top_level,
        }
        if top_level:
            block["x"] = x
            block["y"] = y
        self.blocks[bid] = block
        return bid

    def hat_green_flag(self, x=0, y=0):
        """Start a new chain with green flag hat block."""
        bid = self._add_block("event_whenflagclicked", top_level=True, x=x, y=y)
        self._chain_stack = [(bid, bid)]
        return self

    def hat_broadcast_received(self, broadcast_name, broadcast_id, x=0, y=0):
        """Start chain with 'when I receive' hat."""
        bid = self._add_block(
            "event_whenbroadcastreceived",
            fields={"BROADCAST_OPTION": [broadcast_name, broadcast_id]},
            top_level=True, x=x, y=y
        )
        self._chain_stack = [(bid, bid)]
        return self

    def _append_to_chain(self, block_id):
        """Append block to current chain."""
        if self._chain_stack:
            head, tail = self._chain_stack[-1]
            self.blocks[tail]["next"] = block_id
            self.blocks[block_id]["parent"] = tail
            self._chain_stack[-1] = (head, block_id)
        return self

    def broadcast(self, msg_name, msg_id):
        """broadcast message."""
        # Create the shadow/menu block for the broadcast input
        menu_id = _uid()
        self.blocks[menu_id] = {
            "opcode": "event_broadcast_menu",
            "next": None,
            "parent": None,  # will be set
            "inputs": {},
            "fields": {"BROADCAST_OPTION": [msg_name, msg_id]},
            "shadow": True,
            "topLevel": False,
        }
        bid = self._add_block(
            "event_broadcast",
            inputs={"BROADCAST_INPUT": [1, menu_id]},
        )
        self.blocks[menu_id]["parent"] = bid
        return self._append_to_chain(bid)

    def broadcast_and_wait(self, msg_name, msg_id):
        """broadcast and wait."""
        menu_id = _uid()
        self.blocks[menu_id] = {
            "opcode": "event_broadcast_menu",
            "next": None,
            "parent": None,
            "inputs": {},
            "fields": {"BROADCAST_OPTION": [msg_name, msg_id]},
            "shadow": True,
            "topLevel": False,
        }
        bid = self._add_block(
            "event_broadcastandwait",
            inputs={"BROADCAST_INPUT": [1, menu_id]},
        )
        self.blocks[menu_id]["parent"] = bid
        return self._append_to_chain(bid)

    def wait(self, seconds):
        """control_wait."""
        bid = self._add_block(
            "control_wait",
            inputs={"DURATION": [1, [4, str(seconds)]]},
        )
        return self._append_to_chain(bid)

    def switch_costume(self, costume_name):
        """looks_switchcostumeto."""
        menu_id = _uid()
        self.blocks[menu_id] = {
            "opcode": "looks_costume",
            "next": None,
            "parent": None,
            "inputs": {},
            "fields": {"COSTUME": [costume_name, None]},
            "shadow": True,
            "topLevel": False,
        }
        bid = self._add_block(
            "looks_switchcostumeto",
            inputs={"COSTUME": [1, menu_id]},
        )
        self.blocks[menu_id]["parent"] = bid
        return self._append_to_chain(bid)

    def switch_backdrop(self, backdrop_name):
        """looks_switchbackdropto."""
        menu_id = _uid()
        self.blocks[menu_id] = {
            "opcode": "looks_backdrops",
            "next": None,
            "parent": None,
            "inputs": {},
            "fields": {"BACKDROP": [backdrop_name, None]},
            "shadow": True,
            "topLevel": False,
        }
        bid = self._add_block(
            "looks_switchbackdropto",
            inputs={"BACKDROP": [1, menu_id]},
        )
        self.blocks[menu_id]["parent"] = bid
        return self._append_to_chain(bid)

    def go_to_xy(self, x, y):
        """motion_gotoxy."""
        bid = self._add_block(
            "motion_gotoxy",
            inputs={
                "X": [1, [4, str(x)]],
                "Y": [1, [4, str(y)]],
            },
        )
        return self._append_to_chain(bid)

    def glide_to(self, secs, x, y):
        """motion_glidesecstoxy."""
        bid = self._add_block(
            "motion_glidesecstoxy",
            inputs={
                "SECS": [1, [4, str(secs)]],
                "X": [1, [4, str(x)]],
                "Y": [1, [4, str(y)]],
            },
        )
        return self._append_to_chain(bid)

    def change_x_by(self, dx):
        bid = self._add_block(
            "motion_changexby",
            inputs={"DX": [1, [4, str(dx)]]},
        )
        return self._append_to_chain(bid)

    def change_y_by(self, dy):
        bid = self._add_block(
            "motion_changeyby",
            inputs={"DY": [1, [4, str(dy)]]},
        )
        return self._append_to_chain(bid)

    def show(self):
        bid = self._add_block("looks_show")
        return self._append_to_chain(bid)

    def hide(self):
        bid = self._add_block("looks_hide")
        return self._append_to_chain(bid)

    def set_size(self, size):
        bid = self._add_block(
            "looks_setsizeto",
            inputs={"SIZE": [1, [4, str(size)]]},
        )
        return self._append_to_chain(bid)

    def change_size_by(self, delta):
        bid = self._add_block(
            "looks_changesizeby",
            inputs={"CHANGE": [1, [4, str(delta)]]},
        )
        return self._append_to_chain(bid)

    def set_effect(self, effect, value):
        """looks_seteffectto. effect: 'ghost', 'color', etc."""
        bid = self._add_block(
            "looks_seteffectto",
            inputs={"VALUE": [1, [4, str(value)]]},
            fields={"EFFECT": [effect.upper(), None]},
        )
        return self._append_to_chain(bid)

    def change_effect(self, effect, value):
        bid = self._add_block(
            "looks_changeeffectby",
            inputs={"CHANGE": [1, [4, str(value)]]},
            fields={"EFFECT": [effect.upper(), None]},
        )
        return self._append_to_chain(bid)

    def clear_effects(self):
        bid = self._add_block("looks_cleargraphiceffects")
        return self._append_to_chain(bid)

    def go_to_front(self):
        bid = self._add_block(
            "looks_gotofrontback",
            fields={"FRONT_BACK": ["front", None]},
        )
        return self._append_to_chain(bid)

    def go_to_back(self):
        bid = self._add_block(
            "looks_gotofrontback",
            fields={"FRONT_BACK": ["back", None]},
        )
        return self._append_to_chain(bid)

    def play_sound(self, sound_name):
        """sound_play (fire and forget)."""
        menu_id = _uid()
        self.blocks[menu_id] = {
            "opcode": "sound_sounds_menu",
            "next": None,
            "parent": None,
            "inputs": {},
            "fields": {"SOUND_MENU": [sound_name, None]},
            "shadow": True,
            "topLevel": False,
        }
        bid = self._add_block(
            "sound_play",
            inputs={"SOUND_MENU": [1, menu_id]},
        )
        self.blocks[menu_id]["parent"] = bid
        return self._append_to_chain(bid)

    def play_sound_until_done(self, sound_name):
        menu_id = _uid()
        self.blocks[menu_id] = {
            "opcode": "sound_sounds_menu",
            "next": None,
            "parent": None,
            "inputs": {},
            "fields": {"SOUND_MENU": [sound_name, None]},
            "shadow": True,
            "topLevel": False,
        }
        bid = self._add_block(
            "sound_playuntildone",
            inputs={"SOUND_MENU": [1, menu_id]},
        )
        self.blocks[menu_id]["parent"] = bid
        return self._append_to_chain(bid)

    def set_volume(self, vol):
        bid = self._add_block(
            "sound_setvolumeto",
            inputs={"VOLUME": [1, [4, str(vol)]]},
        )
        return self._append_to_chain(bid)

    def stop_all_sounds(self):
        bid = self._add_block("sound_stopallsounds")
        return self._append_to_chain(bid)

    def repeat(self, times):
        """Start a repeat block. Call end_repeat() after adding body blocks."""
        bid = self._add_block(
            "control_repeat",
            inputs={"TIMES": [1, [6, str(times)]]},
        )
        self._append_to_chain(bid)
        # Push a new sub-chain for the body (SUBSTACK)
        self._chain_stack.append((bid, bid))
        self._current_repeat_id = bid
        return self

    def end_repeat(self):
        """Close the current repeat block body."""
        if len(self._chain_stack) < 2:
            return self
        # Pop the body chain
        body_head, body_tail = self._chain_stack.pop()
        repeat_id = body_head  # The repeat block itself
        # Get first block after repeat in body
        first_body = self.blocks[repeat_id].get("next")
        if first_body:
            # Move the body blocks into SUBSTACK
            self.blocks[repeat_id]["inputs"]["SUBSTACK"] = [2, first_body]
            self.blocks[repeat_id]["next"] = None
            # Fix parent references
            self.blocks[first_body]["parent"] = repeat_id
        return self

    def forever(self):
        """Start a forever block."""
        bid = self._add_block("control_forever")
        self._append_to_chain(bid)
        self._chain_stack.append((bid, bid))
        return self

    def end_forever(self):
        """Close the forever block body."""
        if len(self._chain_stack) < 2:
            return self
        body_head, body_tail = self._chain_stack.pop()
        forever_id = body_head
        first_body = self.blocks[forever_id].get("next")
        if first_body:
            self.blocks[forever_id]["inputs"]["SUBSTACK"] = [2, first_body]
            self.blocks[forever_id]["next"] = None
            self.blocks[first_body]["parent"] = forever_id
        return self

    def stop_this_script(self):
        bid = self._add_block(
            "control_stop",
            fields={"STOP_OPTION": ["this script", None]},
        )
        self.blocks[bid]["mutation"] = {
            "tagName": "mutation",
            "children": [],
            "hasnext": "false",
        }
        return self._append_to_chain(bid)

    def get_blocks(self):
        return dict(self.blocks)


# ============================================================
# BROADCAST MESSAGE IDS
# ============================================================

BROADCASTS = {
    "act1-start": _uid(),
    "act2-explosion": _uid(),
    "act3-jump": _uid(),
    "act4-parachute": _uid(),
    "act5-landing": _uid(),
    "the-end": _uid(),
    "screen-shake": _uid(),
}


def _make_broadcast_vars():
    """Return broadcast dict for target."""
    return {v: k for k, v in BROADCASTS.items()}


# ============================================================
# STAGE TARGET
# ============================================================

def _build_stage_blocks():
    """Build blocks for the Stage (master timeline + backdrop switching)."""
    b = BlockBuilder()

    # Master timeline
    b.hat_green_flag(x=50, y=50)
    b.switch_backdrop("office-interior")
    b.broadcast("act1-start", BROADCASTS["act1-start"])
    b.wait(10)
    b.broadcast("act2-explosion", BROADCASTS["act2-explosion"])
    b.wait(5)
    b.broadcast("act3-jump", BROADCASTS["act3-jump"])
    b.wait(5)
    b.broadcast("act4-parachute", BROADCASTS["act4-parachute"])
    b.wait(8)
    b.broadcast("act5-landing", BROADCASTS["act5-landing"])
    b.wait(2)
    b.broadcast("the-end", BROADCASTS["the-end"])

    # Backdrop switch on act3
    b2 = BlockBuilder()
    b2.hat_broadcast_received("act3-jump", BROADCASTS["act3-jump"], x=50, y=400)
    b2.wait(2)
    b2.switch_backdrop("building-exterior")

    # Backdrop switch for landing
    b3 = BlockBuilder()
    b3.hat_broadcast_received("act5-landing", BROADCASTS["act5-landing"], x=50, y=600)
    b3.switch_backdrop("building-with-ground")

    all_blocks = {}
    all_blocks.update(b.get_blocks())
    all_blocks.update(b2.get_blocks())
    all_blocks.update(b3.get_blocks())
    return all_blocks


def build_stage_target(backdrop_costumes, stage_sounds):
    """Build the Stage target dict.

    backdrop_costumes: list of {"name", "assetId", "md5ext", "dataFormat", ...}
    stage_sounds: list of {"name", "assetId", "md5ext", "dataFormat", ...}
    """
    return {
        "isStage": True,
        "name": "Stage",
        "variables": {},
        "lists": {},
        "broadcasts": _make_broadcast_vars(),
        "blocks": _build_stage_blocks(),
        "comments": {},
        "currentCostume": 0,
        "costumes": backdrop_costumes,
        "sounds": stage_sounds,
        "volume": 100,
        "layerOrder": 0,
        "tempo": 60,
        "videoTransparency": 50,
        "videoState": "off",
        "textToSpeechLanguage": None,
    }


# ============================================================
# STICKMAN HERO TARGET
# ============================================================

def _build_hero_blocks():
    all_blocks = {}

    # --- Green flag: init ---
    b = BlockBuilder()
    b.hat_green_flag(x=50, y=50)
    b.show()
    b.set_size(100)
    b.clear_effects()
    b.go_to_xy(-50, -30)
    b.switch_costume("typing-1")
    all_blocks.update(b.get_blocks())

    # --- Act 1: typing animation ---
    b = BlockBuilder()
    b.hat_broadcast_received("act1-start", BROADCASTS["act1-start"], x=50, y=300)
    b.repeat(25)
    b.switch_costume("typing-1")
    b.wait(0.2)
    b.switch_costume("typing-2")
    b.wait(0.2)
    b.end_repeat()
    # React to glitching computer at ~8s
    b.switch_costume("surprised")
    b.wait(0.5)
    all_blocks.update(b.get_blocks())

    # --- Act 2: explosion reaction ---
    b = BlockBuilder()
    b.hat_broadcast_received("act2-explosion", BROADCASTS["act2-explosion"], x=50, y=600)
    b.switch_costume("knocked-back")
    b.glide_to(0.3, -100, -20)
    b.wait(0.3)
    # Shake the stickman
    b.repeat(6)
    b.change_x_by(5)
    b.wait(0.05)
    b.change_x_by(-5)
    b.wait(0.05)
    b.end_repeat()
    b.wait(1)
    all_blocks.update(b.get_blocks())

    # --- Act 3: run to window and jump ---
    b = BlockBuilder()
    b.hat_broadcast_received("act3-jump", BROADCASTS["act3-jump"], x=50, y=900)
    b.switch_costume("running-1")
    b.glide_to(0.4, 0, -30)
    b.switch_costume("running-2")
    b.glide_to(0.4, 60, -30)
    b.switch_costume("running-3")
    b.glide_to(0.4, 120, -30)
    b.switch_costume("running-1")
    b.glide_to(0.3, 160, -30)
    b.switch_costume("jumping")
    b.glide_to(0.5, 180, 0)
    # Now transition to exterior - reposition at top
    b.wait(0.5)
    b.go_to_xy(50, 150)
    b.switch_costume("falling-1")
    # Falling
    b.repeat(8)
    b.switch_costume("falling-1")
    b.change_y_by(-8)
    b.wait(0.1)
    b.switch_costume("falling-2")
    b.change_y_by(-8)
    b.wait(0.1)
    b.switch_costume("falling-3")
    b.change_y_by(-8)
    b.wait(0.1)
    b.end_repeat()
    all_blocks.update(b.get_blocks())

    # --- Act 4: parachute deploy + slow drift ---
    b = BlockBuilder()
    b.hat_broadcast_received("act4-parachute", BROADCASTS["act4-parachute"], x=50, y=1300)
    b.switch_costume("parachute-hold")
    b.wait(0.5)
    # Slow drift down with sway
    b.repeat(30)
    b.change_y_by(-3)
    b.change_x_by(2)
    b.wait(0.1)
    b.change_y_by(-3)
    b.change_x_by(-2)
    b.wait(0.1)
    b.end_repeat()
    all_blocks.update(b.get_blocks())

    # --- Act 5: landing ---
    b = BlockBuilder()
    b.hat_broadcast_received("act5-landing", BROADCASTS["act5-landing"], x=50, y=1700)
    b.switch_costume("landing")
    b.glide_to(0.3, 50, -120)
    # Bounce
    b.glide_to(0.15, 50, -110)
    b.glide_to(0.15, 50, -120)
    b.wait(0.3)
    b.switch_costume("standing-final")
    b.wait(0.5)
    b.switch_costume("shrug")
    all_blocks.update(b.get_blocks())

    return all_blocks


def build_hero_target(costumes, sounds):
    return {
        "isStage": False,
        "name": "StickmanHero",
        "variables": {},
        "lists": {},
        "broadcasts": {},
        "blocks": _build_hero_blocks(),
        "comments": {},
        "currentCostume": 0,
        "costumes": costumes,
        "sounds": sounds,
        "volume": 100,
        "visible": True,
        "x": -50,
        "y": -30,
        "size": 100,
        "direction": 90,
        "draggable": False,
        "rotationStyle": "all around",
        "layerOrder": 5,
    }


# ============================================================
# COWORKER TARGETS
# ============================================================

def _build_coworker_blocks(prefix, start_x, start_y, idle_delay=0.3):
    all_blocks = {}

    # Init
    b = BlockBuilder()
    b.hat_green_flag(x=50, y=50)
    b.show()
    b.set_size(70)
    b.clear_effects()
    b.go_to_xy(start_x, start_y)
    b.switch_costume(f"{prefix}-idle-1")
    all_blocks.update(b.get_blocks())

    # Act 1: idle animation
    b = BlockBuilder()
    b.hat_broadcast_received("act1-start", BROADCASTS["act1-start"], x=50, y=300)
    b.repeat(15)
    b.switch_costume(f"{prefix}-idle-1")
    b.wait(idle_delay)
    b.switch_costume(f"{prefix}-idle-2")
    b.wait(idle_delay + 0.1)
    b.end_repeat()
    all_blocks.update(b.get_blocks())

    # Act 2: panic
    b = BlockBuilder()
    b.hat_broadcast_received("act2-explosion", BROADCASTS["act2-explosion"], x=50, y=600)
    b.switch_costume(f"{prefix}-panic-1")
    b.wait(0.3)
    b.repeat(5)
    b.switch_costume(f"{prefix}-panic-1")
    b.change_x_by(3)
    b.wait(0.15)
    b.switch_costume(f"{prefix}-panic-2")
    b.change_x_by(3)
    b.wait(0.15)
    b.end_repeat()
    all_blocks.update(b.get_blocks())

    # Act 3: hide (they stay in building)
    b = BlockBuilder()
    b.hat_broadcast_received("act3-jump", BROADCASTS["act3-jump"], x=50, y=900)
    b.wait(1)
    b.hide()
    all_blocks.update(b.get_blocks())

    return all_blocks


def build_coworker_target(name, prefix, costumes, sounds, start_x, start_y, idle_delay=0.3):
    return {
        "isStage": False,
        "name": name,
        "variables": {},
        "lists": {},
        "broadcasts": {},
        "blocks": _build_coworker_blocks(prefix, start_x, start_y, idle_delay),
        "comments": {},
        "currentCostume": 0,
        "costumes": costumes,
        "sounds": sounds,
        "volume": 100,
        "visible": True,
        "x": start_x,
        "y": start_y,
        "size": 70,
        "direction": 90,
        "draggable": False,
        "rotationStyle": "all around",
        "layerOrder": 2,
    }


# ============================================================
# COMPUTER TARGET
# ============================================================

def _build_computer_blocks():
    all_blocks = {}

    # Init
    b = BlockBuilder()
    b.hat_green_flag(x=50, y=50)
    b.show()
    b.set_size(100)
    b.clear_effects()
    b.go_to_xy(-10, -30)
    b.switch_costume("normal-1")
    all_blocks.update(b.get_blocks())

    # Act 1: screen glow
    b = BlockBuilder()
    b.hat_broadcast_received("act1-start", BROADCASTS["act1-start"], x=50, y=300)
    b.repeat(12)
    b.switch_costume("normal-1")
    b.wait(0.3)
    b.switch_costume("normal-2")
    b.wait(0.3)
    b.end_repeat()
    # Start glitching
    b.repeat(5)
    b.switch_costume("glitching")
    b.wait(0.15)
    b.switch_costume("normal-1")
    b.wait(0.1)
    b.switch_costume("red-screen")
    b.wait(0.1)
    b.switch_costume("normal-2")
    b.wait(0.1)
    b.end_repeat()
    all_blocks.update(b.get_blocks())

    # Act 2: destroyed
    b = BlockBuilder()
    b.hat_broadcast_received("act2-explosion", BROADCASTS["act2-explosion"], x=50, y=700)
    b.switch_costume("destroyed")
    b.wait(2)
    all_blocks.update(b.get_blocks())

    # Act 3: hide
    b = BlockBuilder()
    b.hat_broadcast_received("act3-jump", BROADCASTS["act3-jump"], x=50, y=900)
    b.hide()
    all_blocks.update(b.get_blocks())

    return all_blocks


def build_computer_target(costumes, sounds):
    return {
        "isStage": False,
        "name": "Computer",
        "variables": {},
        "lists": {},
        "broadcasts": {},
        "blocks": _build_computer_blocks(),
        "comments": {},
        "currentCostume": 0,
        "costumes": costumes,
        "sounds": sounds,
        "volume": 100,
        "visible": True,
        "x": -10,
        "y": -30,
        "size": 100,
        "direction": 90,
        "draggable": False,
        "rotationStyle": "all around",
        "layerOrder": 3,
    }


# ============================================================
# EXPLOSION TARGET
# ============================================================

def _build_explosion_blocks():
    all_blocks = {}

    # Init: hidden
    b = BlockBuilder()
    b.hat_green_flag(x=50, y=50)
    b.hide()
    b.go_to_xy(-10, -10)
    b.set_size(100)
    b.clear_effects()
    all_blocks.update(b.get_blocks())

    # Act 2: explosion animation
    b = BlockBuilder()
    b.hat_broadcast_received("act2-explosion", BROADCASTS["act2-explosion"], x=50, y=300)
    b.show()
    b.go_to_front()
    b.switch_costume("flash-small")
    b.wait(0.08)
    b.switch_costume("fireball-1")
    b.wait(0.1)
    b.switch_costume("fireball-2")
    b.wait(0.12)
    b.switch_costume("fireball-3")
    b.wait(0.15)
    b.switch_costume("smoke-1")
    b.wait(0.2)
    b.switch_costume("smoke-2")
    b.wait(0.25)
    b.switch_costume("smoke-3")
    b.wait(0.3)
    b.switch_costume("dissipate")
    b.wait(0.4)
    # Fade out
    b.repeat(10)
    b.change_effect("ghost", 10)
    b.wait(0.05)
    b.end_repeat()
    b.hide()
    all_blocks.update(b.get_blocks())

    return all_blocks


def build_explosion_target(costumes, sounds):
    return {
        "isStage": False,
        "name": "Explosion",
        "variables": {},
        "lists": {},
        "broadcasts": {},
        "blocks": _build_explosion_blocks(),
        "comments": {},
        "currentCostume": 0,
        "costumes": costumes,
        "sounds": sounds,
        "volume": 100,
        "visible": False,
        "x": -10,
        "y": -10,
        "size": 100,
        "direction": 90,
        "draggable": False,
        "rotationStyle": "all around",
        "layerOrder": 8,
    }


# ============================================================
# PARACHUTE TARGET
# ============================================================

def _build_parachute_blocks():
    all_blocks = {}

    # Init: hidden
    b = BlockBuilder()
    b.hat_green_flag(x=50, y=50)
    b.hide()
    b.set_size(100)
    b.clear_effects()
    all_blocks.update(b.get_blocks())

    # Act 4: deploy
    b = BlockBuilder()
    b.hat_broadcast_received("act4-parachute", BROADCASTS["act4-parachute"], x=50, y=300)
    b.go_to_xy(50, 20)
    b.show()
    b.switch_costume("packed")
    b.wait(0.2)
    b.switch_costume("deploying-1")
    b.wait(0.2)
    b.switch_costume("deploying-2")
    b.wait(0.2)
    b.switch_costume("full-open")
    b.wait(0.5)
    # Drift with sway
    b.repeat(15)
    b.switch_costume("drifting-1")
    b.change_y_by(-3)
    b.change_x_by(2)
    b.wait(0.2)
    b.switch_costume("drifting-2")
    b.change_y_by(-3)
    b.change_x_by(-2)
    b.wait(0.2)
    b.end_repeat()
    all_blocks.update(b.get_blocks())

    # Act 5: collapse
    b = BlockBuilder()
    b.hat_broadcast_received("act5-landing", BROADCASTS["act5-landing"], x=50, y=700)
    b.switch_costume("collapsed")
    b.glide_to(0.3, 50, -100)
    b.wait(1)
    # Fade
    b.repeat(10)
    b.change_effect("ghost", 10)
    b.wait(0.05)
    b.end_repeat()
    b.hide()
    all_blocks.update(b.get_blocks())

    return all_blocks


def build_parachute_target(costumes, sounds):
    return {
        "isStage": False,
        "name": "Parachute",
        "variables": {},
        "lists": {},
        "broadcasts": {},
        "blocks": _build_parachute_blocks(),
        "comments": {},
        "currentCostume": 0,
        "costumes": costumes,
        "sounds": sounds,
        "volume": 100,
        "visible": False,
        "x": 50,
        "y": 20,
        "size": 100,
        "direction": 90,
        "draggable": False,
        "rotationStyle": "all around",
        "layerOrder": 6,
    }


# ============================================================
# DEBRIS TARGET
# ============================================================

def _build_debris_blocks():
    all_blocks = {}

    # Init: hidden
    b = BlockBuilder()
    b.hat_green_flag(x=50, y=50)
    b.hide()
    b.set_size(80)
    b.clear_effects()
    b.go_to_xy(-10, -10)
    all_blocks.update(b.get_blocks())

    # Act 2: fly outward (simple -- no clones, just move)
    b = BlockBuilder()
    b.hat_broadcast_received("act2-explosion", BROADCASTS["act2-explosion"], x=50, y=300)
    b.wait(0.2)
    b.show()
    b.switch_costume("debris-1")
    b.glide_to(0.5, 80, 60)
    b.switch_costume("debris-2")
    b.glide_to(0.4, 120, 100)
    b.switch_costume("debris-3")
    b.glide_to(0.3, 140, 130)
    b.wait(0.5)
    # Fade
    b.repeat(10)
    b.change_effect("ghost", 10)
    b.wait(0.05)
    b.end_repeat()
    b.hide()
    all_blocks.update(b.get_blocks())

    # Hide on act 3
    b = BlockBuilder()
    b.hat_broadcast_received("act3-jump", BROADCASTS["act3-jump"], x=50, y=700)
    b.hide()
    all_blocks.update(b.get_blocks())

    return all_blocks


def build_debris_target(costumes, sounds):
    return {
        "isStage": False,
        "name": "Debris",
        "variables": {},
        "lists": {},
        "broadcasts": {},
        "blocks": _build_debris_blocks(),
        "comments": {},
        "currentCostume": 0,
        "costumes": costumes,
        "sounds": sounds,
        "volume": 100,
        "visible": False,
        "x": -10,
        "y": -10,
        "size": 80,
        "direction": 90,
        "draggable": False,
        "rotationStyle": "all around",
        "layerOrder": 7,
    }


# ============================================================
# SECOND DEBRIS TARGET (different trajectory)
# ============================================================

def _build_debris2_blocks():
    all_blocks = {}

    b = BlockBuilder()
    b.hat_green_flag(x=50, y=50)
    b.hide()
    b.set_size(60)
    b.clear_effects()
    b.go_to_xy(-10, -10)
    all_blocks.update(b.get_blocks())

    b = BlockBuilder()
    b.hat_broadcast_received("act2-explosion", BROADCASTS["act2-explosion"], x=50, y=300)
    b.wait(0.15)
    b.show()
    b.switch_costume("debris-2")
    b.glide_to(0.5, -100, 80)
    b.switch_costume("debris-3")
    b.glide_to(0.4, -130, 120)
    b.wait(0.3)
    b.repeat(10)
    b.change_effect("ghost", 10)
    b.wait(0.05)
    b.end_repeat()
    b.hide()
    all_blocks.update(b.get_blocks())

    b = BlockBuilder()
    b.hat_broadcast_received("act3-jump", BROADCASTS["act3-jump"], x=50, y=700)
    b.hide()
    all_blocks.update(b.get_blocks())

    return all_blocks


def build_debris2_target(costumes, sounds):
    return {
        "isStage": False,
        "name": "Debris2",
        "variables": {},
        "lists": {},
        "broadcasts": {},
        "blocks": _build_debris2_blocks(),
        "comments": {},
        "currentCostume": 0,
        "costumes": costumes,
        "sounds": sounds,
        "volume": 100,
        "visible": False,
        "x": -10,
        "y": -10,
        "size": 60,
        "direction": 90,
        "draggable": False,
        "rotationStyle": "all around",
        "layerOrder": 7,
    }


# ============================================================
# THE END TEXT TARGET
# ============================================================

def _build_theend_blocks():
    all_blocks = {}

    b = BlockBuilder()
    b.hat_green_flag(x=50, y=50)
    b.hide()
    b.set_size(100)
    b.set_effect("ghost", 100)
    b.go_to_xy(0, 30)
    all_blocks.update(b.get_blocks())

    b = BlockBuilder()
    b.hat_broadcast_received("the-end", BROADCASTS["the-end"], x=50, y=300)
    b.show()
    b.go_to_front()
    # Fade in
    b.repeat(20)
    b.change_effect("ghost", -5)
    b.wait(0.05)
    b.end_repeat()
    all_blocks.update(b.get_blocks())

    return all_blocks


def build_theend_target(costumes, sounds):
    return {
        "isStage": False,
        "name": "TheEnd",
        "variables": {},
        "lists": {},
        "broadcasts": {},
        "blocks": _build_theend_blocks(),
        "comments": {},
        "currentCostume": 0,
        "costumes": costumes,
        "sounds": sounds,
        "volume": 100,
        "visible": False,
        "x": 0,
        "y": 30,
        "size": 100,
        "direction": 90,
        "draggable": False,
        "rotationStyle": "all around",
        "layerOrder": 10,
    }


# ============================================================
# SOUND CONTROLLER SPRITE (invisible, handles all sounds)
# ============================================================

def _build_sound_controller_blocks():
    """A hidden sprite that handles sound playback via broadcasts."""
    all_blocks = {}

    # Init: hide
    b = BlockBuilder()
    b.hat_green_flag(x=50, y=50)
    b.hide()
    b.set_volume(100)
    all_blocks.update(b.get_blocks())

    # Act 1 sounds: typing + chatter + hum
    b = BlockBuilder()
    b.hat_broadcast_received("act1-start", BROADCASTS["act1-start"], x=50, y=200)
    b.set_volume(60)
    b.play_sound("chatter-loop")
    b.play_sound("office-hum")
    b.repeat(3)
    b.play_sound_until_done("typing-loop")
    b.end_repeat()
    all_blocks.update(b.get_blocks())

    # Act 2 sounds: explosion + glass + gasp
    b = BlockBuilder()
    b.hat_broadcast_received("act2-explosion", BROADCASTS["act2-explosion"], x=50, y=500)
    b.stop_all_sounds()
    b.set_volume(100)
    b.play_sound("explosion")
    b.wait(0.2)
    b.play_sound("glass-shatter")
    b.wait(0.3)
    b.play_sound("gasp")
    all_blocks.update(b.get_blocks())

    # Act 3 sounds: footsteps + glass + wind
    b = BlockBuilder()
    b.hat_broadcast_received("act3-jump", BROADCASTS["act3-jump"], x=50, y=800)
    b.play_sound("footsteps")
    b.wait(1.5)
    b.play_sound("glass-shatter")
    b.wait(0.5)
    b.play_sound("wind-rush")
    all_blocks.update(b.get_blocks())

    # Act 4 sounds: parachute + fabric + wind
    b = BlockBuilder()
    b.hat_broadcast_received("act4-parachute", BROADCASTS["act4-parachute"], x=50, y=1100)
    b.play_sound("parachute-pop")
    b.wait(0.5)
    b.set_volume(70)
    b.play_sound("fabric-flap")
    b.play_sound("wind-rush")
    b.wait(3)
    b.set_volume(40)
    b.play_sound("siren-distant")
    all_blocks.update(b.get_blocks())

    # Act 5 sounds: thud
    b = BlockBuilder()
    b.hat_broadcast_received("act5-landing", BROADCASTS["act5-landing"], x=50, y=1400)
    b.stop_all_sounds()
    b.set_volume(100)
    b.play_sound("landing-thud")
    all_blocks.update(b.get_blocks())

    return all_blocks


def build_sound_controller_target(sounds):
    """Invisible sprite that only plays sounds."""
    # Needs a minimal costume
    return {
        "isStage": False,
        "name": "SoundController",
        "variables": {},
        "lists": {},
        "broadcasts": {},
        "blocks": _build_sound_controller_blocks(),
        "comments": {},
        "currentCostume": 0,
        "costumes": [],  # will be set by packager with a tiny transparent SVG
        "sounds": sounds,
        "volume": 100,
        "visible": False,
        "x": 0,
        "y": 0,
        "size": 100,
        "direction": 90,
        "draggable": False,
        "rotationStyle": "all around",
        "layerOrder": 1,
    }


# ============================================================
# FULL PROJECT
# ============================================================

def build_project(targets):
    """Build the full project.json structure."""
    return {
        "targets": targets,
        "monitors": [],
        "extensions": [],
        "meta": {
            "semver": "3.0.0",
            "vm": "0.2.0-prerelease.20190521152515",
            "agent": "Claude Code",
        },
    }
