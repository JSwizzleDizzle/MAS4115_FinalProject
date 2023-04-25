# Import statements
import glfw
from OpenGL.GL import *
import numpy as np
import glm

import render_tools as rnd
import random




# Constants
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 960

# Camera
camera = rnd.Camera(45, WINDOW_WIDTH / WINDOW_HEIGHT, 0.1, 100)


def window_size_cbfun(window, width:int, height:int):
    WINDOW_WIDTH = width
    WINDOW_HEIGHT = height
    camera.aspect_ratio = width / height
    camera.calc_perspective()
    glViewport(0, 0, width, height)



def cursor_pos_cbfun(window, xpos:float, ypos:float):
    if not camera.active:
        camera.last_x = xpos
        camera.last_y = ypos
        camera.active = True

    camera.angles.yaw += (xpos - camera.last_x) * camera.sensitivity
    camera.angles.pitch += (camera.last_y - ypos) * camera.sensitivity

    camera.angles.pitch = max(glm.radians(-89.9), min(camera.angles.pitch, glm.radians(89.9)))

    camera.last_x = xpos
    camera.last_y = ypos



def key_press_cbfun(window, key:int, scancode:int, action:int, mods:int):
    if action == glfw.PRESS:
        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)


def process_input():
    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        camera.pos += glm.normalize(glm.vec3(camera.front.x, 0, camera.front.z)) * camera.speed
    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        camera.pos -= glm.normalize(glm.vec3(camera.front.x, 0, camera.front.z)) * camera.speed
    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        camera.pos += camera.right * camera.speed
    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        camera.pos -= camera.right * camera.speed
    if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
        camera.pos += camera.up * camera.speed
    if glfw.get_key(window, glfw.KEY_LEFT_CONTROL) == glfw.PRESS:
        camera.pos -= camera.up * camera.speed



if __name__ == "__main__":

    # ---------------- WINDOW/CONTEXT SETUP ---------------- #
    # Initialize GLFW, terminate if unsuccessful
    if not glfw.init():
        raise Exception("GLFW could not initialize.")

    # Create, verify, and configure window instance
    window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Test window", None, None)
    if not window:
        glfw.terminate()
        raise Exception("Window could not be created.")

    # Configure window
    glfw.set_window_pos(window, 480, 270)
    glfw.set_window_size_callback(window, window_size_cbfun)
    glfw.set_cursor_pos_callback(window, cursor_pos_cbfun)
    glfw.set_key_callback(window, key_press_cbfun)
    glfw.make_context_current(window)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    
    

    # ---------------- OBJECT SETUP ---------------- #
    # Creates object geometry and buffers
    obj = rnd.RenderData(rnd.GeometryData.cube())

    # Create and use shader program (see render_tools.py)
    program = rnd.ShaderProgram("vert.glsl", "frag.glsl")
    program.activate()

    # Set up camera
    camera.pos = glm.vec3(0, 8, 0)

    # Texture
    texture = rnd.Texture("dirt.jpg")
    texture.activate()


    
    # ---------------- TERRAIN GENERATION ---------------- #
    size = 24
    transforms = []
    glm.setSeed(int(random.random() * 2**31))
    seed = glm.linearRand(glm.vec3(-256), glm.vec3(256))
    for i in range(size**2):
        translation = glm.vec3(i % size - (size / 2), 0, (i // size) - (size / 2))
        translation.y = int(4 * glm.perlin(translation * 0.08 + seed))
        transforms.append(rnd.Transform(translation, glm.radians(0), glm.vec3(0, 0, 1), glm.vec3(0.5)))



    # ---------------- RENDER LOOP ---------------- #
    # Runs continuously while the window is open
    print("Program initialized successfully")
    glClearColor(0.5294, 0.8078, 0.9216, 1.0)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    glFrontFace(GL_CCW)
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glfw.poll_events()
        process_input()
        camera.calc_view()

        #transform.angle = 2 * glfw.get_time()
        
        for trn in transforms:
            mvp = camera.perspective * camera.view * trn.model_matrix()

            program.setUniformMat4f("uModel", trn.model_matrix())
            program.setUniformMat4f("uNormalModel", trn.normal_model_matrix())
            program.setUniformMat4f("uView", camera.view)
            program.setUniformMat4f("uProjection", camera.perspective)
            program.setUniformMat4f("uMVP", mvp)

            glBindVertexArray(obj.vao())
            glDrawElements(GL_TRIANGLES, obj.index_count(), GL_UNSIGNED_INT, ctypes.c_void_p(0))
            
        glBindVertexArray(0)

        glfw.swap_buffers(window)


    # Terminate GLFW, i.e. free allocated resources
    glfw.terminate()


