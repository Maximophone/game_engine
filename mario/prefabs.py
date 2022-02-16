from components.animation_state import AnimationState
from mario.components.breakable_brick import BreakableBrick
from mario.components.coin import Coin
from mario.components.coin_block import CoinBlock
from mario.components.fireball import Fireball
from mario.components.flagpole import Flagpole
from mario.components.flower import Flower
from mario.components.goomba_ai import GoombaAI
from mario.components.ground import Ground
from mario.components.mushroom_ai import MushroomAI
from mario.components.pipe import Pipe
from mario.components.player_controller import PlayerController
from mario.components.question_block import QuestionBlock
from components.sprite import Sprite
from components.sprite_renderer import SpriteRenderer
from components.state_machine import StateMachine
from mario.components.turtle_ai import TurtleAI
from mxeng.direction import Direction
from mxeng.game_object import GameObject
from components.transform import Transform
from physics2d.components.box_2d_collider import Box2DCollider
from physics2d.components.circle_collider import CircleCollider
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
    def generate_ground_block(sprite: Sprite) -> GameObject:
        block = Prefabs.generate_sprite_object(sprite, 0.25, 0.25)
        rb = RigidBody2D()
        rb.body_type = BodyType.Static
        block.add_component(rb)
        b2d = Box2DCollider()
        b2d.half_size = Vector2([0.25, 0.25]
        )
        block.add_component(b2d)
        block.add_component(Ground())
        return block

    @staticmethod
    def generate_breakable_block(sprite: Sprite) -> GameObject:
        block = Prefabs.generate_ground_block(sprite)
        block.add_component(BreakableBrick())
        return block

    @staticmethod
    def generate_mario() -> GameObject:
        player_sprites = AssetPool.get_spritesheet("mario/assets/images/spritesheet.png")
        big_player_sprites = AssetPool.get_spritesheet("mario/assets/images/bigSpritesheet.png")
        mario = Prefabs.generate_sprite_object(player_sprites.get_sprite(0), 0.25, 0.25)
        
        run = AnimationState("Run")
        default_frame_time = 0.23
        run.add_frame(player_sprites.get_sprite(0), default_frame_time)
        run.add_frame(player_sprites.get_sprite(2), default_frame_time)
        run.add_frame(player_sprites.get_sprite(3), default_frame_time)
        run.add_frame(player_sprites.get_sprite(2), default_frame_time)
        run.does_loop = True

        switch_direction = AnimationState("Switch Direction")
        switch_direction.add_frame(player_sprites.get_sprite(4), 0.1)
        switch_direction.does_loop = False

        idle = AnimationState("Idle")
        idle.add_frame(player_sprites.get_sprite(0), 0.1)
        idle.does_loop = False

        jump = AnimationState("Jump")
        jump.add_frame(player_sprites.get_sprite(5), 0.1)
        jump.does_loop = False

        # Big mario animations
        big_run = AnimationState("Big Run")
        big_run.add_frame(big_player_sprites.get_sprite(0), default_frame_time)
        big_run.add_frame(big_player_sprites.get_sprite(1), default_frame_time)
        big_run.add_frame(big_player_sprites.get_sprite(2), default_frame_time)
        big_run.add_frame(big_player_sprites.get_sprite(3), default_frame_time)
        big_run.add_frame(big_player_sprites.get_sprite(2), default_frame_time)
        big_run.add_frame(big_player_sprites.get_sprite(1), default_frame_time)
        big_run.does_loop = True

        big_switch_direction = AnimationState("Big Switch Direction")
        big_switch_direction.add_frame(big_player_sprites.get_sprite(4), 0.1)
        big_switch_direction.does_loop = False

        big_idle = AnimationState("BigIdle")
        big_idle.add_frame(big_player_sprites.get_sprite(0), 0.1)
        big_idle.does_loop = False

        big_jump = AnimationState("BigJump")
        big_jump.add_frame(big_player_sprites.get_sprite(5), 0.1)
        big_jump.does_loop = False

        #Fire mario animations
        fire_offset = 21
        fire_run = AnimationState("FireRun")
        fire_run.add_frame(big_player_sprites.get_sprite(fire_offset + 0), default_frame_time)
        fire_run.add_frame(big_player_sprites.get_sprite(fire_offset + 1), default_frame_time)
        fire_run.add_frame(big_player_sprites.get_sprite(fire_offset + 2), default_frame_time)
        fire_run.add_frame(big_player_sprites.get_sprite(fire_offset + 3), default_frame_time)
        fire_run.add_frame(big_player_sprites.get_sprite(fire_offset + 2), default_frame_time)
        fire_run.add_frame(big_player_sprites.get_sprite(fire_offset + 1), default_frame_time)
        fire_run.does_loop = True

        fire_switch_direction = AnimationState("Fire Switch Direction")
        fire_switch_direction.add_frame(big_player_sprites.get_sprite(fire_offset + 4), 0.1)
        fire_switch_direction.does_loop = False

        fire_idle = AnimationState("FireIdle")
        fire_idle.add_frame(big_player_sprites.get_sprite(fire_offset + 0), 0.1)
        fire_idle.does_loop = False

        fire_jump = AnimationState("FireJump")
        fire_jump.add_frame(big_player_sprites.get_sprite(fire_offset + 5), 0.1)
        fire_jump.does_loop = False

        die = AnimationState("Die")
        die.add_frame(player_sprites.get_sprite(6), 0.1)
        die.does_loop = False

        state_machine = StateMachine()
        state_machine.add_state(run)
        state_machine.add_state(switch_direction)
        state_machine.add_state(idle)
        state_machine.add_state(jump)
        state_machine.add_state(die)

        state_machine.add_state(big_run)
        state_machine.add_state(big_idle)
        state_machine.add_state(big_switch_direction)
        state_machine.add_state(big_jump)

        state_machine.add_state(fire_run)
        state_machine.add_state(fire_idle)
        state_machine.add_state(fire_switch_direction)
        state_machine.add_state(fire_jump)

        state_machine.set_default_state(idle.title)

        state_machine.add_state_trigger(run.title, switch_direction.title, "switch_direction");
        state_machine.add_state_trigger(run.title, idle.title, "stop_running");
        state_machine.add_state_trigger(run.title, jump.title, "jump");
        state_machine.add_state_trigger(switch_direction.title, idle.title, "stop_running");
        state_machine.add_state_trigger(switch_direction.title, run.title, "start_running");
        state_machine.add_state_trigger(switch_direction.title, jump.title, "jump");
        state_machine.add_state_trigger(idle.title, run.title, "start_running");
        state_machine.add_state_trigger(idle.title, jump.title, "jump");
        state_machine.add_state_trigger(jump.title, idle.title, "stop_jumping");

        state_machine.add_state_trigger(big_run.title, big_switch_direction.title, "switch_direction");
        state_machine.add_state_trigger(big_run.title, big_idle.title, "stop_running");
        state_machine.add_state_trigger(big_run.title, big_jump.title, "jump");
        state_machine.add_state_trigger(big_switch_direction.title, big_idle.title, "stop_running");
        state_machine.add_state_trigger(big_switch_direction.title, big_run.title, "start_running");
        state_machine.add_state_trigger(big_switch_direction.title, big_jump.title, "jump");
        state_machine.add_state_trigger(big_idle.title, big_run.title, "start_running");
        state_machine.add_state_trigger(big_idle.title, big_jump.title, "jump");
        state_machine.add_state_trigger(big_jump.title, big_idle.title, "stop_jumping");

        state_machine.add_state_trigger(fire_run.title, fire_switch_direction.title, "switch_direction");
        state_machine.add_state_trigger(fire_run.title, fire_idle.title, "stop_running");
        state_machine.add_state_trigger(fire_run.title, fire_jump.title, "jump");
        state_machine.add_state_trigger(fire_switch_direction.title, fire_idle.title, "stop_running");
        state_machine.add_state_trigger(fire_switch_direction.title, fire_run.title, "start_running");
        state_machine.add_state_trigger(fire_switch_direction.title, fire_jump.title, "jump");
        state_machine.add_state_trigger(fire_idle.title, fire_run.title, "start_running");
        state_machine.add_state_trigger(fire_idle.title, fire_jump.title, "jump");
        state_machine.add_state_trigger(fire_jump.title, fire_idle.title, "stop_jumping");

        state_machine.add_state_trigger(run.title, big_run.title, "powerup");
        state_machine.add_state_trigger(idle.title, big_idle.title, "powerup");
        state_machine.add_state_trigger(switch_direction.title, big_switch_direction.title, "powerup");
        state_machine.add_state_trigger(jump.title, big_jump.title, "powerup");
        state_machine.add_state_trigger(big_run.title, fire_run.title, "powerup");
        state_machine.add_state_trigger(big_idle.title, fire_idle.title, "powerup");
        state_machine.add_state_trigger(big_switch_direction.title, fire_switch_direction.title, "powerup");
        state_machine.add_state_trigger(big_jump.title, fire_jump.title, "powerup");

        state_machine.add_state_trigger(big_run.title, run.title, "damage");
        state_machine.add_state_trigger(big_idle.title, idle.title, "damage");
        state_machine.add_state_trigger(big_switch_direction.title, switch_direction.title, "damage");
        state_machine.add_state_trigger(big_jump.title, jump.title, "damage");
        state_machine.add_state_trigger(fire_run.title, big_run.title, "damage");
        state_machine.add_state_trigger(fire_idle.title, big_idle.title, "damage");
        state_machine.add_state_trigger(fire_switch_direction.title, big_switch_direction.title, "damage");
        state_machine.add_state_trigger(fire_jump.title, big_jump.title, "damage");

        state_machine.add_state_trigger(run.title, die.title, "die");
        state_machine.add_state_trigger(switch_direction.title, die.title, "die");
        state_machine.add_state_trigger(idle.title, die.title, "die");
        state_machine.add_state_trigger(jump.title, die.title, "die");
        state_machine.add_state_trigger(big_run.title, run.title, "die");
        state_machine.add_state_trigger(big_switch_direction.title, switch_direction.title, "die");
        state_machine.add_state_trigger(big_idle.title, idle.title, "die");
        state_machine.add_state_trigger(big_jump.title, jump.title, "die");
        state_machine.add_state_trigger(fire_run.title, big_run.title, "die");
        state_machine.add_state_trigger(fire_switch_direction.title, big_switch_direction.title, "die");
        state_machine.add_state_trigger(fire_idle.title, big_idle.title, "die");
        state_machine.add_state_trigger(fire_jump.title, big_jump.title, "die");

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

        mario.transform.z_index = 10

        return mario

    @staticmethod
    def generate_question_block() -> GameObject:
        items_sprites = AssetPool.get_spritesheet("mario/assets/images/items.png")
        question_block = Prefabs.generate_sprite_object(items_sprites.get_sprite(0), 0.25, 0.25)
        
        flicker = AnimationState("Flicker")
        default_frame_time = 0.23
        flicker.add_frame(items_sprites.get_sprite(0), default_frame_time)
        flicker.add_frame(items_sprites.get_sprite(1), default_frame_time)
        flicker.add_frame(items_sprites.get_sprite(2), default_frame_time)
        flicker.does_loop = True

        inactive = AnimationState("Inactive")
        inactive.add_frame(items_sprites.get_sprite(3), 0.1)
        inactive.does_loop = False

        state_machine = StateMachine()
        state_machine.add_state(flicker)
        state_machine.add_state(inactive)
        state_machine.set_default_state(flicker.title)

        state_machine.add_state_trigger(flicker.title, inactive.title, "set_inactive")
        
        question_block.add_component(state_machine)
        question_block.add_component(QuestionBlock())
        rb = RigidBody2D()
        rb.body_type = BodyType.Static
        question_block.add_component(rb)
        b2d = Box2DCollider()
        b2d.half_size = Vector2([0.25, 0.25])
        question_block.add_component(b2d)
        question_block.add_component(Ground())

        return question_block

    @staticmethod
    def generate_coin_block() -> GameObject:
        items_sprites = AssetPool.get_spritesheet("mario/assets/images/items.png")
        coin = Prefabs.generate_sprite_object(items_sprites.get_sprite(7), 0.25, 0.25)
        
        coin_flip = AnimationState("Coin Flip")
        default_frame_time = 0.23
        coin_flip.add_frame(items_sprites.get_sprite(7), default_frame_time)
        coin_flip.add_frame(items_sprites.get_sprite(8), default_frame_time)
        coin_flip.add_frame(items_sprites.get_sprite(9), default_frame_time)
        coin_flip.does_loop = True

        state_machine = StateMachine()
        state_machine.add_state(coin_flip)
        state_machine.set_default_state(coin_flip.title)
        
        coin.add_component(state_machine)
        coin.add_component(CoinBlock())

        return coin

    @staticmethod
    def generate_coin() -> GameObject:
        items_sprites = AssetPool.get_spritesheet("mario/assets/images/items.png")
        coin = Prefabs.generate_sprite_object(items_sprites.get_sprite(7), 0.25, 0.25)
        
        coin_flip = AnimationState("Coin Flip")
        default_frame_time = 0.23
        coin_flip.add_frame(items_sprites.get_sprite(7), default_frame_time)
        coin_flip.add_frame(items_sprites.get_sprite(8), default_frame_time)
        coin_flip.add_frame(items_sprites.get_sprite(9), default_frame_time)
        coin_flip.does_loop = True

        state_machine = StateMachine()
        state_machine.add_state(coin_flip)
        state_machine.set_default_state(coin_flip.title)
        
        coin.add_component(state_machine)
        coin.add_component(Coin())

        circle_collider = CircleCollider()
        circle_collider.radius = 0.12
        coin.add_component(circle_collider)
        rb = RigidBody2D()
        rb.body_type = BodyType.Static
        coin.add_component(rb)

        return coin

    @staticmethod
    def generate_mushroom() -> GameObject:
        items_sprites = AssetPool.get_spritesheet("mario/assets/images/items.png")
        mushroom = Prefabs.generate_sprite_object(items_sprites.get_sprite(10), 0.25, 0.25)
        
        rb = RigidBody2D()
        rb.body_type = BodyType.Dynamic
        rb.fixed_rotation = True
        rb.is_continuous_collision = False
        mushroom.add_component(rb)

        circle_collider = CircleCollider()
        circle_collider.radius = 0.14
        mushroom.add_component(circle_collider)
        mushroom.add_component(MushroomAI())

        return mushroom

    @staticmethod
    def generate_flower() -> GameObject:
        items_sprites = AssetPool.get_spritesheet("mario/assets/images/items.png")
        flower = Prefabs.generate_sprite_object(items_sprites.get_sprite(20), 0.25, 0.25)
        
        rb = RigidBody2D()
        rb.body_type = BodyType.Static
        rb.fixed_rotation = True
        rb.is_continuous_collision = False
        flower.add_component(rb)

        circle_collider = CircleCollider()
        circle_collider.radius = 0.14
        flower.add_component(circle_collider)
        flower.add_component(Flower())

        return flower

    @staticmethod
    def generate_goomba() -> GameObject:
        sprites = AssetPool.get_spritesheet("mario/assets/images/spritesheet.png")
        goomba = Prefabs.generate_sprite_object(sprites.get_sprite(14), 0.25, 0.25)
        
        walk = AnimationState("Walk")
        default_frame_time = 0.23
        walk.add_frame(sprites.get_sprite(14), default_frame_time)
        walk.add_frame(sprites.get_sprite(15), default_frame_time)
        walk.does_loop = True

        squashed = AnimationState("Squashed")
        squashed.add_frame(sprites.get_sprite(16), 0.1)
        squashed.does_loop = False

        state_machine = StateMachine()
        state_machine.add_state(walk)
        state_machine.add_state(squashed)
        state_machine.set_default_state(walk.title)
        
        state_machine.add_state_trigger(walk.title, squashed.title, "squash_me")

        goomba.add_component(state_machine)
        rb = RigidBody2D()
        rb.body_type = BodyType.Dynamic
        rb.mass = 0.1
        rb.fixed_rotation = True
        goomba.add_component(rb)

        circle = CircleCollider()
        circle.radius = 0.12
        goomba.add_component(circle)

        goomba.add_component(GoombaAI())

        return goomba

    @staticmethod
    def generate_turtle() -> GameObject:
        turtle_sprites = AssetPool.get_spritesheet("mario/assets/images/turtle.png")
        turtle = Prefabs.generate_sprite_object(turtle_sprites.get_sprite(0), 0.25, 0.35)
        
        walk = AnimationState("Walk")
        default_frame_time = 0.23
        walk.add_frame(turtle_sprites.get_sprite(0), default_frame_time)
        walk.add_frame(turtle_sprites.get_sprite(1), default_frame_time)
        walk.does_loop = True

        squashed = AnimationState("Turtle Shell Spin")
        squashed.add_frame(turtle_sprites.get_sprite(2), 0.1)
        squashed.does_loop = False

        state_machine = StateMachine()
        state_machine.add_state(walk)
        state_machine.add_state(squashed)
        state_machine.set_default_state(walk.title)
        
        state_machine.add_state_trigger(walk.title, squashed.title, "squash_me")

        turtle.add_component(state_machine)
        rb = RigidBody2D()
        rb.body_type = BodyType.Dynamic
        rb.mass = 0.1
        rb.fixed_rotation = True
        turtle.add_component(rb)

        circle = CircleCollider()
        circle.radius = 0.13
        circle.offset = Vector2([0., -0.05])
        turtle.add_component(circle)

        turtle.add_component(TurtleAI())

        return turtle

    @staticmethod
    def generate_fireball(position: Vector2) -> GameObject:
        items_sprites = AssetPool.get_spritesheet("mario/assets/images/items.png")
        fireball = Prefabs.generate_sprite_object(items_sprites.get_sprite(32), 0.18, 0.18)
        fireball.transform.position = position
        
        rb = RigidBody2D()
        rb.body_type = BodyType.Dynamic
        rb.fixed_rotation = True
        rb.is_continuous_collision = False
        fireball.add_component(rb)

        circle_collider = CircleCollider()
        circle_collider.radius = 0.08
        fireball.add_component(circle_collider)
        fireball.add_component(Fireball())

        return fireball

    @staticmethod
    def generate_flag_top() -> GameObject:
        items_sprites = AssetPool.get_spritesheet("mario/assets/images/items.png")
        flagtop = Prefabs.generate_sprite_object(items_sprites.get_sprite(6), 0.25, 0.25)
        
        rb = RigidBody2D()
        rb.body_type = BodyType.Static
        rb.is_continuous_collision = False
        flagtop.add_component(rb)

        box_collider = Box2DCollider()
        box_collider.half_size = Vector2([0.1, 0.25])
        box_collider.offset = Vector2([-0.075, 0.0])
        flagtop.add_component(box_collider)
        flagtop.add_component(Flagpole(True))

        return flagtop

    @staticmethod
    def generate_flag_pole() -> GameObject:
        items_sprites = AssetPool.get_spritesheet("mario/assets/images/items.png")
        flagpole = Prefabs.generate_sprite_object(items_sprites.get_sprite(33), 0.25, 0.25)
        
        rb = RigidBody2D()
        rb.body_type = BodyType.Static
        rb.is_continuous_collision = False
        flagpole.add_component(rb)

        box_collider = Box2DCollider()
        box_collider.half_size = Vector2([0.1, 0.25])
        box_collider.offset = Vector2([-0.075, 0.0])
        flagpole.add_component(box_collider)
        flagpole.add_component(Flagpole(False))

        return flagpole

    @staticmethod
    def generate_pipe(direction: Direction) -> GameObject:
        print(direction)
        pipes = AssetPool.get_spritesheet("mario/assets/images/pipes.png")

        sprite_index = {
                Direction.Down: 0,
                Direction.Up: 1,
                Direction.Right: 2,
                Direction.Left: 3,
        }[direction]

        pipe = Prefabs.generate_sprite_object(pipes.get_sprite(sprite_index), 0.5, 0.5)
        rb = RigidBody2D()
        rb.body_type = BodyType.Static
        rb.fixed_rotation = True
        rb.is_continuous_collision = False
        pipe.add_component(rb)

        b2d = Box2DCollider()
        b2d.half_size = Vector2([0.5, 0.5])
        pipe.add_component(b2d)

        pipe.add_component(Pipe(direction))
        pipe.add_component(Ground())

        return pipe