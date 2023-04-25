# Import statements
from OpenGL.GL import *
from PIL import Image as img
import numpy as np
import glm



class GeometryData:
    """
    A basic data class to group vertex and index data
    Serves as a namespace for functions that generate primitive solids
    """
    def __init__(self, verts, inds):
        self.verts = verts
        self.inds = inds


    def plane():
        verts = np.array([
            0.5, -0.5, 0,   0.0, 0.0, 1.0,   1.0, 0.0, 
            0.5,  0.5, 0,   0.0, 0.0, 1.0,   1.0, 1.0, 
            -0.5,  0.5, 0,   0.0, 0.0, 1.0,   0.0, 1.0, 
            -0.5, -0.5, 0,   0.0, 0.0, 1.0,   0.0, 0.0
        ], dtype=np.float32)

        inds = np.array([
            0, 1, 2,
            2, 3, 0
        ], dtype=np.uint32)

        return GeometryData(verts, inds)
    

    def cube():
        verts = np.array([
            1.0, -1.0, -1.0,    1.0,  0.0,  0.0,   1.0, 0.0,
            1.0,  1.0, -1.0,    1.0,  0.0,  0.0,   1.0, 1.0,
            1.0,  1.0,  1.0,    1.0,  0.0,  0.0,   0.0, 1.0,
            1.0, -1.0,  1.0,    1.0,  0.0,  0.0,   0.0, 0.0,
            
            1.0,  1.0,  1.0,    0.0,  1.0,  0.0,   1.0, 0.0,
            1.0,  1.0, -1.0,    0.0,  1.0,  0.0,   1.0, 1.0,
            -1.0,  1.0, -1.0,    0.0,  1.0,  0.0,   0.0, 1.0,
            -1.0,  1.0,  1.0,    0.0,  1.0,  0.0,   0.0, 0.0,

            1.0, -1.0,  1.0,    0.0,  0.0,  1.0,   1.0, 0.0,
            1.0,  1.0,  1.0,    0.0,  0.0,  1.0,   1.0, 1.0,
            -1.0,  1.0,  1.0,    0.0,  0.0,  1.0,   0.0, 1.0,
            -1.0, -1.0,  1.0,    0.0,  0.0,  1.0,   0.0, 0.0,

            -1.0, -1.0,  1.0,   -1.0,  0.0,  0.0,   1.0, 0.0,
            -1.0,  1.0,  1.0,   -1.0,  0.0,  0.0,   1.0, 1.0,
            -1.0,  1.0, -1.0,   -1.0,  0.0,  0.0,   0.0, 1.0,
            -1.0, -1.0, -1.0,   -1.0,  0.0,  0.0,   0.0, 0.0,
            
            1.0, -1.0,  1.0,    0.0, -1.0,  0.0,   0.0, 1.0,
            -1.0, -1.0,  1.0,    0.0, -1.0,  0.0,   1.0, 1.0,
            -1.0, -1.0, -1.0,    0.0, -1.0,  0.0,   1.0, 0.0,
            1.0, -1.0, -1.0,    0.0, -1.0,  0.0,   0.0, 0.0,
            
            1.0, -1.0, -1.0,    0.0,  0.0, -1.0,   0.0, 0.0,
            -1.0, -1.0, -1.0,    0.0,  0.0, -1.0,   1.0, 0.0,
            -1.0,  1.0, -1.0,    0.0,  0.0, -1.0,   1.0, 1.0,
            1.0,  1.0, -1.0,    0.0,  0.0, -1.0,   0.0, 1.0,
            
        ], dtype=np.float32)

        inds = np.array([
            0, 1, 2,
            2, 3, 0,

            4, 5, 6, 
            6, 7, 4, 

            8, 9, 10, 
            10, 11, 8, 

            12, 13, 14, 
            14, 15, 12, 

            16, 17, 18, 
            18, 19, 16,

            20, 21, 22, 
            22, 23, 20
        ], dtype=np.uint32)

        return GeometryData(verts, inds)





class Transform:
    """
    Stores 3D transformation information based on:
    - a 3D translation vector
    - a 3D rotation axis and the angle about said axis
    - a 3D vector containing scaling components along each axis
    The transformation matrix is only recalculated when explicitly instructed to save computations
    """
    def __init__(self, translation = glm.vec3(0, 0, 0), angle:float = 0, axis = glm.vec3(0, 1, 0), scale = glm.vec3(1, 1, 1)):
        self.translation = translation
        self.angle = angle
        self.axis = axis
        self.scale = scale
        self.__model_matrix = glm.mat4(1.0)
        self.__normal_model_matrix = glm.mat4(1.0)
        self.calc_matrix()


    def calc_matrix(self):
        #glm.translate(glm.rotate(glm.scale(self.scale), self.angle, self.axis), self.translation)
        self.__model_matrix = glm.scale(glm.rotate(glm.translate(glm.mat4(1.0), self.translation), self.angle, self.axis), self.scale)
        self.__normal_model_matrix = glm.inverse(glm.transpose(self.__model_matrix))


    def model_matrix(self):
        return self.__model_matrix
    
    def normal_model_matrix(self):
        return self.__normal_model_matrix





class RenderData:
    """
    Manages the creation and storage of buffer objects (VAO, VBO, EBO)
    Keeps track of vertex/index count for drawing
    """
    def __init__(self, geometry: GeometryData, draw_type = GL_STATIC_DRAW):
        # Create object buffers
        self.__VAO = glGenVertexArrays(1)
        self.__VBO = glGenBuffers(1)
        self.__EBO = glGenBuffers(1)
        self.__vertex_count = len(geometry.verts)
        self.__index_count = len(geometry.inds)

        # Bind VAO
        glBindVertexArray(self.__VAO)

        # Bind and configure VBO (raw vertex data)
        glBindBuffer(GL_ARRAY_BUFFER, self.__VBO)
        glBufferData(GL_ARRAY_BUFFER, geometry.verts.nbytes, geometry.verts, draw_type)

        # Bind and configure EBO (connectivity data)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.__EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, geometry.inds.nbytes, geometry.inds, draw_type)

        # Specify vertex position, normal, and uv attributes
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(24))
        # Enable attributes
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glEnableVertexAttribArray(2)

        # Unbind VAO
        glBindVertexArray(0)


    def vao(self):
        return self.__VAO
    
    def vbo(self):
        return self.__VBO
    
    def ebo(self):
        return self.__EBO

    def vertex_count(self):
        return self.__vertex_count

    def index_count(self):
        return self.__index_count
    




class Texture():
    """
    Creates an OpenGL texture object from a file directory
    """

    # Static member that contains the path to the shader locations
    directory = "textures/"

    def __init__(self, path):
        # Image
        image = img.open(Texture.directory + path)
        image = image.transpose(img.FLIP_TOP_BOTTOM)
        self.__data = image.convert("RGBA").tobytes()

        # Texture
        self.__id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.__id)
        # Wrapping mode
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        # Filter mode
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.__data)
        glBindTexture(GL_TEXTURE_2D, 0)


    def activate(self):
        glBindTexture(GL_TEXTURE_2D, self.__id)
        glActiveTexture(GL_TEXTURE0)

    def deactivate(self):
        glBindTexture(GL_TEXTURE_2D, 0)





class EulerAngles:
    """
    A simple data class containing Euler angle data.
    Pitch is up/down tilt
    Yaw is side-to-side rotation
    Roll is rotation along the viewing axis
    """
    def __init__(self, pitch:float = 0, yaw:float = 0, roll:float = 0):
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll





class Camera:
    """
    Represents a perspective camera in 3D space
    Takes parameters for perspective projection (field-of-view, aspect ratio, clip bounds)
    Starts at the origin facing the negative z axis
    """
    def __init__(self, fov:float = 45, aspect_ratio:float = 16 / 9, near_clip:float = 0.1, far_clip:float = 100):
        self.fov = fov
        self.aspect_ratio = aspect_ratio
        self.near_clip = near_clip
        self.far_clip = far_clip
        self.perspective = glm.perspective(self.fov, self.aspect_ratio, self.near_clip, self.far_clip)

        self.pos = glm.vec3(0)
        self.front = glm.vec3(0, 0, -1)
        self.right = glm.vec3(1, 0, 0)
        self.up = glm.vec3(0, 1, 0)

        self.angles = EulerAngles()
        self.view = glm.lookAt(self.pos, self.pos + self.front, self.up)

        self.last_x = 0
        self.last_y = 0

        self.sensitivity = 0.002
        self.speed = 0.08

        self.active = False
        

    def calc_view(self):
        self.front = glm.vec3(glm.cos(self.angles.pitch) * glm.sin(self.angles.yaw), glm.sin(self.angles.pitch), glm.cos(self.angles.pitch) * -glm.cos(self.angles.yaw))
        self.up = glm.vec3(0, 1, 0)   # glm.vec3(glm.sin(self.angles.roll) * self.__front.x, glm.cos(self.angles.roll), glm.sin(self.angles.roll) * self.__front.z)
        self.right = glm.normalize(glm.cross(self.front, self.up))
        self.view = glm.lookAt(self.pos, self.pos + self.front, self.up)

    def calc_perspective(self):
        self.perspective = glm.perspective(self.fov, self.aspect_ratio, self.near_clip, self.far_clip)





class ShaderProgram:
    """
    Creates a GLSL shader program from vertex fragment shader source paths as arguments.
    Encapsulates shader interactivity including program activation and passing of uniforms.
    """

    # Static member that contains the path to the shader locations
    directory = "shaders/"

    def __init__(self, vertex_path: str, fragment_path: str):
        # Initialize shader components
        vertex_id = self.__initShader(vertex_path, GL_VERTEX_SHADER)
        fragment_id = self.__initShader(fragment_path, GL_FRAGMENT_SHADER)

        # Link components into program
        self.__id = glCreateProgram()
        glAttachShader(self.__id, vertex_id)
        glAttachShader(self.__id, fragment_id)
        glLinkProgram(self.__id)

        # Check for linking errors
        result = glGetProgramiv(self.__id, GL_LINK_STATUS)
        if not result:
            raise RuntimeError(f"ERROR::SHADER::LINK {vertex_path} and {fragment_path} could not be linked: {result}, {glGetProgramInfoLog(self.__id)}")
        
        # Get rid of shader pipeline components
        glDetachShader(self.__id, vertex_id)
        glDetachShader(self.__id, fragment_id)

        glDeleteShader(vertex_id)
        glDeleteShader(fragment_id)



    def activate(self):
        glUseProgram(self.__id)

    def deactivate(self):
        glUseProgram(0);
    


    def setUniformMat4f(self, name: str, mat4):
        glUniformMatrix4fv(glGetUniformLocation(self.__id, name), 1, GL_FALSE, np.array(mat4.to_list()))



    def __initShader(self, path: str, type):
        """
        Helper method that creates and configures individual shader pipeline components
        """

        # Read shader source from file
        file = open(ShaderProgram.directory + path, "r")
        source = file.read()
        file.close()

        # Create shader object and compile source
        id = glCreateShader(type)
        glShaderSource(id, source)
        glCompileShader(id)

        # Check for compilation errors
        result = glGetShaderiv(id, GL_COMPILE_STATUS)
        if not result:
            raise RuntimeError(f"ERROR::SHADER::COMPILE: Shader {path} could not be compiled: {result}, {glGetShaderInfoLog(id)}")
        
        return id
    

