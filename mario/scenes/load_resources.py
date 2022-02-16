from components.spritesheet import Spritesheet
from util.asset_pool import AssetPool


def load_resources():
    AssetPool.get_shader("assets/shaders/default.glsl")

    AssetPool.add_spritesheet(
        "mario/assets/images/spritesheets/decorationsAndBlocks.png",
        Spritesheet(AssetPool.get_texture("mario/assets/images/spritesheets/decorationsAndBlocks.png"), 16, 16, 81, 0)
    )
    AssetPool.add_spritesheet(
        "mario/assets/images/spritesheet.png",
        Spritesheet(AssetPool.get_texture("mario/assets/images/spritesheet.png"), 16, 16, 26, 0)
    )
    AssetPool.add_spritesheet(
        "mario/assets/images/bigSpritesheet.png",
        Spritesheet(AssetPool.get_texture("mario/assets/images/bigSpritesheet.png"), 16, 32, 42, 0)
    )
    AssetPool.add_spritesheet(
        "mario/assets/images/items.png",
        Spritesheet(AssetPool.get_texture("mario/assets/images/items.png"), 16, 16, 35, 0)
    )
    AssetPool.add_spritesheet(
        "mario/assets/images/turtle.png",
        Spritesheet(AssetPool.get_texture("mario/assets/images/turtle.png"), 16, 24, 4, 0)
    )
    AssetPool.add_spritesheet(
        "mario/assets/images/pipes.png",
        Spritesheet(AssetPool.get_texture("mario/assets/images/pipes.png"), 32, 32, 6, 0)
    )
    AssetPool.add_spritesheet(
        "assets/images/gizmos.png",
        Spritesheet(AssetPool.get_texture("assets/images/gizmos.png"), 24, 48, 3, 0)
    )
    AssetPool.add_sound("mario/assets/sounds/1-up.ogg", loops=False)
    AssetPool.add_sound("mario/assets/sounds/bowserfalls.ogg", loops=False)
    AssetPool.add_sound("mario/assets/sounds/bowserfire.ogg", loops=False)
    AssetPool.add_sound("mario/assets/sounds/break_block.ogg", loops=False)
    AssetPool.add_sound("mario/assets/sounds/bump.ogg", loops=False)
    AssetPool.add_sound("mario/assets/sounds/coin.ogg", loops=False)
    AssetPool.add_sound("mario/assets/sounds/fireball.ogg", loops=False)
    AssetPool.add_sound("mario/assets/sounds/fireworks.ogg", loops=False)
    AssetPool.add_sound("mario/assets/sounds/flagpole.ogg", loops=False)
    AssetPool.add_sound("mario/assets/sounds/gameover.ogg", loops=False)
    AssetPool.add_sound("mario/assets/sounds/invincible.ogg", loops=False)
    AssetPool.add_sound("mario/assets/sounds/jump-small.ogg", loops=False)
    AssetPool.add_sound("mario/assets/sounds/jump-super.ogg", loops=False)
    AssetPool.add_sound("mario/assets/sounds/kick.ogg", loops=False)        
    AssetPool.add_sound("mario/assets/sounds/main-theme-overworld.ogg", loops=True)
    AssetPool.add_sound("mario/assets/sounds/mario_die.ogg", loops=False)
    AssetPool.add_sound("mario/assets/sounds/pipe.ogg", loops=False)
    AssetPool.add_sound("mario/assets/sounds/powerup.ogg", loops=False)
    AssetPool.add_sound("mario/assets/sounds/powerup_appears.ogg", loops=False)
    AssetPool.add_sound("mario/assets/sounds/stage_clear.ogg", loops=False)
    AssetPool.add_sound("mario/assets/sounds/stomp.ogg", loops=False)
    AssetPool.add_sound("mario/assets/sounds/vine.ogg", loops=False)
    AssetPool.add_sound("mario/assets/sounds/warning.ogg", loops=False)
    AssetPool.add_sound("mario/assets/sounds/world_clear.ogg", loops=False)