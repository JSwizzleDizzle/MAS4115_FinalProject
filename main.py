# Import statements
import glfw
from OpenGL.GL import *
import numpy as np
import glm
import render_tools as rnd




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

    glfw.set_window_pos(window, 480, 270)
    glfw.set_window_size_callback(window, window_size_cbfun)
    glfw.set_cursor_pos_callback(window, cursor_pos_cbfun)
    glfw.set_key_callback(window, key_press_cbfun)
    glfw.make_context_current(window)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    
    

    # ---------------- OBJECT SETUP ---------------- #
    # Creates object geometry and buffers
    obj = rnd.RenderData(rnd.GeometryData.cube())

    # Matrices
    transform = rnd.Transform(glm.vec3(0, 0, -5), glm.radians(0), glm.vec3(0, 0, 1), glm.vec3(1))
    view = glm.lookAt(glm.vec3(4, 4, 4), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
    projection = glm.perspective(45, WINDOW_WIDTH / WINDOW_HEIGHT, 0.1, 100)
    mvp = projection * view * transform.model_matrix()
    print(view)

    # Create and use shader program (see render_tools.py)
    program = rnd.ShaderProgram("vert.glsl", "frag.glsl")
    program.activate()

    
    # Set up camera
    camera.pos = glm.vec3(0, 0, 4)



    # ---------------- RENDER LOOP ---------------- #
    # Runs continuously while the window is open
    print("Program initialized successfully")
    glClearColor(0.1, 0.1, 0.12, 1.0)
    glEnable(GL_DEPTH_TEST)
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glfw.poll_events()
        process_input()
        camera.calc_view()

        

        transform.angle = 2 * glfw.get_time()
        transform.calc_matrix()
        theta = 0.4 * glfw.get_time()
        rad = 4

        #view = glm.lookAt(glm.vec3(rad * glm.sin(theta), 0, rad * glm.cos(theta)), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
        mvp = camera.perspective * camera.view * transform.model_matrix()
        
        program.setUniformMat4f("uModel", transform.model_matrix())
        program.setUniformMat4f("uNormalModel", transform.normal_model_matrix())
        program.setUniformMat4f("uView", view)
        program.setUniformMat4f("uProjection", projection)
        program.setUniformMat4f("uMVP", mvp)

        
        

        glBindVertexArray(obj.vao())
        glDrawElements(GL_TRIANGLES, obj.index_count(), GL_UNSIGNED_INT, ctypes.c_void_p(0))
        glBindVertexArray(0)

        glfw.swap_buffers(window)


    # Terminate GLFW, i.e. free allocated resources
    glfw.terminate()


