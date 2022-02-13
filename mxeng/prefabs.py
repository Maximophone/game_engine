from components.animation_state import AnimationState
from components.player_controller import PlayerController
from components.sprite import Sprite
from components.sprite_renderer import SpriteRenderer
from components.state_machine import StateMachine
from mxeng.game_object import GameObject
from components.transform import Transform
from physics2d.components.pillbox_collider import PillboxCollider
from physics2d.components.rigid_body_2d import RigidBody2D
from physics2d.enums.body_type import BodyType
from util.asset_pool import AssetPool

from util.vectors import Vector2

class Prefabs:
    @staticmethod
    def generate_sprite_object(sprite: Sprite, size_x: float, size_y: float) -> GameObject:
        from mxeng.window import Window
        block = Window.get_scene().create_game_object(
            "Sprite_Object_Gen", 
            Transform(
                Vector2([0., 0.]),
                Vector2([size_x, size_y])
            ))
        renderer = SpriteRenderer(sprite=sprite)
        block.add_component(renderer)
        return block

    @staticmethod
    def generate_mario() -> GameObject:
        from mxeng.window import Window
        player_sprites = AssetPool.get_spritesheet("assets/images/spritesheet.png")
        mario = Prefabs.generate_sprite_object(player_sprites.get_sprite(0), 0.25, 0.25)
        
        run: AnimationState = AnimationState("Run")
        default_frame_time = 0.23
        run.add_frame(player_sprites.get_sprite(0), default_frame_time)
        run.add_frame(player_sprites.get_sprite(2), default_frame_time)
        run.add_frame(player_sprites.get_sprite(3), default_frame_time)
        run.add_frame(player_sprites.get_sprite(2), default_frame_time)
        run.does_loop = True

        state_machine = StateMachine()
        state_machine.add_state(run)
        state_machine.set_default_state(run.title)
        
        mario.add_component(state_machine)

        pb = PillboxCollider()
        pb.width = 0.39
        pb.height = 0.31
        rb = RigidBody2D()
        rb.body_type = BodyType.Dynamic
        rb.is_continuous_collision = False
        rb.fixed_rotation = True
        rb.mass = 25.

        mario.add_component(rb)
        mario.add_component(pb)
        mario.add_component(PlayerController())

        return mario

    @staticmethod
    def generate_question_block() -> GameObject:
        from mxeng.window import Window
        items_sprites = AssetPool.get_spritesheet("assets/images/items.png")
        question_block = Prefabs.generate_sprite_object(items_sprites.get_sprite(0), 0.25, 0.25)
        
        flicker: AnimationState = AnimationState("Flicker")
        default_frame_time = 0.57
        flicker.add_frame(items_sprites.get_sprite(0), default_frame_time)
        flicker.add_frame(items_sprites.get_sprite(1), default_frame_time)
        flicker.add_frame(items_sprites.get_sprite(2), default_frame_time)
        flicker.does_loop = True

        state_machine = StateMachine()
        state_machine.add_state(flicker)
        state_machine.set_default_state(flicker.title)
        
        question_block.add_component(state_machine)

        return question_block