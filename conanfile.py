from conans import ConanFile, CMake, tools
from conans.tools import os_info, SystemPackageTool

class OgredepsConan(ConanFile):
    name = "OGREdeps"
    version = "20.19.4"
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
        tools.get("https://bitbucket.org/cabalistic/ogredeps/get/dbf4f822eb78.zip")
        tools.replace_in_file("cabalistic-ogredeps-dbf4f822eb78/src/CMakeLists.txt",
        'if (WIN32 OR (APPLE AND NOT OGRE_BUILD_PLATFORM_APPLE_IOS))',
        'if (FALSE)')

    def build(self):
        cmake = CMake(self)
        cmake.definitions['OGREDEPS_BUILD_AMD_QBS'] = 'OFF'
        cmake.definitions['OGREDEPS_BUILD_NVIDIA_NVAPI'] = 'OFF'
        cmake.definitions['OGREDEPS_BUILD_RAPIDJSON'] = 'OFF'
        cmake.definitions['OGREDEPS_BUILD_REMOTERY'] = 'OFF'
        cmake.definitions['OGREDEPS_BUILD_SDL2'] = 'OFF'
        cmake.configure(source_folder="cabalistic-ogredeps-dbf4f822eb78")
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.includedirs = ['include',
                                     'include/Cg',
                                     'include/freetype',
                                     'include/OIS',
                                     'include/zzip'
        ]
        self.cpp_info.libdirs = ['lib', 'lib/release', 'lib/debug']	 # Directories where libraries can be found
        self.cpp_info.libs = tools.collect_libs(self)
