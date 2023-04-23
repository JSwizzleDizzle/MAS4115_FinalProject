# Import statements
import glfw
from OpenGL.GL import *
import numpy as np
import glm
import render_tools as rnd



def window_size_cbfun(window, width: int, height: int):
    glViewport(0, 0, width, height)

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 960

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
    glfw.make_context_current(window)
    
    

    # ---------------- OBJECT SETUP ---------------- #
    # Creates object geometry and buffers
    plane = rnd.RenderData(rnd.GeometryData.plane())

    # Matrices
    transform = rnd.Transform(glm.vec3(0, 0, -5), glm.radians(0), glm.vec3(0, 0, 1), glm.vec3(1, 1, 1))
    view = glm.lookAt(glm.vec3(0, 0, 5), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
    projection = glm.perspective(45, WINDOW_WIDTH / WINDOW_HEIGHT, 0.1, 100)
    print(view)

    # Create and use shader program (see render_tools.py)
    program = rnd.ShaderProgram("vert.glsl", "frag.glsl")
    program.activate()
    
    

    # ---------------- RENDER LOOP ---------------- #
    # Runs continuously while the window is open
    print("Program initialized successfully")
    glClearColor(0.1, 0.1, 0.12, 1.0)
    glEnable(GL_DEPTH_TEST)
    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        transform.angle = glfw.get_time()
        transform.calc_matrix()
        
        program.setUniformMat4f("uModel", transform.model_matrix())
        program.setUniformMat4f("uNormalModel", transform.normal_model_matrix())
        #program.setUniformMat4f("uView", view)
        #program.setUniformMat4f("uProjection", projection)

        glBindVertexArray(plane.vao())
        glDrawElements(GL_TRIANGLES, plane.index_count(), GL_UNSIGNED_INT, ctypes.c_void_p(0))
        glBindVertexArray(0)


        glfw.swap_buffers(window)


    # Terminate GLFW, i.e. free allocated resources
    glfw.terminate()


