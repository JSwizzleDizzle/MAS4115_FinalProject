# Import statements
import glfw
from OpenGL.GL import *
import glm
import render_tools as rnd
import random


# Constants
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 960

# Camera
camera = rnd.Camera(45, WINDOW_WIDTH / WINDOW_HEIGHT, 0.1, 100)
fill = True



# ---------------- CALLBACK FUNCTION SETUP ---------------- #
# Callback function for window resizing
def window_size_cbfun(window, width:int, height:int):
    WINDOW_WIDTH = width
    WINDOW_HEIGHT = height
    camera.aspect_ratio = width / height
    camera.calc_perspective()
    glViewport(0, 0, width, height)



# Callback function for mouse movement
def cursor_pos_cbfun(window, xpos:float, ypos:float):
    # Check for mouse entering the window
    if not camera.active:
        camera.last_x = xpos
        camera.last_y = ypos
        camera.active = True

    # Calculate camera angle movement
    camera.angles.yaw += (xpos - camera.last_x) * camera.sensitivity
    camera.angles.pitch += (camera.last_y - ypos) * camera.sensitivity
    camera.angles.pitch = max(glm.radians(-89.5), min(camera.angles.pitch, glm.radians(89.5)))

    # Keep track of previous position
    camera.last_x = xpos
    camera.last_y = ypos



# Callback function for keyboard input
def key_press_cbfun(window, key:int, scancode:int, action:int, mods:int):
    if action == glfw.PRESS:
        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)
        if key == glfw.KEY_Z:
            global fill
            fill = not fill
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL if fill else GL_LINE)



# Camera input function 
def process_input():
    speed = camera.speed
    if glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS:
        speed *= 1.5
    
    move_direction = glm.vec3(0, 0, 0)
    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        move_direction += glm.normalize(glm.vec3(camera.front.x, 0, camera.front.z))
    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        move_direction -= glm.normalize(glm.vec3(camera.front.x, 0, camera.front.z))
    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        move_direction += camera.right
    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        move_direction -= camera.right
    if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
        move_direction += camera.up
    if glfw.get_key(window, glfw.KEY_LEFT_CONTROL) == glfw.PRESS:
        move_direction -= camera.up

    if move_direction != glm.vec3(0, 0, 0):
        camera.pos += glm.normalize(move_direction) * speed





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

    # Set GL context variables
    glClearColor(0.5294, 0.8078, 0.9216, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    glFrontFace(GL_CCW)
    
    

    # ---------------- OBJECT SETUP ---------------- #
    # Creates object geometry and buffers
    obj = rnd.RenderData(rnd.GeometryData.cube())

    # Create and use shader program (see render_tools.py)
    program = rnd.ShaderProgram("vert.glsl", "frag.glsl")
    program.activate()
    # Set sunlight parameters
    program.setUniform3f("uDirLight.data.ambient", glm.vec3(0.5))
    program.setUniform3f("uDirLight.data.diffuse", glm.vec3(0.85))
    program.setUniform3f("uDirLight.data.specular", glm.vec3(0.15))
    program.setUniform3f("uDirLight.direction", glm.vec3(0.3, -1.0, 0.2))

    # Set up camera
    camera.pos = glm.vec3(0, 8, 6)

    # Texture
    texture = rnd.Texture("stone.png")
    texture.activate()


    
    # ---------------- TERRAIN GENERATION ---------------- #
    # Generates an nxn square of blocks with y-coordinates randomly generated via perlin noise
    size = 24
    transforms = []
    glm.setSeed(int(random.random() * 2**31))
    seed = glm.linearRand(glm.vec3(-256), glm.vec3(256))
    for i in range(size**2):
        translation = glm.vec3(i % size - (size / 2), 0, (i // size) - (size / 2))
        translation.y = int(4 * glm.perlin(translation * 0.08 + seed))
        transforms.append(rnd.Transform(translation, glm.radians(0), glm.vec3(0, 1, 0), glm.vec3(0.5)))



    # ---------------- RENDER LOOP ---------------- #
    # Runs continuously while the window is open
    print("Program initialized successfully")
    while not glfw.window_should_close(window):
        # Clear previous frame info
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Take user input
        glfw.poll_events()
        process_input()

        # Update camera variables
        camera.calc_view()
        program.setUniformMat4f("uView", camera.view)
        program.setUniformMat4f("uProjection", camera.perspective)
        program.setUniform3f("uCameraPos", camera.pos)
        
        # Draw all blocks
        for trn in transforms:
            program.setUniformMat4f("uModel", trn.model_matrix())
            program.setUniformMat4f("uNormalModel", trn.normal_model_matrix())
            
            glBindVertexArray(obj.vao())
            glDrawElements(GL_TRIANGLES, obj.index_count(), GL_UNSIGNED_INT, ctypes.c_void_p(0))
        glBindVertexArray(0)

        glfw.swap_buffers(window)


    # Terminate GLFW, i.e. free allocated resources
    glfw.terminate()


