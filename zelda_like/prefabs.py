from components.spritesheet import Spritesheet
from zelda_like.components.player_controller import PlayerController
from mxeng.prefabs import Prefabs
from physics2d.components.circle_collider import CircleCollider
from physics2d.components.rigid_body_2d import RigidBody2D
from physics2d.enums.body_type import BodyType
from components.animation_state import AnimationState
from components.state_machine import StateMachine
from mxeng.direction import Direction

class ZeldaPrefabs(Prefabs):
    @staticmethod
    def generate_character(character_sprites: Spritesheet):
        character = Prefabs.generate_sprite_object(character_sprites.get_sprite(0), 0.25, 0.25)

        default_frame_time = 0.2

        state_machine = StateMachine()
        idle = {}
        run = {}
        attack = {}
        jump = {}
        for dir in Direction:
            val = dir.value - 1
            idle[dir] = AnimationState(f"Idle {dir.name}")
            idle[dir].add_frame(character_sprites.get_sprite(0 + val), default_frame_time)
            idle[dir].does_loop = True
            state_machine.add_state(idle[dir])

            run[dir] = AnimationState(f"Run {dir.name}")
            run[dir].add_frame(character_sprites.get_sprite(0 + val), default_frame_time)
            run[dir].add_frame(character_sprites.get_sprite(4 + val), default_frame_time)
            run[dir].add_frame(character_sprites.get_sprite(8 + val), default_frame_time)
            run[dir].add_frame(character_sprites.get_sprite(12 + val), default_frame_time)
            run[dir].does_loop = True
            state_machine.add_state(run[dir])

            attack[dir] = AnimationState(f"Attack {dir.name}")
            attack[dir].add_frame(character_sprites.get_sprite(16 + val), default_frame_time)
            attack[dir].does_loop = False
            state_machine.add_state(attack[dir])

            jump[dir] = AnimationState(f"Jump {dir.name}")
            jump[dir].add_frame(character_sprites.get_sprite(20 + val), default_frame_time)
            jump[dir].does_loop = False
            state_machine.add_state(jump[dir])

        dead = AnimationState("Dead")
        dead.add_frame(character_sprites.get_sprite(24), default_frame_time)
        dead.does_loop = False
        state_machine.add_state(dead)

        state_machine.set_default_state(idle[Direction.Down])

        for dir_from in Direction:
            for dir_to in Direction:
                state_machine.add_state_trigger(idle[dir_from], run[dir_to], f"go_{dir_to.name.lower()}")
                state_machine.add_state_trigger(attack[dir_from], run[dir_to], f"go_{dir_to.name.lower()}")
                if dir_to != dir_from:
                    state_machine.add_state_trigger(run[dir_from], run[dir_to], f"go_{dir_to.name.lower()}")
                
                state_machine.add_state_trigger(run[dir_from], idle[dir_from], "stop")
                state_machine.add_state_trigger(attack[dir_from], idle[dir_from], "stop")
                state_machine.add_state_trigger(jump[dir_from], idle[dir_from], "stop")

                state_machine.add_state_trigger(idle[dir_from], attack[dir_from], "attack")
                state_machine.add_state_trigger(run[dir_from], attack[dir_from], "attack")

                state_machine.add_state_trigger(idle[dir_from], jump[dir_from], "jump")
                state_machine.add_state_trigger(run[dir_from], jump[dir_from], "jump")
                state_machine.add_state_trigger(attack[dir_from], jump[dir_from], "jump")

                state_machine.add_state_trigger(idle[dir_from], dead, "die")
                state_machine.add_state_trigger(jump[dir_from], dead, "die")
                state_machine.add_state_trigger(attack[dir_from], dead, "die")
                state_machine.add_state_trigger(run[dir_from], dead, "die")

        character.add_component(state_machine)

        circle = CircleCollider()
        circle.radius = 0.12
        rb = RigidBody2D()
        rb.body_type = BodyType.Static
        rb.is_continuous_collision = False
        rb.fixed_rotation = True

        character.add_component(circle)
        character.add_component(rb)

        character.add_component(PlayerController())
        character.transform.z_index = 5

        return character





        
