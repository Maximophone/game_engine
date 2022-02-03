import imgui
import ctypes

from mxeng.game_object import GameObject

class SceneHierarchyWindow:
    payload_drag_drop_type = "SceneHierarchy"
    def imgui(self):
        from mxeng.window import Window
        imgui.begin("Scene Hierarchy")

        game_objects = Window.get_scene().get_game_objects()
        index = 0
        for go in game_objects:
            if not go.do_serialize:
                continue

            tree_node_open = self.do_tree_node(go, index)

            if tree_node_open:
                imgui.tree_pop()

            index += 1

        imgui.end()

    def do_tree_node(self, go: GameObject, index: int) -> bool:
        imgui.push_id(str(index))
        tree_node_open = imgui.tree_node(str(go.name), flags=imgui.TREE_NODE_DEFAULT_OPEN | imgui.TREE_NODE_FRAME_PADDING | imgui.TREE_NODE_OPEN_ON_ARROW)
        imgui.pop_id()

        if imgui.begin_drag_drop_source():
            # starting to drag something
            imgui.set_drag_drop_payload(SceneHierarchyWindow.payload_drag_drop_type, str(id(go)).encode("utf-8"))
            imgui.text(go.name)
            imgui.end_drag_drop_source()

        if imgui.begin_drag_drop_target():
            payload = imgui.accept_drag_drop_payload(SceneHierarchyWindow.payload_drag_drop_type)
            if payload is not None:
                game_object_id = int(payload.decode("utf-8"))
                # HACK: we pass the memory id of the object in the payload and use cyptes to retrieve the object
                # If the object does not exist anymore, it will crash
                game_object: GameObject = ctypes.cast(game_object_id, ctypes.py_object).value
                print(f"Payload accepted: {game_object.name}")

            imgui.end_drag_drop_target()

        return tree_node_open
