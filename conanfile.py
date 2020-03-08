from conans import ConanFile, CMake, tools
import os


class DracoConan(ConanFile):
    name = "draco"
    version = "1.3.6"
    generators = "cmake"
    settings = {"os": None, "arch": ["x86_64", "x86"], "compiler": None, "build_type": None}

    options = {"shared": [True, False]}
    default_options = "shared=True"
    exports_sources = "include*", "src*", "cmake*", "CMakeLists.txt"

    exports = ["CMakeLists.txt"]

    license = "Licensed under the Apache License, Version 2.0"
    description = "A library for compressing and decompressing 3D geometric meshes and point clouds"

    scm = {
        "type": "git",
        "subfolder": "sources",
        "url": "https://github.com/google/draco.git",
        "revision": "%s" % version,
    }
    
    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.configure()
        cmake.build()

    def package(self):
        self.copy(pattern="*.h", dst="include", src="src", excludes=("draco/unity","draco/maya"))
        self.copy(pattern="*.h", dst="include/draco", src="draco")
        self.copy(pattern="*.so*", dst="lib", keep_path=False, excludes=("unity","maya") )
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
