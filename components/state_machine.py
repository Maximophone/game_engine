from dataclasses import dataclass
from components.component import Component
from typing import Dict, List

from components.animation_state import AnimationState
from components.sprite_renderer import SpriteRenderer
from editor.mx_imgui import MXImGUI
from util.serialization import serializable

import imgui

@serializable("state", "trigger")
class StateTrigger:
    def __init__(self, state: str = "", trigger: str = ""):
        self.state = state
        self.trigger = trigger

    def __eq__(self, o: object) -> bool:
        if type(o) != StateTrigger:
            return False
        return o.trigger == self.trigger and o.state == self.state

    def __hash__(self) -> int:
        return hash((self.trigger, self.state))

@serializable("state_transfers", "states", "default_state_title")
class StateMachine(Component):
    def __init__(self):
        self.state_transfers: Dict[StateTrigger, str] = {}
        self.states: List[AnimationState] = []
        self.current_state: AnimationState = None
        self.default_state_title: str = ""
        super().__init__()

    def refresh_textures(self):
        for state in self.states:
            state.refresh_textures()

    def add_state_trigger(self, from_: str, to: str, on_trigger: str):
        self.state_transfers[StateTrigger(from_, on_trigger)] = to

    def add_state(self, state: AnimationState):
        self.states.append(state)

    def set_default_state(self, animation_title: str):
        for state in self.states:
            if state.title == animation_title:
                self.default_state_title = animation_title
                if self.current_state is None:
                    self.current_state = state
                    return
        print(f"Unable to find state: {animation_title} in set default state")

    def trigger(self, trigger: str):
        wanted_state = self.state_transfers.get(StateTrigger(self.current_state.title, trigger))
        if wanted_state is not None:
            self.current_state = next(state for state in self.states if state.title == wanted_state)
            return
        print(f"Unable to find trigger {trigger} for state {self.current_state.title}")

    def start(self):
        for state in self.states:
            if state.title == self.default_state_title:
                self.current_state = state
                break

    def update(self, dt: float):
        if self.current_state is not None:
            self.current_state.update(dt)
            spr: SpriteRenderer = self.game_object.get_component(SpriteRenderer)
            if spr is not None:
                spr.set_sprite(self.current_state.get_current_sprite())

    def editor_update(self, dt: float):
        self.update(dt)

    def imgui(self):
        index = 0
        for state in self.states:
            state.title = MXImGUI.input_text("State: ", state.title)

            changed, value = imgui.checkbox("Does Loop? ", state.does_loop)
            if changed:
                state.does_loop = value
            for frame in state.animation_frames:
                changed, value = imgui.drag_float(f"Frame({index}) Time", frame.frame_time, 0.01)
                if changed:
                    frame.frame_time = value
                index += 1