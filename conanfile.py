from conans import ConanFile, CMake, tools
from conans.tools import os_info, SystemPackageTool

class OgredepsConan(ConanFile):
    name = "OGREdeps"
    version = "2018-07"
    url = "https://github.com/AnotherFoxGuy/conan-ogredeps"
    description = "This package is provided as a quick route to compile the core dependencies of OGRE (http://www.ogre3d.org) on most supported platforms."
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def system_requirements(self):
        if os_info.is_linux:
            if os_info.with_apt:
                installer = SystemPackageTool()
                installer.install("libx11-dev")

    def source(self):
        tools.get("https://bitbucket.org/cabalistic/ogredeps/get/019e46bf5ce0.zip")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
#        tools.replace_in_file("hello/CMakeLists.txt", "PROJECT(MyHello)",
#                              '''PROJECT(MyHello)
#include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
#conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.definitions['OGREDEPS_BUILD_AMD_QBS'] = 'OFF'
        cmake.definitions['OGREDEPS_BUILD_NVIDIA_NVAPI'] = 'OFF'
        cmake.definitions['OGREDEPS_BUILD_RAPIDJSON'] = 'OFF'
        cmake.definitions['OGREDEPS_BUILD_REMOTERY'] = 'OFF'
        cmake.definitions['OGREDEPS_BUILD_SDL2'] = 'OFF'
        cmake.configure(source_folder="cabalistic-ogredeps-019e46bf5ce0")
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.configure(source_folder="cabalistic-ogredeps-019e46bf5ce0")
        cmake.install()

    def package_info(self):
        self.cpp_info.libdirs = ['lib', 'lib/release', 'lib/debug']	 # Directories where libraries can be found
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.build_type == "Release":
            self.cpp_info.libs.extend(tools.collect_libs(self, folder="lib/release"))
        else:
            self.cpp_info.libs.extend(tools.collect_libs(self, folder="lib/debug"))
